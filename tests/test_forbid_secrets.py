import os
import json
import yaml
import pytest
from hooks.forbid_secrets import (
    check_secret,
    check_template_content,
    main,
    extract_yaml_documents,
)
import sys


def load_yaml_file(filename):
    """Load YAML file from the fixtures directory."""
    filepath = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def load_json_file(filename):
    """Load JSON file from the fixtures directory."""
    filepath = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(filepath, "r") as f:
        return json.load(f)


def load_yaml_all(filename):
    """Load all documents from a multi-doc YAML file."""
    filepath = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(filepath, "r") as f:
        return list(yaml.safe_load_all(f))


def test_non_secret_yaml():
    """Test that non-Secret YAML files pass."""
    data = load_yaml_file("pass/configmap.yaml")
    assert check_secret(data, "test.yaml") is True


def test_encrypted_secret():
    """Test that SOPS-encrypted Secret files pass."""
    data = load_yaml_file("pass/encrypted-secret.yaml")
    assert check_secret(data, "test.yaml") is True


def test_unencrypted_secret():
    """Test that unencrypted Secret files fail."""
    data = load_yaml_file("fail/unencrypted-secret.yaml")
    assert check_secret(data, "test.yaml") is False


def test_unencrypted_stringdata():
    """Test that unencrypted Secret with stringData fails."""
    data = load_yaml_file("fail/unencrypted-stringdata.yaml")
    assert check_secret(data, "test.yaml") is False


def test_empty_secret():
    """Test that empty Secret data passes."""
    data = load_yaml_file("pass/empty-secret.yaml")
    assert check_secret(data, "test.yaml") is True


def test_malformed_sops():
    """Test that malformed SOPS metadata fails."""
    data = load_yaml_file("fail/malformed-sops.yaml")
    assert check_secret(data, "test.yaml") is False


def test_invalid_sops_metadata():
    """Test that invalid SOPS metadata is detected."""
    data = load_yaml_file("fail/invalid-sops.yaml")
    assert check_secret(data, "test.yaml") is False


def test_missing_sops_fields():
    """Test that missing required SOPS fields are detected."""
    data = load_yaml_file("fail/missing-sops-fields.yaml")
    assert check_secret(data, "test.yaml") is False


def test_non_dict_yaml():
    """Test that non-dict YAML content passes."""
    data = load_yaml_file("pass/non-dict.yaml")
    assert check_secret(data, "test.yaml") is True


def test_fake_encrypted():
    """Test that fake encrypted secrets fail."""
    data = load_yaml_file("fail/fake-encrypted.yaml")
    assert check_secret(data, "test.yaml") is False


def test_raw_json_secret():
    """Test that raw JSON files with unencrypted data fail."""
    data = load_json_file("fail/raw-json-secret.json")
    assert check_secret(data, "secret.json") is False


def test_raw_json_encrypted():
    """Test that raw JSON files with SOPS encryption pass."""
    data = load_json_file("pass/raw-json-encrypted.json")
    assert check_secret(data, "secret.json") is True


def test_ksops_generator():
    """Test that ksops secret generator configurations pass."""
    data = load_yaml_file("pass/ksops-generator.yaml")
    assert check_secret(data, "secret-generator.yaml") is True


def test_unencrypted_kustomize_secret():
    """Test that unencrypted kustomize secrets fail."""
    data = load_yaml_file("fail/unencrypted-kustomize-secret.yaml")
    assert check_secret(data, "test.yaml") is False


def test_kustomize_patch_secret():
    """Test that unencrypted secrets in kustomize patches fail."""
    data = load_yaml_file("fail/kustomize-patch-secret.yaml")
    assert check_secret(data, "test.yaml") is False


def test_kustomize_mixed_secrets():
    """Test that mixed encrypted/unencrypted files in secretGenerator fail."""
    data = load_yaml_file("fail/kustomize-mixed-secrets.yaml")
    assert check_secret(data, "test.yaml") is False


def test_non_dict_data():
    """Test that Secret with non-dict data fails."""
    data = load_yaml_file("fail/non-dict-data.yaml")
    assert check_secret(data, "test.yaml") is False


def test_multi_doc_yaml():
    """Test that multi-document YAML files are handled correctly."""
    docs = load_yaml_all("pass/multi-doc.yaml")
    for doc in docs:
        assert check_secret(doc, "test.yaml") is True


def test_nonexistent_file(monkeypatch, capsys):
    """Test handling of non-existent files."""
    monkeypatch.setattr(sys, "argv", ["script", "nonexistent.yaml"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error reading file" in captured.out


def test_malformed_yaml(monkeypatch, capsys):
    """Test that malformed YAML files are checked for secrets regardless of syntax."""
    monkeypatch.setattr(sys, "argv", ["script", "tests/fixtures/fail/malformed.yaml"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    # We don't care about malformed YAML, only secrets
    assert exc_info.value.code == 0
    # Debug output has been removed


def test_unencrypted_basic_auth():
    """Test that unencrypted basic auth secrets fail."""
    data = load_yaml_file("fail/secret-ignore.txt")
    assert check_secret(data, "test.yaml") is False


def test_template_with_tls_secret():
    """Test that unencrypted TLS certificate/key pairs in templates fail."""
    filepath = os.path.join(
        os.path.dirname(__file__), "fixtures/fail/secret-ignore.yaml.j2"
    )
    with open(filepath, "r") as f:
        content = f.read()
    assert check_template_content(content, filepath) is False


def test_template_with_basic_auth():
    """Test that unencrypted basic auth in templates fail."""
    filepath = os.path.join(
        os.path.dirname(__file__), "fixtures/fail/secret-ignore.txt"
    )
    with open(filepath, "r") as f:
        content = f.read()
    assert check_template_content(content, filepath) is False


def test_kustomize_output_log():
    """Test that kustomize build output in log files is detected."""
    docs = load_yaml_all("fail/kustomize-output.log")
    for doc in docs:
        assert check_secret(doc, "output.log") is False


def test_backup_secret_file():
    """Test that backup files containing secrets are detected."""
    data = load_yaml_file("fail/backup-secret.yaml.bak")
    assert check_secret(data, "secret.yaml.bak") is False


def test_debug_output_with_secrets():
    """Test that debug output files containing secrets are detected."""
    data = load_yaml_file("fail/debug-output.txt")
    assert check_secret(data, "debug.txt") is False


def test_main_with_non_yaml_files(monkeypatch, capsys):
    """Test handling of non-YAML/JSON files that might contain secrets."""
    monkeypatch.setattr(sys, "argv", ["script", "tests/fixtures/fail/debug-output.txt"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "unencrypted sensitive data" in captured.out.lower()


def test_mixed_content_with_secrets():
    """Test that secrets in mixed content files are detected."""
    filepath = os.path.join(
        os.path.dirname(__file__), "fixtures/fail/mixed-content.txt"
    )
    with open(filepath, "r") as f:
        content = f.read()
    docs = extract_yaml_documents(content)
    assert len(docs) > 0
    for doc in docs:
        if doc and doc.get("kind") == "Secret":
            assert check_secret(doc, filepath) is False

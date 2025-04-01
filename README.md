# sops-pre-commit

A pre-commit hook to prevent unencrypted Kubernetes secrets and kustomize secretGenerators from being committed.

## Features

- Detects unencrypted Kubernetes Secret resources
- Detects unencrypted kustomize secretGenerator configurations:
  - Literal values in secretGenerator
  - Unencrypted file references
  - Nested secretGenerator in patches
- Provides clear error messages with file locations
- Validates SOPS metadata structure

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/nicholasklem/sops-pre-commit
  rev: v2.2.7 # Use the ref you want to point at
  hooks:
    - id: forbid-secrets
```

## What it checks

1. Standard Kubernetes Secrets:

   - Ensures all Secret resources are encrypted with SOPS
   - Validates SOPS metadata structure
   - Checks for required SOPS fields (mac, lastmodified)

2. Kustomize Secrets:
   - Prevents unencrypted literals in secretGenerator
   - Requires encrypted files (_.enc.yaml or _.sops.yaml) in secretGenerator
   - Detects unencrypted secrets in nested patches

## Example Violations

```yaml
# Unencrypted literals in secretGenerator
secretGenerator:
- name: database-creds
  literals:  # Will fail
  - username=admin
  - password=secret123

# Unencrypted file references
secretGenerator:
- name: api-keys
  files:  # Will fail
  - api-key.txt  # Not encrypted
  - config.json  # Not encrypted

# Nested unencrypted secrets in patches
patches:
- patch: |-
    secretGenerator:
    - name: additional-secrets
      literals:  # Will fail
      - EXTRA_KEY=unsafevalue
```

## Valid Examples

```yaml
# Using encrypted files
secretGenerator:
  - name: valid-secrets
    files:
      - secrets.enc.yaml
      - config.sops.yaml

# Using KSOPS
generators:
  - ksops.yaml
```

## Requirements

- Python 3.6+
- PyYAML

## License

MIT License (see LICENSE file)

Test pre-commit hooks

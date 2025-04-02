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
- Supports ignoring specific lines or entire files with comments

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/nicholasklem/sops-pre-commit
  rev: v3.0.0 # Use the ref you want to point at
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

## Ignoring Files or Lines

You can tell the hook to ignore specific lines or entire files using special comments:

1. To ignore a specific line:

   ```yaml
   password: my-unencrypted-value # sops-pre-commit: ignore-line
   ```

2. To ignore an entire file, add this comment at the top (within first 3 lines):
   ```yaml
   # sops-pre-commit: ignore-file
   ```

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

## Development

To set up a development environment:

1. Clone the repository:

   ```bash
   git clone https://github.com/nicholasklem/sops-pre-commit.git
   cd sops-pre-commit
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in editable mode with development dependencies:

   ```bash
   pip install -e .
   pip install -r dev-requirements.txt
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

Run the test suite with coverage:

```bash
pytest
```

### Development Dependencies

The `dev-requirements.txt` file includes tools needed for development:

- `pre-commit`: For running pre-commit hooks locally
- `pytest` and `pytest-cov`: For running tests with coverage
- `coverage`: For detailed coverage reports

## Requirements

- Python 3.6+
- PyYAML

## License

MIT License (see LICENSE file)

Test pre-commit hooks

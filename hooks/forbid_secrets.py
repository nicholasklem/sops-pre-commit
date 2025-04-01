# Test pre-commit hooks
#!/usr/bin/env python3

import sys
import yaml

def check_secret(data, filename):
    """Check if a YAML/JSON document contains unencrypted sensitive data.

    This checks:
    1. Kubernetes Secret resources
    2. Raw JSON/YAML files with data/stringData fields that should be encrypted
    3. Secret generator configurations referencing secret files
    """
    if not isinstance(data, dict):
        return True

    # Check for secret generator configurations
    if data.get('kind') == 'ksops' and data.get('apiVersion', '').startswith('viaduct.ai/'):
        # For ksops generators, we don't need to encrypt the generator itself
        # The referenced files will be checked separately
        return True

    # For Kubernetes resources, only check Secrets
    if 'kind' in data:
        if data['kind'] != 'Secret':
            return True

    # For non-Kubernetes files, check if they contain sensitive data fields
    has_data = 'data' in data
    has_string_data = 'stringData' in data

    # Skip if no data fields present
    if not (has_data or has_string_data):
        # If this is a Secret with SOPS metadata, validate it even without data
        if data.get('kind') == 'Secret' and 'sops' in data:
            return validate_sops_metadata(data, filename)
        return True

    # Check if this is a SOPS encrypted file
    if 'sops' in data:
        return validate_sops_metadata(data, filename)

    # If not encrypted, check for non-empty data
    data_value = data.get('data')
    string_data_value = data.get('stringData')

    # For dict values, check if any values are non-empty
    if isinstance(data_value, dict):
        has_data = any(v for v in data_value.values() if v is not None and v != '')
    else:
        has_data = data_value is not None and data_value != ''

    if isinstance(string_data_value, dict):
        has_string_data = any(v for v in string_data_value.values() if v is not None and v != '')
    else:
        has_string_data = string_data_value is not None and string_data_value != ''

    if has_data or has_string_data:
        print(f"Unencrypted sensitive data found in {filename}")
        print("Please encrypt data using SOPS before committing")
        return False

    return True

def validate_sops_metadata(data, filename):
    """Validate that SOPS metadata is present and valid."""
    if not isinstance(data.get('sops'), dict):
        print(f"Invalid SOPS metadata structure in {filename}")
        return False

    sops_data = data['sops']
    if 'mac' not in sops_data or \
       'lastmodified' not in sops_data or \
       sops_data.get('mac') is None or \
       sops_data.get('lastmodified') is None:
        print(f"Missing or invalid required SOPS metadata fields in {filename}")
        return False

    return True

def main():
    """Main entry point."""
    exit_code = 0

    for filename in sys.argv[1:]:
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            exit_code = 1
            continue

        try:
            # Handle multi-document YAML files
            docs = list(yaml.safe_load_all(content))

            for doc in docs:
                if not check_secret(doc, filename):
                    exit_code = 1
                    break

        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {filename}: {e}")
            exit_code = 1
            continue
        except Exception as e:
            print(f"Unexpected error processing {filename}: {e}")
            exit_code = 1
            continue

    sys.exit(exit_code)

if __name__ == '__main__':
    main()

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-03-29

Initial release of the forked project.

### Breaking Changes

- Changed pre-commit hook to use types instead of file patterns for better file identification
- Added validation for encrypted files (SOPS and SealedSecrets)
- Modified core functionality of secret detection and validation

### Added

- Support for detecting encrypted SOPS files
- Support for detecting encrypted SealedSecrets
- Comprehensive test suite for encrypted file validation
- Improved error messages for unencrypted secrets

### Changed

- Improved configuration files and development setup
- Updated dependencies to latest versions
- Enhanced documentation with more examples

## Project History

This project was forked from [onedr0p/sops-pre-commit](https://github.com/onedr0p/sops-pre-commit) in March 2024. Version 3.0.0 represents a fresh start with significant improvements and new features while maintaining the core mission of preventing unencrypted secrets from being committed.

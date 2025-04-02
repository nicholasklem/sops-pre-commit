# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-04-01

### Added

- Extension-agnostic secret detection
- Support for detecting secrets in any text file
- Test cases for mixed content (logs + YAML)
- YAML extraction from debug output and logs
- Explicit PyYAML dependency to pre-commit hook configuration

### Changed

- Updated pre-commit hook to scan all text files
- Focus on secret detection rather than YAML validation
- Removed support for Python 3.7
- Added support for Python 3.11
- Updated dependencies
- Improved error handling and logging
- Added more test coverage
- Added more documentation
- Added more examples
- Added more CI/CD checks
- Added more security checks
- Added more code quality checks
- Added more code style checks

## Project History

This project was forked from [onedr0p/sops-pre-commit](https://github.com/onedr0p/sops-pre-commit) in March 2024. Version 3.0.0 represents a fresh start with significant improvements and new features while maintaining the core mission of preventing unencrypted secrets from being committed.

# Changelog

All notable changes to Claude Knowledge Catalyst (CKC) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.1] - 2025-06-19

### Added
- **🔒 CLAUDE.md Sync Feature**: Secure synchronization of CLAUDE.md files with section-level filtering
  - Configurable sync option (`include_claude_md`) - disabled by default for security
  - Section exclusion patterns (`claude_md_sections_exclude`) for filtering sensitive information
  - Case-insensitive section header matching (e.g., "# secrets", "# SECRETS", "# Secrets")
  - Enhanced metadata generation for CLAUDE.md files with project context analysis
  - Intelligent content analysis detecting project overviews, architecture info, commands, and guidelines
- **📚 Comprehensive Documentation**:
  - [User Guide: CLAUDE.md Sync](docs/user-guide/claude-md-sync.md) with security best practices
  - [Configuration Reference](docs/api-reference/configuration.md) with complete option details
  - Developer guide with implementation architecture and security considerations
  - Quick start examples and troubleshooting guides
- **🧪 Robust Testing**: Complete test suite with 9 test cases covering all functionality
  - Section filtering with case-insensitive matching
  - Empty file handling and validation
  - Metadata generation and content analysis
  - Security boundary testing

### Changed
- **⚙️ Enhanced Watch Configuration**: Extended `WatchConfig` with CLAUDE.md-specific options
- **🔍 Improved File Processing**: Enhanced file pattern matching to support CLAUDE.md detection
- **📊 Enriched Metadata System**: Added specialized metadata fields for CLAUDE.md files

### Security
- **🛡️ Security-First Design**: CLAUDE.md sync disabled by default to prevent accidental information exposure
- **🚫 Sensitive Content Protection**: Flexible section exclusion system to filter out:
  - API keys and credentials (`# secrets`, `# credentials`)
  - Personal information (`# private`, `# personal`)
  - Confidential project data (`# confidential`, `# internal`)
- **🔒 Safe Processing**: Non-destructive filtering that preserves original files

### Developer
- **🏗️ New Core Module**: `core.claude_md_processor.ClaudeMdProcessor` for specialized CLAUDE.md handling
- **🔧 Integration Points**: Seamless integration with existing file watcher and sync systems
- **⚡ Performance Optimized**: Efficient pattern matching with pre-compiled regular expressions
- **📋 Configuration Schema**: Pydantic-based validation for all new configuration options

## [0.9.0] - 2025-06-18

### Added
- **🏗️ Adaptive System Foundation**: 10-step numbering system (00→10→20→30) for knowledge maturity visualization
- **🧠 Intelligent Knowledge Management**: Automatic metadata extraction with project detection and tag inference
- **🎯 Deep Obsidian Integration**: Structured vault synchronization with PARA method organization
- **📊 Comprehensive Analytics**: Knowledge analytics with visualization and usage statistics
- **🤖 AI-Powered Features**: Content improvement suggestions and intelligent template generation
- **⚡ Enhanced CLI Interface**: Rich console output with colored formatting and progress indicators
- **🔄 Hybrid Structure System**: Flexible directory organization with backward compatibility
- **🛠️ Automation Tools**: Automated structure maintenance and metadata consistency checking

### Changed
- **📈 Performance Improvements**: 50% faster sync operations and 30% reduced memory usage
- **🔧 Configuration System**: Enhanced Pydantic-based configuration with automatic migration
- **📚 Documentation**: Complete overhaul with Read the Docs integration

### Fixed
- Metadata extraction for complex frontmatter
- File watching reliability improvements
- Sync issues with large file batches
- Cross-platform path handling

## [0.8.x] - Previous Versions

For changelog information about versions prior to 0.9.0, please refer to [RELEASE_NOTES.md](RELEASE_NOTES.md).

---

## Legend

- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes and security improvements

## Version Links

[Unreleased]: https://github.com/drillan/claude-knowledge-catalyst/compare/v0.9.1...HEAD
[0.9.1]: https://github.com/drillan/claude-knowledge-catalyst/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/drillan/claude-knowledge-catalyst/releases/tag/v0.9.0
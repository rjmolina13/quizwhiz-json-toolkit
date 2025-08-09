# Changelog

All notable changes to the **QuizWhiz JSON Toolkit** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.6.5] - 2025-08-09
### 🔧 Fixes
- **Build Process**: Updated GitHub Actions workflow to remove `--windowed` flag from PyInstaller command
- **CLI Support**: Ensured executables properly handle command-line arguments and console output
- **Cross-Platform**: Improved executable compatibility across Windows, macOS, and Linux platforms

### ⚡ Technical Improvements
- **PyInstaller Configuration**: Aligned CI/CD build process with local build script for consistency
- **Console Handling**: Automatic console window management - hidden for GUI mode, visible for CLI operations
- **Build Reliability**: Enhanced build process reliability by removing windowed mode restrictions

## [4.6] - 2025-08-09
### 🚀 Enhanced Features
- **Robust MHTML Extraction**: Implemented multi-strategy MHTML parsing to handle different file structures
- **Improved Compatibility**: Enhanced extraction logic now successfully processes MHTML files with non-standard HTML section layouts
- **Better Error Handling**: Added comprehensive fallback strategies for MHTML content extraction
- **Enhanced Logging**: Improved verbose output with detailed strategy information during extraction process

### ⚡ Technical Improvements
- **Multi-Strategy Parsing**: Added three-tier extraction approach (Original → Section Scoring → Main Content Area)
- **Google Forms Detection**: Enhanced pattern matching for Qr7Oae, M7eMe, and aDTYNe indicators
- **Boundary Analysis**: Improved MHTML boundary detection and section parsing
- **Backward Compatibility**: Maintained full compatibility with existing functionality while adding robust extraction

## [4.5] - 2025-08-09

### 🚀 Enhanced Features
- **NLP Difficulty Classification**: Significantly enhanced the difficulty analysis system with new patterns and keywords
- **Cognitive Indicators**: Added new recall and evaluation patterns for better question classification
- **Domain Complexity**: Expanded keyword dictionaries with General Education, Science, and Professional Education terms
- **Pattern Recognition**: Improved recognition of simple factual and comparative analysis question types
- **Educational Context**: Enhanced support for Philippine educational context and LET-specific terminology

### ⚡ Technical Improvements
- **Keyword Expansion**: Added 50+ new keywords across basic facts, scientific principles, and educational theory domains
- **Pattern Matching**: Enhanced regex patterns for better subject and session extraction
- **Classification Accuracy**: Improved NLP-based difficulty scoring with domain-specific indicators
- **Professional Education**: Enhanced recognition of assessment methods, reliability measures, and creative thinking patterns

## [4.4.5] - 2025-08-09

### 🔧 Fixes
- **Build Process**: Simplified build process by removing spec file dependency and compression settings
- **Compatibility**: Improved build reliability by using direct PyInstaller commands instead of spec files
- **Maintenance**: Streamlined build scripts for better maintainability and faster builds

### ⚡ Technical Improvements
- **Build Simplification**: Replaced spec file usage with direct PyInstaller command-line options
- **GitHub Actions**: Updated workflow to use direct PyInstaller commands for consistency
- **Local Builds**: Simplified `build_local.py` script by removing spec file manipulation
- **Documentation**: Updated README.md to reflect simplified build process

## [4.4] - 2025-08-09

### 🔧 Fixes
- **GitHub Actions**: Fixed build failures by updating `quiz_toolkit.spec` and improving `sed` command compatibility
- **Build Process**: Enhanced workflow with proper timeouts and platform-specific handling
- **Version Management**: Optimized version change detection and build triggering

### ⚡ Technical Improvements
- **CI/CD Pipeline**: Added pip caching and increased timeouts to prevent build cancellations
- **Cross-Platform**: Implemented platform-specific `sed` commands for macOS and other systems
- **Build Efficiency**: Added conditional builds that only run when version changes are detected
- **Error Handling**: Improved error detection and recovery in automated builds

## [4.3] - 2025-08-09

### 🔧 Fixes
- **Executable Size**: Optimized PyInstaller build process to reduce file size from ~9.9MB to ~9.7MB
- **Build Process**: Enhanced build configuration with custom spec file for better optimization

### ⚡ Technical Improvements
- **Size Optimization**: Added custom PyInstaller spec file with module exclusions and optimization flags
- **Build Efficiency**: Excluded unused modules (PIL, matplotlib, numpy, etc.) and enabled maximum optimization
- **Documentation**: Updated build instructions and added comprehensive size optimization guide

## [4.2] - 2025-08-09

### Fixed
- 🔧 **GitHub Actions Workflow**: Modified release and notify jobs to proceed without version change requirements
- 🚀 **CI/CD Pipeline**: Enhanced workflow flexibility for manual releases and re-releases
- ⚡ **Release Process**: Improved automated release creation with proper permissions

### Technical Improvements
- **Workflow Flexibility**: Removed version-change dependency for release and notify jobs
- **Release Automation**: Enhanced GitHub Actions to support releases regardless of version changes
- **Build Reliability**: Improved workflow execution with contents: write permissions

## [4.1] - 2025-08-09

### Fixed
- 🔧 **GitHub Actions Workflow**: Updated artifact actions from deprecated v3 to v4
- 🚀 **CI/CD Pipeline**: Resolved workflow failures due to deprecated actions/upload-artifact and actions/download-artifact
- ⚡ **Build Performance**: Improved upload/download speeds by up to 98% with v4 artifact actions

### Technical Improvements
- **Workflow Compatibility**: Updated build-release.yml to use latest GitHub Actions
- **Deprecation Resolution**: Eliminated deprecated v3 artifact actions before January 30th, 2025 deadline
- **Build Reliability**: Enhanced automated build process stability

## [4.0] - 2025-08-08

### Added
- 🌞 **Light Mode Command-Line Option**: New `--light-mode` argument to force GUI launch in light mode
- 🎛️ **Theme Override Control**: Enhanced theme system with manual override capabilities
- 🎨 **Enhanced Dark Mode Support**: Complete dark theme implementation with automatic Windows theme detection
- 🔧 **Improved Theme Refresh**: Enhanced theme switching mechanism with widget tree updates
- 📖 **Improved Help Documentation**: Updated help text with usage examples for new features
- 🖥️ **Cross-Platform Compatibility**: Improved support for Windows, macOS, and Linux
- 🎨 **Modern UI Elements**: Enhanced styling for Entry widgets, LabelFrames, and other components


### Enhanced
- **Command-Line Interface**: Extended argument parser with theme control options
- **GUI Initialization**: Enhanced constructor to accept theme preference parameters
- **GUI Interface**: Complete redesign with tabbed interface and modern styling
- **Theme Detection**: Improved theme setup method to respect forced light mode preference
- **User Experience**: Better control over application appearance regardless of system theme

### Technical Improvements
- **Code Modularity**: Enhanced separation between theme detection and theme application
- **Parameter Passing**: Improved argument flow from CLI to GUI components
- **Documentation**: Added inline examples and usage patterns for new features

## [3.5] - 2025-08-07

### Added
- 🎯 **Advanced Difficulty Analysis**: Enhanced NLP-based difficulty scoring using Bloom's Taxonomy
- 📚 **LET Pattern Recognition**: Specialized analysis for Licensure Examination for Teachers questions
- 🔄 **Smart Duplicate Detection**: Advanced fuzzy matching and semantic similarity analysis
- 📊 **Comprehensive Logging**: Detailed operation logs and error reporting

### Enhanced
- **MHTML Extraction**: Improved parsing accuracy for complex Google Forms layouts
- **JSON Merging**: Better conflict resolution and metadata preservation
- **Error Handling**: More robust error detection and user-friendly messages
- **Performance**: Optimized processing for large files and datasets

### Fixed
- 🐛 **Dark Mode Issues**: Resolved white appearance of Entry widgets and LabelFrame borders
- 🔧 **Theme Refresh**: Fixed theme application on startup and during runtime
- 📝 **Variable Scope**: Resolved UnboundLocalError for border_color variable
- 🎨 **Widget Styling**: Consistent styling across all UI components
- 🖱️ **Focus States**: Proper focus and selection colors for form elements

### Technical Improvements
- **Code Organization**: Better separation of concerns and modular design
- **Documentation**: Comprehensive inline documentation and type hints
- **Testing**: Enhanced error handling and validation
- **Build Process**: Automated executable generation with PyInstaller

## [3.4] - Previous Version

### Added
- Basic GUI interface with tkinter
- MHTML file extraction capabilities
- JSON file merging functionality
- Command-line interface support

### Features
- Google Forms MHTML parsing
- Quiz data extraction and formatting
- Multiple file format support
- Basic difficulty analysis

## [3.3] - Earlier Version

### Added
- Initial release of QuizWhiz JSON Toolkit
- Core extraction and merging functionality
- Basic command-line interface

---

## Release Notes Format

Each release includes:
- 🚀 **New Features**: Major additions and capabilities
- 🔧 **Improvements**: Enhancements to existing functionality
- 🐛 **Bug Fixes**: Resolved issues and problems
- 📚 **Documentation**: Updates to guides and documentation
- ⚡ **Performance**: Speed and efficiency improvements
- 🔒 **Security**: Security-related updates and fixes

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Contributing

When contributing, please:
1. Update this CHANGELOG.md with your changes
2. Follow the established format and categories
3. Include the date of the release
4. Use clear, descriptive language for changes

## Links

- [GitHub Repository](https://github.com/rjmolina13/quizwhiz-json-toolkit)
- [Latest Release](https://github.com/rjmolina13/quizwhiz-json-toolkit/releases/latest)
- [Issues](https://github.com/rjmolina13/quizwhiz-json-toolkit/issues)
- [Pull Requests](https://github.com/rjmolina13/quizwhiz-json-toolkit/pulls)
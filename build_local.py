#!/usr/bin/env python3
"""
Local Build Script for QuizWhiz JSON Toolkit

This script automates the local build process using direct PyInstaller commands
without compression for faster builds and better compatibility.

Features:
- Extracts version from quiz_toolkit.py
- Builds executable using direct PyInstaller commands (no spec file)
- Generates SHA256 checksums
- Cross-platform support (Windows, macOS, Linux)

Usage:
    python build_local.py

Author: RubyJ/@rjmolina13
"""

import os
import sys
import re
import subprocess
import hashlib
import platform
from pathlib import Path

def get_version_from_file():
    """Extract version from quiz_toolkit.py"""
    try:
        with open('quiz_toolkit.py', 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for VERSION = "x.x" pattern
            version_match = re.search(r'VERSION\s*=\s*["\']([0-9]+\.[0-9]+)["\']', content)
            if version_match:
                return version_match.group(1)
            else:
                print("⚠️  Warning: Could not find version in quiz_toolkit.py, using default 1.0")
                return "1.0"
    except FileNotFoundError:
        print("❌ Error: quiz_toolkit.py not found!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading quiz_toolkit.py: {e}")
        sys.exit(1)

def build_executable_name(version):
    """Generate version-specific executable name"""
    return f"QuizWhiz-Toolkit_v{version}"

def run_pyinstaller(version):
    """Run PyInstaller with direct command-line options"""
    try:
        print("🔨 Building executable with PyInstaller...")
        executable_name = build_executable_name(version)
        
        # PyInstaller command with direct options (no compression, no spec file)
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            f'--name={executable_name}',
            '--clean',
            'quiz_toolkit.py'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ PyInstaller build completed successfully!")
        if result.stdout:
            print("📋 Build output:")
            print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller build failed with exit code {e.returncode}")
        if e.stdout:
            print("📋 stdout:")
            print(e.stdout)
        if e.stderr:
            print("📋 stderr:")
            print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: PyInstaller not found! Please install it with: pip install pyinstaller")
        sys.exit(1)

def get_executable_path(version):
    """Get the path to the built executable based on platform"""
    system = platform.system().lower()
    base_name = f"QuizWhiz-Toolkit_v{version}"
    
    if system == 'windows':
        return Path('dist') / f"{base_name}.exe"
    else:
        return Path('dist') / base_name

def rename_executable(version):
    """Rename executable with platform suffix"""
    system = platform.system().lower()
    original_path = get_executable_path(version)
    
    if not original_path.exists():
        print(f"❌ Error: Built executable not found at {original_path}")
        return None
    
    # Determine platform suffix
    if system == 'windows':
        platform_suffix = 'Windows'
        new_name = f"QuizWhiz-Toolkit_v{version}_{platform_suffix}.exe"
    elif system == 'darwin':
        platform_suffix = 'macOS'
        new_name = f"QuizWhiz-Toolkit_v{version}_{platform_suffix}"
    else:
        platform_suffix = 'Linux'
        new_name = f"QuizWhiz-Toolkit_v{version}_{platform_suffix}"
    
    new_path = Path('dist') / new_name
    
    try:
        original_path.rename(new_path)
        print(f"✅ Renamed executable to {new_name}")
        return new_path
    except Exception as e:
        print(f"❌ Error renaming executable: {e}")
        return original_path

def generate_checksum(file_path):
    """Generate SHA256 checksum for the executable"""
    try:
        print(f"🔐 Generating SHA256 checksum for {file_path.name}...")
        
        # Calculate SHA256
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        checksum = sha256_hash.hexdigest()
        
        # Write checksum to file
        checksum_file = file_path.with_suffix(file_path.suffix + '.sha256')
        with open(checksum_file, 'w') as f:
            f.write(f"{checksum}  {file_path.name}\n")
        
        print(f"✅ Checksum saved to {checksum_file.name}")
        print(f"📋 SHA256: {checksum}")
        
    except Exception as e:
        print(f"❌ Error generating checksum: {e}")

def get_file_size(file_path):
    """Get human-readable file size"""
    size_bytes = file_path.stat().st_size
    
    # Convert to MB
    size_mb = size_bytes / (1024 * 1024)
    
    return f"{size_mb:.2f} MB ({size_bytes:,} bytes)"

def print_build_summary(executable_path, version):
    """Print build summary"""
    print("\n" + "="*60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"📦 Executable: {executable_path.name}")
    print(f"📍 Location: {executable_path.absolute()}")
    print(f"📏 Size: {get_file_size(executable_path)}")
    print(f"🏷️  Version: v{version}")
    print(f"💻 Platform: {platform.system()} {platform.machine()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("="*60)
    print("\n🚀 Your optimized executable is ready to use!")
    print(f"\n💡 To run: {executable_path.name}")
    if platform.system() != 'Windows':
        print(f"   (Make executable first: chmod +x {executable_path.name})")

def main():
    """Main build process"""
    print("🔧 QuizWhiz JSON Toolkit - Local Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('quiz_toolkit.py'):
        print("❌ Error: quiz_toolkit.py not found in current directory!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Step 1: Get version
    print("📋 Step 1: Extracting version...")
    version = get_version_from_file()
    print(f"✅ Found version: v{version}")
    
    # Step 2: Build with PyInstaller
    print("\n📋 Step 2: Building executable...")
    run_pyinstaller(version)
    
    # Step 3: Rename executable
    print("\n📋 Step 3: Renaming executable...")
    executable_path = rename_executable(version)
    
    if executable_path:
        # Step 4: Generate checksum
        print("\n📋 Step 4: Generating checksum...")
        generate_checksum(executable_path)
        
        # Step 5: Print summary
        print_build_summary(executable_path, version)
    else:
        print("❌ Build process failed!")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Build process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
"""
Script to install Rust on Windows, macOS, or Linux.
This is an alternative to using pre-compiled packages that require Rust.
"""
import os
import platform
import subprocess
import sys

def install_rust_windows():
    print("Downloading Rust installer for Windows...")
    # Download the rustup-init.exe installer
    subprocess.run(["curl", "-O", "https://win.rustup.rs/x86_64", "-o", "rustup-init.exe"], check=True)
    
    print("Running Rust installer...")
    # Run the installer
    subprocess.run(["rustup-init.exe", "-y"], check=True)
    
    print("Rust installation complete!")
    print("Please restart your terminal or run 'set PATH=%PATH%;%USERPROFILE%\\.cargo\\bin' to update your PATH.")

def install_rust_unix():
    print("Downloading and installing Rust...")
    # Download and run the rustup installer script
    subprocess.run(["curl", "--proto", "=https", "--tlsv1.2", "-sSf", "https://sh.rustup.rs", "|", "sh", "-s", "--", "-y"], shell=True, check=True)
    
    print("Rust installation complete!")
    print("Please restart your terminal or run 'source $HOME/.cargo/env' to update your PATH.")

def main():
    system = platform.system()
    
    print(f"Detected operating system: {system}")
    
    try:
        if system == "Windows":
            install_rust_windows()
        elif system in ["Darwin", "Linux"]:  # macOS or Linux
            install_rust_unix()
        else:
            print(f"Unsupported operating system: {system}")
            print("Please install Rust manually from https://rustup.rs/")
            sys.exit(1)
        
        print("\nAfter installing Rust, you can install the Python requirements with:")
        print("pip install -r backend/requirements.txt")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during Rust installation: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

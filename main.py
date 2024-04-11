import os
import argparse
from pathlib import Path

EXIT = 0
FAILURE = 1

def install_apt_package(package_name):
    os.system("sudo apt-get update")
    os.system(f"sudo apt-get install -y {package_name}")

def install_snap_package(package_name):
    os.system(f"sudo snap install {package_name} --classic")

def install_packages(apt_file, snap_file):
    succesfully_installed_packages = []
    unsuccesfully_installed_packages = []

    if apt_file is None and snap_file is None:
        print("No packages to install")
        return

    if apt_file is not None and apt_file.exists():
        print(f"Installing apt packages from {apt_file}")
        with open(apt_file, 'r') as f:
            os.system("sudo apt-get update")
            apt_packages = f.read().splitlines()
        for package in apt_packages:
            if install_apt_package(package) == EXIT:
                succesfully_installed_packages.append(package)
            else:
                unsuccesfully_installed_packages.append(package)

    if snap_file is not None and snap_file.exists():
        print(f"Installing snap packages from {snap_file}")
        with open(snap_file, 'r') as f:
            snap_packages = f.read().splitlines()
        for package in snap_packages:
            if install_snap_package(package) == EXIT:
                succesfully_installed_packages.append(package)
            else:
                unsuccesfully_installed_packages.append(package)

    print("Succesfully installed packages:")
    for package in succesfully_installed_packages:
        print("\033[1;32m" + package)

    print("Unsuccesfully installed packages:")
    for package in unsuccesfully_installed_packages:
        print("\033[91m" + package)

def main():
    parser = argparse.ArgumentParser(
        description="Install packages"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    install_parser = subparsers.add_parser(
        "install", help="Install packages"
    )

    install_parser.add_argument(
        "--apt",
        type=Path,
        help="File with list of apt packages to install",
    )

    install_parser.add_argument(
        "--snap",
        type=Path,
        help="File with list of snap packages to install",
    )

    args = parser.parse_args()

    if args.command == "install":
        install_packages(args.apt, args.snap)
    else:
        print("No command passed")

if __name__ == "__main__":
    main()
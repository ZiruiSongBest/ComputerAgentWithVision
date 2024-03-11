import platform
import subprocess
import re

def get_os_version():
    system = platform.system()

    if system == "Darwin":
        # macOS
        return 'macOS ' + platform.mac_ver()[0]

    elif system == "Linux":
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("PRETTY_NAME"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            pass
        return platform.version()

    elif system == "Windows":
        # Windows
        try:
            output = subprocess.check_output(["cmd.exe", "/c", "ver"]).decode("utf-8")
            version_line = output.strip().split("\n")[0]
            version_pattern = r"(\d+\.\d+\.\d+)"
            match = re.search(version_pattern, version_line)
            if match:
                return 'Windows ' + match.group(1)
            else:
                return "Unknown Windows Version"
        except Exception as e:
            print(f"Error retrieving Windows version: {e}")
            return "Unknown Windows Version"

    else:
        return "Unknown Operating System"

def check_os_version(s):
    if "mac" in s or "Ubuntu" in s or "CentOS" in s or 'Windows' in s:
        print("perating System Version:", s)
    else:
        raise ValueError("Unknown Operating System")


if __name__ == "__main__":
    os_version = get_os_version()
    print("Operating System Version:", os_version)
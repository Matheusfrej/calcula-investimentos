import subprocess
import shutil
import os
import re
import sys

class BuildExecutable:
    def __init__(self, name, bump_type) -> None:
        self.name = name
        self.bump_type = bump_type
        self.release_folder = "release"

    def install_dependencies(self):
        """Instala o PyInstaller se não estiver instalado"""
        try:
            subprocess.run(["pyinstaller", "--version"], check=True)
        except FileNotFoundError:
            print("PyInstaller não encontrado. Instalando...")
            subprocess.run(["pip", "install", "pyinstaller"], check=True)

    def clean_builds(self):
        """Remove pastas do PyInstaller"""
        for folder in ["build", "dist", f"{self.name}.spec", self.release_folder]:
            if os.path.exists(folder):
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
                else:
                    os.remove(folder)

    def create_executable(self):
        """Executa o PyInstaller para gerar o executável"""
        cmd = ["pyinstaller", "--onefile", f"--name={self.name}", "main.py"]
        subprocess.run(cmd, check=True)

    def move_executable(self):
        """Move o executável para a pasta 'release'"""
        exe_path = os.path.join("dist", f"{self.name}.exe")
        release_path = os.path.join(self.release_folder, f"{self.name}.exe")

        if not os.path.exists(self.release_folder):
            os.makedirs(self.release_folder)

        if os.path.exists(exe_path):
            shutil.move(exe_path, release_path)
            print(f"✅ Executável gerado com sucesso: {release_path}")
        else:
            print("❌ Erro ao gerar o executável!")

    def get_latest_version(self):
        """Gets the latest Git tag version or starts at 1.0.0 if no tags exist"""
        try:
            result = subprocess.run(["git", "tag"], capture_output=True, text=True, check=True)
            tags = result.stdout.strip().split("\n")
            if not tags or tags == ['']:  # No tags found
                return "1.0.0"

            latest_version = sorted(tags, key=lambda s: list(map(int, re.findall(r'\d+', s))))[-1]
            return latest_version
        except subprocess.CalledProcessError:
            return "1.0.0"

    def bump_version(self, version):
        """Bumps the version number based on 'major', 'minor', or 'patch'"""
        major, minor, patch = map(int, version.lstrip("v").split("."))

        if self.bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif self.bump_type == "minor":
            minor += 1
            patch = 0
        elif self.bump_type == "patch":
            patch += 1
        else:
            print("❌ Invalid version type! Use 'major', 'minor', or 'patch'.")
            sys.exit(1)

        return f"v{major}.{minor}.{patch}"

    def commit_and_push_executable(self, version):
        """Adds, commits, and pushes the new executable to GitHub"""
        try:
            subprocess.run(["git", "add", self.release_folder], check=True)
            subprocess.run(["git", "commit", "-m", f"🚀 Release {version}: Add new executable"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"✅ Successfully committed and pushed new executable for {version}")
        except subprocess.CalledProcessError:
            print("❌ Error committing and pushing the new executable!")

    def create_git_tag(self, version):
        """Creates a git tag and pushes it to GitHub"""
        try:
            subprocess.run(["git", "tag", version, "-m", f"Release {version}"], check=True)
            subprocess.run(["git", "push", "origin", version], check=True)
            print(f"✅ Successfully created and pushed tag {version}")
        except subprocess.CalledProcessError:
            print("❌ Error creating git tag. Make sure your repository is set up correctly.")

    def execute_pipeline(self):
        self.install_dependencies()
        self.clean_builds()
        self.create_executable()
        self.move_executable()

        current_version = self.get_latest_version()
        new_version = self.bump_version(current_version)

        self.commit_and_push_executable(new_version)  # ✅ Commit before tagging
        self.create_git_tag(new_version)  # ✅ Tag and push

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build.py [major|minor|patch]")
        sys.exit(1)

    bump_type = sys.argv[1]
    exe = BuildExecutable('CalculaInvestimentos', bump_type)
    exe.execute_pipeline()

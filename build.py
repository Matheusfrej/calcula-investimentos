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
        self.version = None  # Versão será definida antes da criação do executável

    def log_step(self, message):
        print(f"\n🔹 {message}...")

    def install_dependencies(self):
        self.log_step("Installing dependencies")
        try:
            subprocess.run(["pyinstaller", "--version"], check=True)
        except FileNotFoundError:
            print("⚠️ PyInstaller not found. Installing...")
            subprocess.run(["pip", "install", "pyinstaller"], check=True)

    def clean_builds(self, stage):
        self.log_step(f"Cleaning build files ({stage})")
        
        # Determine the correct .spec filename
        spec_pattern = f"{self.name}_v*.exe.spec"  # Matches versioned .spec files
        spec_files = [f for f in os.listdir() if re.match(spec_pattern.replace("*", r"\d+\.\d+\.\d+"), f)]

        if (self.version == "test"): spec_files = [f"{self.name}_test.exe.spec"]
        
        folders = ["build", "dist", self.release_folder] if stage == "before" else ["build", "dist"]

        # Remove directories
        for folder in folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)

        # Remove matching .spec files
        for spec_file in spec_files:
            os.remove(spec_file)

    def get_latest_version(self):
        self.log_step("Checking latest version")
        try:
            result = subprocess.run(["git", "tag"], capture_output=True, text=True, check=True)
            tags = result.stdout.strip().split("\n")
            if not tags or tags == ['']:
                return "v1.0.0"
            latest_version = sorted(tags, key=lambda s: list(map(int, re.findall(r'\d+', s))))[-1]
            print(f"🔖 Latest version: {latest_version}")
            return latest_version
        except subprocess.CalledProcessError:
            return "v1.0.0"

    def bump_version(self, version):
        self.log_step("Bumping version")
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

        new_version = f"v{major}.{minor}.{patch}"
        print(f"🔹 New version: {new_version}")
        return new_version

    def create_executable(self):
        self.log_step("Creating executable")
        exe_name = f"{self.name}_{self.version}.exe"
        cmd = ["pyinstaller", "--onefile", f"--name={exe_name}", "main.py"]
        subprocess.run(cmd, check=True)

    def move_executable(self):
        self.log_step("Moving executable to release folder")
        exe_name = f"{self.name}_{self.version}.exe"
        exe_path = os.path.join("dist", exe_name)
        release_path = os.path.join(self.release_folder, exe_name)

        if not os.path.exists(self.release_folder):
            os.makedirs(self.release_folder)

        if os.path.exists(exe_path):
            shutil.move(exe_path, release_path)
            print(f"✅ Executável gerado com sucesso: {release_path}")
        else:
            print("❌ Erro ao gerar o executável!")

    def commit_and_push_executable(self):
        self.log_step("Committing and pushing executable")
        try:
            subprocess.run(["git", "add", self.release_folder], check=True)
            subprocess.run(["git", "commit", "-m", f"🚀 Release {self.version}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"✅ Successfully committed and pushed new executable for {self.version}")
        except subprocess.CalledProcessError:
            print("❌ Error committing and pushing the new executable!")

    def create_git_tag(self):
        self.log_step(f"Creating and pushing tag {self.version}")
        try:
            subprocess.run(["git", "tag", self.version, "-m", f"Release {self.version}"], check=True)
            subprocess.run(["git", "push", "origin", self.version], check=True)
            print(f"✅ Successfully created and pushed tag {self.version}")
        except subprocess.CalledProcessError:
            print("❌ Error creating git tag. Make sure your repository is set up correctly.")

    def execute_pipeline(self):
        print("\n🚀 Starting build pipeline...")
        self.install_dependencies()
        self.clean_builds("before")

        if self.bump_type != "test":
            current_version = self.get_latest_version()
            self.version = self.bump_version(current_version)
        else:
            self.version = "test"

        self.create_executable()
        self.move_executable()
        self.clean_builds("after")

        if self.bump_type != "test":
            self.commit_and_push_executable()
            self.create_git_tag()

        print("\n✅ Build pipeline completed!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build.py [major|minor|patch|test]")
        sys.exit(1)

    bump_type = sys.argv[1]
    exe = BuildExecutable('CalculaInvestimentos', bump_type)
    exe.execute_pipeline()

import os

class ProjectInitTool:
    """
    Project Initialization Tool
    Follows gemini.md guidelines:
    - CamelCase naming
    - Static class structure
    - Strict directory hierarchy
    """

    @staticmethod
    def run():
        ProjectInitTool.createDirectories()
        ProjectInitTool.createPackages()
        ProjectInitTool.createConfigFiles()
        print("Project initialization complete.")

    @staticmethod
    def createDirectories():
        # Define directory structure based on gemini.md
        dirs = [
            "app/bin",
            "app/code/core",
            "app/code/dao",
            "app/code/utils",
            "app/code/tests",
            "app/config",
            "app/logs/archive",
            "app/data/tempAudio",
            "app/out"
        ]

        for dirPath in dirs:
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
                print(f"[Created Dir] {dirPath}")
            else:
                print(f"[Exists] {dirPath}")

    @staticmethod
    def createPackages():
        # Create __init__.py to make directories Python packages
        packageDirs = [
            "app/code",
            "app/code/core",
            "app/code/dao",
            "app/code/utils",
            "app/code/tests"
        ]

        for packageDir in packageDirs:
            filePath = os.path.join(packageDir, "__init__.py")
            ProjectInitTool.touchFile(filePath)

    @staticmethod
    def createConfigFiles():
        # Create empty config files
        configFiles = [
            "app/config/appDev.yaml",
            "app/config/appProd.yaml",
            "app/config/models.yaml" # Included for completeness per MD
        ]

        for configPath in configFiles:
            ProjectInitTool.touchFile(configPath)

    @staticmethod
    def touchFile(filePath):
        if not os.path.exists(filePath):
            # Ensure parent dir exists just in case
            parentDir = os.path.dirname(filePath)
            if not os.path.exists(parentDir):
                os.makedirs(parentDir)
            
            with open(filePath, 'w', encoding='utf-8') as f:
                pass
            print(f"[Created File] {filePath}")
        else:
            print(f"[Exists] {filePath}")

if __name__ == "__main__":
    ProjectInitTool.run()

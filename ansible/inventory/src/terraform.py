import json
import subprocess
from pathlib import Path


class TerraformOutputRetriever:
    """Class to catch and store Terraform output."""

    COMMAND = ["terraform", "output", "-json"]

    def __init__(self, folder: Path):
        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError(f"Terraform directory not found: {folder}")

        self.folder = folder

    def run(self) -> dict:
        result = subprocess.run(
            self.COMMAND, cwd=self.folder, capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)

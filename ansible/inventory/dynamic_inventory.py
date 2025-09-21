#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
import argparse

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TERRAFORM_DIR = BASE_DIR / "infra"


def get_terraform_output(folder: Path) -> dict:
    """Run `terraform output -json` and return the parsed JSON output."""

    assert (
        folder.exists() and folder.is_dir()
    ), f"Terraform directory not found: {folder}"
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=folder,
        capture_output=True,
        text=True,
        check=True,
    )
    parsed_output = json.loads(result.stdout)
    for key in ("vm_dev_name", "vm_dev_address"):
        assert key in parsed_output, f"Missing key in Terraform output: {key}"

    return parsed_output


def build_inventory(dev_ip: str, prod_ip: str) -> dict:
    """Build the Ansible inventory structure from Terraform output."""

    return {
        "_meta": {
            "hostvars": {
                "vm-dev": {
                    "ansible_host": dev_ip,
                    "ansible_user": "ubuntu",
                    "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
                    "ansible_python_interpreter": "/usr/bin/python3",
                },
                "vm-prod": {
                    "ansible_host": prod_ip,
                    "ansible_user": "ubuntu",
                    "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
                    "ansible_python_interpreter": "/usr/bin/python3",
                },
            }
        },
        "dev": {"hosts": ["vm-dev"]},
        "prod": {"hosts": ["vm-prod"]},
        "all": {
            "children": ["dev", "prod"],
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate Ansible dynamic inventory from Terraform output"
    )
    parser.add_argument("--list", action="store_true", help="List all hosts")
    parser.add_argument("--host", type=str, help="Get variables for a specific host")

    args = parser.parse_args()
    if not (args.list or args.host):
        parser.print_help()
        raise SystemExit(1)

    tf_output = get_terraform_output(TERRAFORM_DIR)
    inventory = build_inventory(
        dev_ip=tf_output["vm_dev_address"]["value"],
        prod_ip=tf_output["vm_prod_address"]["value"],
    )

    if args.list:
        print(json.dumps(inventory, indent=2))
        return

    if args.host:
        host = args.host
        host_vars = inventory["_meta"]["hostvars"].get(host)
        if host_vars:
            print(json.dumps(host_vars, indent=2))
            return
        print("{}")  # Host not found


if __name__ == "__main__":
    main()

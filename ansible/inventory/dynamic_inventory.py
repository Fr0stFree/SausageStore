#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
import argparse
from typing import NamedTuple


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TERRAFORM_DIR = BASE_DIR / "infra"


class VMConfig(NamedTuple):
    """Configuration for a virtual machine."""

    address: str
    key_file: str
    user: str


def get_terraform_output() -> dict:
    """Run `terraform output -json` and return the parsed JSON output."""

    assert (
        TERRAFORM_DIR.exists() and TERRAFORM_DIR.is_dir()
    ), f"Terraform directory not found: {TERRAFORM_DIR}"
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    parsed_output = json.loads(result.stdout)
    for key in ("vm_dev_name", "vm_dev_address", "vm_prod_name", "vm_prod_address"):
        assert key in parsed_output, f"Missing key in Terraform output: {key}"

    return parsed_output


def build_inventory(dev: VMConfig, prod: VMConfig) -> dict:
    """Build the Ansible inventory structure from Terraform output."""

    return {
        "_meta": {
            "hostvars": {
                "vm-dev": {
                    "ansible_host": dev.address,
                    "ansible_user": dev.user,
                    "ansible_ssh_private_key_file": dev.key_file,
                    "ansible_python_interpreter": "/usr/bin/python3"
                },
                "vm-prod": {
                    "ansible_host": prod.address,
                    "ansible_user": prod.user,
                    "ansible_ssh_private_key_file": prod.key_file,
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


def new_argument_parser() -> argparse.ArgumentParser:
    """Create and return a new argument parser."""

    parser = argparse.ArgumentParser(
        description="Generate Ansible dynamic inventory from Terraform output"
    )
    parser.add_argument("--list", action="store_true", help="List all hosts")
    parser.add_argument("--host", type=str, help="Get variables for a specific host")
    parser.add_argument(
        "--key-file",
        type=str,
        default="~/.ssh/id_rsa",
        help="Path to the SSH private key file",
    )
    parser.add_argument(
        "--user",
        type=str,
        default="ubuntu",
        help="SSH user for the virtual machines",
    )
    return parser


def main():
    parser = new_argument_parser()
    args = parser.parse_args()
    if not (args.list or args.host):
        parser.print_help()
        raise SystemExit(1)

    tf_output = get_terraform_output()
    dev_vm = VMConfig(
        address=tf_output["vm_dev_address"]["value"],
        key_file=args.key_file,
        user=args.user,
    )
    prod_vm = VMConfig(
        address=tf_output["vm_prod_address"]["value"],
        key_file=args.key_file,
        user=args.user,
    )

    inventory = build_inventory(dev_vm, prod_vm)

    if args.list:
        print(json.dumps(inventory, indent=2))
        return

    if args.host:
        host = args.host
        host_vars = inventory["_meta"]["hostvars"].get(host)
        if not host_vars:
            print("{}")  # Host not found
            return

        print(json.dumps(host_vars, indent=2)) 


if __name__ == "__main__":
    main()

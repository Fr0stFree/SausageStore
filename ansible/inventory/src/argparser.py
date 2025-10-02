from argparse import ArgumentParser
from typing import NamedTuple, Optional


class InventoryArgs(NamedTuple):
    list: bool
    host: Optional[str]


class AnsibleArgumentParser:
    """Class to parse command line arguments for Ansible dynamic inventory script."""
    def __init__(self) -> None:
        self.parser = ArgumentParser(
            description="Generate Ansible dynamic inventory from Terraform output"
        )
        self.parser.add_argument("--list", action="store_true", help="List all hosts")
        self.parser.add_argument(
            "--host", type=str, help="Get variables for a specific host"
        )

    def parse(self) -> InventoryArgs:
        args = self.parser.parse_args()
        if not (args.list or args.host):
            self.parser.print_help()
            raise SystemExit(1)

        return InventoryArgs(list=args.list, host=args.host)

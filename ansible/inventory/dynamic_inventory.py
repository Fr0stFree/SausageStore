#!/usr/bin/env python3
from pathlib import Path

from src.renderer import AnsibleInventoryBuilder, InventoryInfo, VMInfo, EnvInfo
from src.argparser import AnsibleArgumentParser
from src.terraform import TerraformOutputRetriever


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ANSIBLE_DIR = BASE_DIR / "ansible"
TERRAFORM_DIR = BASE_DIR / "infra"
TEMPLATES_DIR = ANSIBLE_DIR / "inventory" / "templates"
ANSIBLE_INVENTORY_TEMPLATE_FILE = TEMPLATES_DIR / "inventory.json.j2"
VM_USER = "ubuntu"


def make_inventory_info(tf_output: dict) -> InventoryInfo:
    return InventoryInfo(
        dev=EnvInfo(
            vm=VMInfo(
                ip=tf_output["vm_dev_address"]["value"],
                user=tf_output["vm_dev_user"]["value"],
            )
        ),
        prod=EnvInfo(
            vm=VMInfo(
                ip=tf_output["vm_prod_address"]["value"],
                user=tf_output["vm_prod_user"]["value"],
            )
        ),
    )


def main():
    parser = AnsibleArgumentParser()
    args = parser.parse()

    retriever = TerraformOutputRetriever(folder=TERRAFORM_DIR)
    output = retriever.run()

    info = make_inventory_info(output)
    builder = AnsibleInventoryBuilder(
        template_dir=TEMPLATES_DIR, template_name=ANSIBLE_INVENTORY_TEMPLATE_FILE.name
    )
    renderer = builder.build(info)

    if args.list:
        renderer.list()
        return

    if args.host:
        renderer.host(args.host)
        return


if __name__ == "__main__":
    main()

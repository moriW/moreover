#! /usr/bin/env python
# MOREOVER
# cli entry
#
# @file: cli
# @time: 2022/01/28
# @author: Mori
#

import click


@click.group()
def cli():
    ...


@cli.command("init")
@click.argument("project_name")
def init_project(project_name: str):
    import os
    import jinja2
    import datetime
    from moreover import MODULE_PATH

    header_template = """#! /usr/bin/env python
# {{ PROJECT_NAME }}
# {{ content }}
#
# @file: web
# @time: {{year}}/{{month}}/{{day}}
# @author: Mori
#"""
    header_template = jinja2.Template(header_template)

    if os.path.exists(project_name):
        raise ValueError(f"{project_name} already exists")

    now = datetime.datetime.now()
    os.mkdir(project_name)
    os.mkdir(os.path.join(project_name, "orm"))
    os.mkdir(os.path.join(project_name, "view"))
    os.mkdir(os.path.join(project_name, "service"))
    os.mkdir(os.path.join(project_name, "migration"))
    os.mkdir(os.path.join(project_name, "utils"))

    with open(os.path.join(project_name, "orm", "__init__.py"), "w") as _f:
        _f.write(
            header_template.render(
                PROJECT_NAME=project_name,
                content="orm entry",
                year=now.year,
                month=now.month,
                day=now.day,
            )
        )

    with open(os.path.join(project_name, "utils", "__init__.py"), "w") as _f:
        _f.write(
            header_template.render(
                PROJECT_NAME=project_name,
                content="utils entry",
                year=now.year,
                month=now.month,
                day=now.day,
            )
        )

    with open(os.path.join(project_name, "view", "__init__.py"), "w") as _f:
        _f.write(
            header_template.render(
                PROJECT_NAME=project_name,
                content="view entry",
                year=now.year,
                month=now.month,
                day=now.day,
            )
        )

    with open(os.path.join(project_name, "service", "__init__.py"), "w") as _f:
        _f.write(
            header_template.render(
                PROJECT_NAME=project_name,
                content="service entry",
                year=now.year,
                month=now.month,
                day=now.day,
            )
        )

    with open(os.path.join(project_name, "migration", "__init__.py"), "w") as _f:
        _f.write(
            header_template.render(
                PROJECT_NAME=project_name,
                content="service entry",
                year=now.year,
                month=now.month,
                day=now.day,
            )
        )

    with open(os.path.join(MODULE_PATH, "template", "app.py.j2"), "r") as _f1, open(
        os.path.join(project_name, "app.py"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(
            template.render(
                year=now.year,
                month=now.month,
                day=now.day,
                PROJECT_NAME=project_name,
            )
        )

    with open(
        os.path.join(MODULE_PATH, "template", "requirements.txt.j2"), "r"
    ) as _f1, open(os.path.join(project_name, "requirements.txt"), "w") as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render())

    with open(os.path.join(MODULE_PATH, "template", "gitignore.j2"), "r") as _f1, open(
        os.path.join(project_name, ".gitignore"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render())

    with open(
        os.path.join(MODULE_PATH, "template", "config.json.j2"), "r"
    ) as _f1, open(os.path.join(project_name, "config.json"), "w") as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render())

    with open(os.path.join(MODULE_PATH, "template", "Dockerfile.j2"), "r") as _f1, open(
        os.path.join(project_name, "Dockerfile"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render())

    with open(
        os.path.join(MODULE_PATH, "template", "dockerignore.j2"), "r"
    ) as _f1, open(os.path.join(project_name, ".dockerignore"), "w") as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render())

    with open(os.path.join(MODULE_PATH, "template", "build.sh.j2"), "r") as _f1, open(
        os.path.join(project_name, "build.sh"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(template.render(PROJECT_NAME=project_name))

    with open(os.path.join(MODULE_PATH, "template", "router.py.j2"), "r") as _f1, open(
        os.path.join(project_name, "view", "router.py"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(
            template.render(
                year=now.year,
                month=now.month,
                day=now.day,
                PROJECT_NAME=project_name,
            )
        )

    with open(os.path.join(MODULE_PATH, "template", "env.py.j2"), "r") as _f1, open(
        os.path.join(project_name, "utils", "env.py"), "w"
    ) as _f2:
        template = jinja2.Template(_f1.read())
        _f2.write(
            template.render(
                year=now.year,
                month=now.month,
                day=now.day,
                PROJECT_NAME=project_name,
            )
        )


@cli.command("dump_config")
@click.argument("config_file", default="config.json")
def dump_config(config_file: str):
    import os
    import json
    import pkgutil
    import importlib
    from moreover.base.config import global_config

    print(os.getcwd())
    for _, name, _ in pkgutil.walk_packages([os.getcwd()]):
        importlib.import_module(name)
    with open(config_file, "w") as _f:
        _f.write(json.dumps(global_config, indent=4))


def main():
    cli()

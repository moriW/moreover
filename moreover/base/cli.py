#! /usr/bin/env python
# MOREOVER
# cli entry
#
# @file: cli
# @time: 2022/01/28
# @author: Mori
#

import click

from moreover import MODULE_PATH


@click.group()
def cli():
    ...


@cli.command("init")
@click.option("--project_name", type=str)
def init_project(project_name: str):
    import os
    import jinja2
    import datetime

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


cli()

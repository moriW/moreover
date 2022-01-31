#! /usr/bin/env python
# MOREOVER
# cli entry
#
# @file: cli
# @time: 2022/01/28
# @author: Mori
#


import click


@click.command()
@click.option("--name", type=str, case_sensitive=False)
def init_project(project_name: str):
    import os
    import jinja2
    import datetime

    files = [
        "web.py.j2",
    ]

    if os.path.exists(project_name):
        raise click.BadArgumentUsage(
            f"project_name {project_name} exists in current path"
        )

    now = datetime.datetime.now()
    os.mkdir(project_name)
    for file in files:
        with open(os.path.join("template", file), "r") as _f:
            template = jinja2.Template(source=_f.read())
            with open(os.path.join(project_name, file.replace(".j2", "")), "w") as _f2:
                _f2.write(
                    template.render(
                        {
                            "year": now.year,
                            "month": now.month,
                            "day": now.day,
                            "PROJECT_NAME": project_name,
                        }
                    )
                )

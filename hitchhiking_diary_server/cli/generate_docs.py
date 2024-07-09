import json

import click
from fastapi.openapi.utils import get_openapi

from hitchhiking_diary_server.core import settings
from hitchhiking_diary_server.main import app


@click.command()
@click.option("--output", help="Output filename", default="openapi.json")
def openapi(output):
    with open(output, "w") as f:
        json.dump(
            get_openapi(
                title=settings.NAME,
                version=settings.VERSION,
                description=settings.DESCRIPTION,
                routes=app.routes,
            ),
            f,
        )

#!/usr/bin/env python

import logging

import alembic.command
import alembic.config
import uvicorn

from settings import settings

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)


def migrate():
    cfg = alembic.config.Config("alembic.ini")
    alembic.command.upgrade(cfg, "head")


def start_server():
    options = {}
    if settings.debug:
        options["reload"] = True
        options["log_level"] = "debug"
        options["debug"] = True
    else:
        options["log_level"] = "info"

    uvicorn.run("some_stuff:app", host="0.0.0.0", **options)


def main():
    migrate()
    start_server()


if __name__ == '__main__':
    main()

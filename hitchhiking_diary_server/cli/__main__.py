import click

from hitchhiking_diary_server.cli import create_user


@click.group()
def cli():
    pass


cli.add_command(create_user.create_user, name="create-user")

if __name__ == "__main__":
    cli()

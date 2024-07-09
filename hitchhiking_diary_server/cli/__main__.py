import click

from hitchhiking_diary_server.cli import create_user, generate_docs


@click.group()
def cli():
    pass


cli.add_command(create_user.create_user, name="create-user")
cli.add_command(generate_docs.openapi, name="openapi")

if __name__ == "__main__":
    cli()

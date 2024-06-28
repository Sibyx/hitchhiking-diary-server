import click
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from hitchhiking_diary_server.db.session import SessionLocal
from hitchhiking_diary_server.models import User


@click.command()
@click.option("--username", prompt="Username", help="The username for the new user")
@click.option(
    "--password", prompt="Password", hide_input=True, confirmation_prompt=True, help="The password for the new user"
)
def create_user(username: str, password: str):
    db: Session = SessionLocal()
    hasher: PasswordHasher = PasswordHasher()

    user = User(username=username, password=hasher.hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    click.echo(f"User {username} created successfully!")
    db.close()

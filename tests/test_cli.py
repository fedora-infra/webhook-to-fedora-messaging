import asyncio

from click.testing import CliRunner

from webhook_to_fedora_messaging import cli, database, models


def test_cli_create(db_session):
    """
    Creating a service using CLI
    """
    runner = CliRunner()
    result = runner.invoke(
        cli.create,
        ["--type", "github", "--service", "dummy/service", "--owner", "dummy-user"],
    )
    assert result.exit_code == 0

    async def _check():
        user, is_created = await database.get_or_create(db_session, models.User, name="dummy-user")
        assert is_created is False
        service, is_created = await database.get_or_create(
            db_session, models.Service, name="dummy/service"
        )
        assert is_created is False
        users = await service.awaitable_attrs.users
        assert len(users) == 1
        assert users[0].id == user.id

    asyncio.run(_check())

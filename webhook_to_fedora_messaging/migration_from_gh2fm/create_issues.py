import asyncio
import logging

import click
import gidgethub
import gidgethub.abc
import gidgethub.httpx
import httpx
from sqlalchemy import select

from ..config import set_config_file
from . import gh2fm


DESC_PREFIX = "Migrated from GitHub2FedMsg."
ISSUE_TITLE = "Migration Requested from Github2Fedmsg to Webhook To Fedora Messaging"
ISSUE_BODY = """
Your project was listed in the Github2Fedmsg database and we reach out to you to inform you about
the upcoming deprecation of the service. As the Fedora Infrastructure is finishing up with
migrating its applications away from Fedmsg to Fedora Messaging, we encourage you to migrate your
repository to the successor of the Github2Fedmsg project, Webhook To Fedora Messaging.

Please read [this official announcement](https://communityblog.fedoraproject.org/?p=14044) of the
project's release and use the instructions there to migrate to the new service.
If this notification was a mistake, please close this ticket. We will not act on the repositories
for which no migration has been requested and any related Github2Fedmsg operations will stop
working once the service is decommissioned.
"""

log = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True, readable=True),
    help="Path to the configuration file",
)
@click.option(
    "-u",
    "--github-username",
    envvar="GITHUB_USERNAME",
    required=True,
    help="The Github username that will be opening the issues",
)
@click.option(
    "-t",
    "--github-token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="The Github API token",
)
@click.option(
    "-g",
    "--github2fedmsg-db-url",
    envvar="GITHUB2FEDMSG_DB_URL",
    required=True,
    help="The URL to Github2Fedmsg's DB",
)
@click.option("-d", "--debug", is_flag=True, help="Show more information")
def main(config_path, github_username, github_token, github2fedmsg_db_url, debug):
    if config_path:
        set_config_file(config_path)
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )
    logging.getLogger("httpx").setLevel(logging.INFO if debug else logging.WARNING)
    asyncio.run(_main(github_username, github_token, github2fedmsg_db_url))


async def _main(github_username, github_token, github2fedmsg_db_url):
    async with httpx.AsyncClient() as http_client:
        gh = gidgethub.httpx.GitHubAPI(http_client, github_username, oauth_token=github_token)
        async with gh2fm.get_session(github2fedmsg_db_url) as gh2fm_session:
            query = (
                select(gh2fm.users.c.github_username, gh2fm.repos.c.name)
                .join_from(gh2fm.repos, gh2fm.users)
                .where(gh2fm.repos.c.enabled.is_(True))
            )
            result = await gh2fm_session.execute(query)
            for user, repo in result.fetchall():
                await process_repo(f"{user}/{repo}", gh)


async def process_repo(repo, gh: gidgethub.abc.GitHubAPI):
    log.debug("Processing %s", repo)
    # Make sure the repo exists:
    try:
        await gh.getitem(f"/repos/{repo}")
    except gidgethub.BadRequest as e:
        if e.status_code == 404:
            log.info("Repo %s not found, skipping", repo)
            return
        print(e, e.__dict__)
        raise
    except gidgethub.RedirectionException:
        # Get the new name
        request_headers = gidgethub.sansio.create_headers(
            gh.requester, accept=gidgethub.sansio.accept_format(), oauth_token=gh.oauth_token
        )
        status_code, headers, content = await gh._request(
            "GET",
            gidgethub.sansio.format_url(f"/repos/{repo}", None, base_url=gh.base_url),
            request_headers,
        )
        new_repo = await gh.getitem(headers["location"])
        repo = new_repo["full_name"]
        log.info("The repo has been moved to %s", repo)
    issues_url = f"/repos/{repo}/issues"
    issues = gh.getiter(issues_url, dict(state="all", creator=gh.requester))
    async for issue in issues:
        if issue["title"] == ISSUE_TITLE:
            return  # The issue already exists in this repo
    log.info("Creating issue in %s", repo)
    new_issue = await gh.post(issues_url, data={"title": ISSUE_TITLE, "body": ISSUE_BODY})
    log.debug("Created issue %s in %s (%s)", new_issue["number"], repo, new_issue["html_url"])


if __name__ == "__main__":
    main()

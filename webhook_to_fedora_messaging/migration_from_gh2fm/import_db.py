import csv
from asyncio import run
from datetime import datetime
from uuid import uuid4

import click
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from ..config import get_config
from ..database import get_session
from ..models import Service, User
from ..models.owners import owners_table


format = "%d-%m-%Y %H:%M:%S"


def read_user(userscsv_fileloca):
    with open(userscsv_fileloca) as file:
        useriter = csv.reader(file)
        next(useriter)
        for item in useriter:
            yield item[0]


def read_repo(reposcsv_fileloca):
    with open(reposcsv_fileloca) as file:
        repoiter = csv.reader(file)
        next(repoiter)
        for item in repoiter:
            yield item[1], item[2], item[4], item[5]


def read_pair(userscsv_fileloca, pairscsv_fileloca):
    pair, userdict = dict(), dict()
    with open(userscsv_fileloca) as file:
        useriter = csv.reader(file)
        next(useriter)
        for item in useriter:
            userdict[item[1]] = item[0]
    with open(pairscsv_fileloca) as file:
        pairiter = csv.reader(file)
        next(pairiter)
        for item in pairiter:
            if item[1] not in pair:
                pair[item[1]] = [userdict[item[0]]]
            else:
                pair[item[1]].append(userdict[item[0]])
    return pair


async def import_user_to_database(userscsv_fileloca):
    async for sess in get_session():
        for item in read_user(userscsv_fileloca):
            try:
                if "github_org" not in item:
                    make_user = User(name=item)
                    sess.add(make_user)
                    await sess.flush()
                    await sess.commit()
                    print(f"[{datetime.now().strftime(format)}] User '{item}' created.")
                else:
                    print(f"[{datetime.now().strftime(format)}] User '{item}' abandoned.")
            except Exception as expt:
                await sess.rollback()
                print(f"[{datetime.now().strftime(format)}] User '{item}' failed.")
                print(f"An error occurred: {expt}")
        await sess.close()


async def import_repo_to_database(userscsv_fileloca, reposcsv_fileloca, pairscsv_fileloca):
    pairdata, done = read_pair(userscsv_fileloca, pairscsv_fileloca), set()
    async for sess in get_session():
        for item in read_repo(reposcsv_fileloca):
            name, desc, team, active = item
            if active == "f":
                continue

            try:
                flag = 0
                if team in pairdata:
                    flag = 1
                else:
                    try:
                        flag = 2
                        qery = select(User).filter_by(name=team).options(selectinload("*"))
                        rslt = await sess.execute(qery)
                        user = rslt.scalar_one()
                    except NoResultFound:
                        print(
                            f"[{datetime.now().strftime(format)}] "
                            f"Service '{team}/{name}' abandoned."
                        )
                        continue

                # SERVICE IS TO BE CREATED ONLY IF FLAG IS 1 OR 2
                # ORPHANS ARE TO BE ABANDONED
                make_service = Service(
                    name=f"{team}/{name}",
                    uuid=uuid4().hex[0:8],
                    type="github",
                    desc=f"Migrated from GitHub2FedMsg. {desc}",
                    disabled=False,
                )
                sess.add(make_service)
                await sess.flush()
                await sess.commit()

                if flag == 1:
                    if team not in done:
                        for username in pairdata[team]:
                            qery = select(User).filter_by(name=username).options(selectinload("*"))
                            rslt = await sess.execute(qery)
                            user = rslt.scalar_one()
                            stmt = owners_table.insert().values(
                                {"service_id": make_service.id, "user_id": user.id}
                            )
                            await sess.execute(stmt)
                            await sess.commit()
                            done.add(team)
                elif flag == 2:
                    qery = select(User).filter_by(name=team).options(selectinload("*"))
                    rslt = await sess.execute(qery)
                    user = rslt.scalar_one()
                    stmt = owners_table.insert().values(
                        {"service_id": make_service.id, "user_id": user.id}
                    )
                    await sess.execute(stmt)
                    await sess.commit()

                print(f"[{datetime.now().strftime(format)}] Service '{team}/{name}' created.")
            except Exception as expt:
                await sess.rollback()
                print(f"[{datetime.now().strftime(format)}] Service '{team}/{name}' failed.")
                print(f"An error occurred: {expt}")
        await sess.close()


@click.command
@click.option(
    "-u", "--users", required=True, type=click.Path(readable=True), help="Path to the users CSV"
)
@click.option(
    "-r", "--repos", required=True, type=click.Path(readable=True), help="Path to the repos CSV"
)
@click.option(
    "-p", "--pairs", required=True, type=click.Path(readable=True), help="Path to the pairs CSV"
)
def main(users, repos, pairs):
    # Ensure that the W2FM_CONFIG environment variable points towards the correct file
    get_config()

    async def _main():
        await import_user_to_database(users)
        await import_repo_to_database(users, repos, pairs)

    run(_main())


if __name__ == "__main__":
    main()

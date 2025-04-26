import logging
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import URL

from .config import get_config
from .main import create_app
from .models import Service, User
from .models.owners import owners_table


log = logging.getLogger(__name__)


async def create_service(
    db: AsyncSession,
    *,
    service_type: str,
    service_name: str,
    owner: str,
    service_description: str = "",
) -> Service:
    db_user = await db.scalar(select(User).where(User.name == owner))
    if not db_user:
        db_user = User(name=owner)
        db.add(db_user)
        log.debug("Adding user %s", owner)
        await db.flush()
    db_service = Service(
        name=service_name,
        uuid=uuid4().hex[0:8],
        type=service_type,
        desc=service_description,
        disabled=False,
    )
    db.add(db_service)
    try:
        await db.flush()
    except IntegrityError as e:
        log.warning("Service already exists.")
        await db.rollback()
        raise ValueError(f"Service {service_name} already exists") from e
    stmt = owners_table.insert().values({"service_id": db_service.id, "user_id": db_user.id})
    await db.execute(stmt)
    log.info("Service %s created", db_service.name)
    print(
        f"""Hi @{owner} !

You can now add the following webhook to the """
        f'{"repo" if "/" in service_name else "organization"} '
        "mentioned above."
    )
    if "/" in service_name:
        user_or_org, repo_name = service_name.split("/")
        print(
            f"Note that you can also add the webhook at the organization level (`{user_or_org}`), "
            "which will make it active for all the organization's repos. I would suggest doing "
            "that to save some effort and automatically cover repos you may add in the future "
            "(make sure however than another teammate hasn't already added it)."
        )
    datagrepper_url = URL(get_config().datagrepper_url)
    if datagrepper_url.netloc == "apps.fedoraproject.org":
        base_url = "https://webhook.fedoraproject.org"
    elif datagrepper_url.netloc == "apps.stg.fedoraproject.org":
        base_url = "https://webhook2fedmsg.apps.ocp.stg.fedoraproject.org"
    else:
        base_url = ""
    app = create_app()
    service_url = app.url_path_for("create_message", uuid=db_service.uuid)
    print(
        f"""
```
Webhook URL: {base_url}{service_url}
Secret: {db_service.token}
Webhook content-type: application/json
```

Please tell us if there are any issues! Thanks!
"""
    )
    return db_service

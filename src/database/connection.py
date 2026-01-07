from sqlalchemy import create_engine, MetaData
import uuid
from datetime import datetime, timezone
from typing import Any
from src.utils.config import get_database_url
from sqlalchemy import func


engine = create_engine(get_database_url())
metadata = MetaData()
# Do not create tables here — tables are defined in `src.database.schema`.
# Table creation (metadata.create_all) will be invoked after all table
# definitions are imported (see src.main).

new_uuid = uuid.uuid4
now = datetime.now(timezone.utc)
default_now: dict[str, Any] = {"default": now, "server_default": func.now()}
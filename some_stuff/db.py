import databases
import sqlalchemy as sa

from settings import settings

database = databases.Database(settings.db_url, force_rollback=settings.testing)
metadata = sa.MetaData()

some_stuff_tbl = sa.Table(
    "some_stuff",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
)

engine = sa.create_engine(settings.db_url)
metadata.create_all(engine)

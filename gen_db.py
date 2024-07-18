TEMPLATE = """
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, UUID, Enum, JSON, Column


class Base(DeclarativeBase):
    __table_args__ = {{
        'extend_existing': True
    }}


DATABASE_URL = "sqlite:///db.sqlite3"    

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# if you use alembic, you don't need this function
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class {kind}(Base):
    uuid = Column(UUID, primary_key=True, nullable=False)
    kind = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    description = Column(String, nullable=False)
    state = Column(Enum("NEW", "INSTALLING", "RUNNING", name="state"), nullable=False, default="NEW")
    json = Column(JSON, nullable=False)

"""

def gen_db(path, kind: str):
    with open(f"{path}/db.py", "w") as f:
        f.write(TEMPLATE.format(kind=kind.capitalize()))
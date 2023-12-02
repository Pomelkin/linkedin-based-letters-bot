from sqlalchemy import Table, Column, MetaData, Integer, Text

metadata = MetaData()

texts = Table(
    "video2text",
    metadata,
    Column('id', Integer, primary_key=True),
    Column("user_id", Integer),
    Column("user_name", Text),
    Column("text_from_video", Text)
)

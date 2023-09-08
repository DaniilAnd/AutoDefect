from sqlalchemy import TIMESTAMP, VARCHAR, Integer, Table, Column, MetaData
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

reports = Table(
    "reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=True),
    Column("image_path", VARCHAR(255), nullable=True),
    Column("bbox_json", JSONB, nullable=True),
    Column("time_escalation", TIMESTAMP, nullable=True),
    Column("gps_coordinates", JSONB, nullable=True),
    Column("city", VARCHAR(255), nullable=True),
    Column("street", VARCHAR(255), nullable=True),
    Column("state", VARCHAR(255), nullable=True),
)
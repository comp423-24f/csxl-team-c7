"""Join table of membership between User and Organization entities.""" ""

from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from .entity_base import EntityBase

user_organization_table = Table(
    "user_organization_table",
    EntityBase.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("role", String),
)

"""Join table of membership between User and Organization entities.""" ""

from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from .entity_base import EntityBase


class UserOrganization(EntityBase):
    __tablename__ = "user_organization"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), primary_key=True)
    role = Column(String)

    user = relationship("User", backref="user_organizations")
    organization = relationship("Organization", backref="user_organizations")


# user_organization_table = Table(
#    "user_organization",
#    EntityBase.metadata,
#    Column("user_id", ForeignKey("user.id"), primary_key=True),
#    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
#    Column("role", String),
# )

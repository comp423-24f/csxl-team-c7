from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from .entity_base import EntityBase
from ..models.organization_message import OrganizationMessage


class OrganizationMessageEntity(EntityBase):
    __tablename__ = "organization_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    # Relationships
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="messages")
    user: Mapped["UserEntity"] = relationship(back_populates="messages")

    @classmethod
    def from_model(cls, model: OrganizationMessage) -> Self:
        """
        Class method that converts an `OrganizationMessage` model into a `OrganizationMessageEntity`

        Parameters:
            - model (OrganizationMessage): Model to convert into an entity
        Returns:
            OrganizationMessageEntity: Entity created from model
        """
        return cls(
            id=model.id,
            organization_id=model.organization_id,
            user_id=model.user_id,
            content=model.content,
            created_at=model.created_at,
        )

    def to_model(self) -> OrganizationMessage:
        """
        Converts a `OrganizationMessageEntity` object into a `OrganizationMessage` model object

        Returns:
            OrganizationMessage: `OrganizationMessage` object from the entity
        """
        return OrganizationMessage(
            id=self.id,
            organization_id=self.organization_id,
            user_id=self.user_id,
            content=self.content,
            created_at=self.created_at,
        )

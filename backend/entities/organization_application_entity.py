"""Definition of SQLAlchemy table-backed object mapping entity for Organization Applications."""

from datetime import datetime
from typing import Self
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from sqlalchemy import Enum as SQLAlchemyEnum

from ..models.organization_application_state import ApplicationState
from ..models.organization_application_details import OrganizationApplicationDetails
from ..models.organization_application import (
    OrganizationApplication,
    NewOrganizationApplication,
)

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationApplicationEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `OrganizationApplication` table"""

    # Name for the applications table in the PostgreSQL database
    __tablename__ = "organization__application"

    # Unique id for OrganizationApplication
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Application content
    answers: Mapped[str] = mapped_column(Text, nullable=False)

    # State of application (e.g., PENDING, APPROVED, REJECTED)
    state: Mapped[ApplicationState] = mapped_column(
        SQLAlchemyEnum(ApplicationState),
        default=ApplicationState.PENDING,
        nullable=False,
    )

    # Timestamps for application lifecycle
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )

    # Reviewer's notes
    reviewer_notes: Mapped[str] = mapped_column(String, default="", nullable=False)

    # Reference to the organization being applied to
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    organization: Mapped["OrganizationEntity"] = relationship(
        back_populates="applications"
    )

    # Reference to the applicant
    applicant_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    applicant: Mapped["UserEntity"] = relationship(
        "UserEntity", foreign_keys=[applicant_id]
    )

    # Reference to the reviewer (optional)
    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    reviewer: Mapped["UserEntity"] = relationship(
        "UserEntity", foreign_keys=[reviewer_id]
    )

    @classmethod
    def from_new_model(cls, model: NewOrganizationApplication) -> Self:
        """
        Class method that converts a `NewOrganizationApplication` model into an `OrganizationApplicationEntity`

        Parameters:
            - model (NewOrganizationApplication): Model to convert into an entity
        Returns:
            OrganizationApplicationEntity: Entity created from model
        """
        return cls(
            answers=model.answers,
            organization_id=model.organization_id,
            applicant_id=model.applicant_id,
        )

    @classmethod
    def from_model(cls, model: OrganizationApplication) -> Self:
        """
        Class method that converts an `OrganizationApplication` model into an `OrganizationApplicationEntity`

        Parameters:
            - model (OrganizationApplication): Model to convert into an entity
        Returns:
            OrganizationApplicationEntity: Entity created from model
        """
        return cls(
            id=model.id,
            answers=model.answers,
            state=model.state,
            created_at=model.created_at,
            reviewed_at=model.reviewed_at,
            reviewer_notes=model.reviewer_notes,
            organization_id=model.organization_id,
            applicant_id=model.applicant_id,
            reviewer_id=model.reviewer_id,
        )

    def to_model(self) -> OrganizationApplication:
        """
        Converts an `OrganizationApplicationEntity` object into an `OrganizationApplication` model object

        Returns:
            OrganizationApplication: `OrganizationApplication` object from the entity
        """
        return OrganizationApplication(
            id=self.id,
            answers=self.answers,
            state=self.state,
            created_at=self.created_at,
            reviewed_at=self.reviewed_at,
            reviewer_notes=self.reviewer_notes,
            organization_id=self.organization_id,
            applicant_id=self.applicant_id,
            reviewer_id=self.reviewer_id,
        )

    def to_details_model(self) -> OrganizationApplicationDetails:
        """
        Converts an `OrganizationApplicationEntity` object into an `OrganizationApplicationDetails` model object

        Returns:
            OrganizationApplicationDetails: `OrganizationApplicationDetails` object from the entity
        """
        return OrganizationApplicationDetails(
            id=self.id,
            answers=self.answers,
            state=self.state,
            created_at=self.created_at,
            reviewed_at=self.reviewed_at,
            reviewer_notes=self.reviewer_notes,
            organization_id=self.organization_id,
            applicant_id=self.applicant_id,
            reviewer_id=self.reviewer_id,
            organization=self.organization.to_model(),
            applicant=self.applicant.to_model(),
            reviewer=self.reviewer.to_model() if self.reviewer is not None else None,
        )

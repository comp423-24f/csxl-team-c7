from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from .entity_base import EntityBase
from ..models.organization_application import OrganizationApplication, ApplicationStatus


class OrganizationApplicationEntity(EntityBase):
    """Database model for organization applications"""

    __tablename__ = "organization_application"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(
        back_populates="organization_applications"
    )

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(
        back_populates="applications"
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        SQLAlchemyEnum(ApplicationStatus), default=ApplicationStatus.PENDING
    )
    interest_statement: Mapped[str] = mapped_column(String)
    experience: Mapped[str] = mapped_column(String)
    expected_graduation: Mapped[str] = mapped_column(String)
    program_pursued: Mapped[str] = mapped_column(String)
    additional_info: Mapped[str] = mapped_column(String)

    admin_response: Mapped[str | None] = mapped_column(String, nullable=True)

    @classmethod
    def from_model(cls, model: OrganizationApplication) -> Self:
        return cls(
            id=model.id,
            user_id=model.user_id,
            organization_id=model.organization_id,
            status=model.status,
            interest_statement=model.interest_statement,
            experience=model.experience,
            expected_graduation=model.expected_graduation,
            program_pursued=model.program_pursued,
            additional_info=model.additional_info,
            admin_response=model.admin_response,
        )

    def to_model(self) -> OrganizationApplication:
        return OrganizationApplication(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            status=self.status,
            interest_statement=self.interest_statement,
            experience=self.experience,
            expected_graduation=self.expected_graduation,
            program_pursued=self.program_pursued,
            additional_info=self.additional_info,
            admin_response=self.admin_response,
        )

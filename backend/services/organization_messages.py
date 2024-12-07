from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.services.exceptions import ResourceNotFoundException

from ..database import db_session
from ..models.organization_message import OrganizationMessage
from ..entities.organization_entity import OrganizationEntity
from ..entities.organization_messages import (
    OrganizationMessage,
    OrganizationMessageEntity,
)
from ..models import User
from .permission import PermissionService


class OrganizationMessageService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        self._session = session
        self._permission = permission

    def create_message(
        self, subject: User, organization_slug: str, content: str
    ) -> OrganizationMessage:
        """
        Create an announcement for all members of the organization to see, only for admin posting

        """
        # Verify admin permissions, change when permission state story is added
        self._permission.enforce(
            subject, "organization.*", f"organization/{organization_slug}"
        )

        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == organization_slug)
            .one_or_none()
        )

        if not organization:
            raise ResourceNotFoundException(
                f"Organization {organization_slug} not found"
            )

        message = OrganizationMessageEntity(
            organization_id=organization.id, user_id=subject.id, content=content
        )

        self._session.add(message)
        self._session.commit()

        return message.to_model()

    def update_message(
        self, subject: User, message_id: int, content: str
    ) -> OrganizationMessage:
        """
        Allows admins to update the message for users to see

        """
        message = self._session.get(OrganizationMessageEntity, message_id)
        if not message:
            raise ResourceNotFoundException("Message not found")

        # Check permissions
        self._permission.enforce(
            subject, "organization.*", f"organization/{message.organization.slug}"
        )

        message.content = content
        self._session.commit()
        return message.to_model()

    def delete_message(self, subject: User, message_id: int) -> None:
        """
        Deletes a previous announcement made

        """
        message = self._session.get(OrganizationMessageEntity, message_id)
        if not message:
            raise ResourceNotFoundException("Message not found")

        # Check permissions
        self._permission.enforce(
            subject, "organization.*", f"organization/{message.organization.slug}"
        )

        self._session.delete(message)
        self._session.commit()

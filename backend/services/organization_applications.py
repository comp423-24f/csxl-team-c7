"""
The Organization Applications Service allows the API to manipulate organization applications data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.organization_application import (
    OrganizationApplication,
    NewOrganizationApplication,
)
from ..models.organization_application_details import OrganizationApplicationDetails
from ..models.organization_application_state import ApplicationState
from ..models.user import User
from ..entities.organization_application_entity import OrganizationApplicationEntity
from ..entities.organization_entity import OrganizationEntity
from .permission import PermissionService
from .exceptions import ResourceNotFoundException

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationApplicationService:
    """Service that performs all of the actions on the `OrganizationApplication` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the database session and permission service."""
        self._session = session
        self._permission = permission

    def create(
        self,
        subject: User,
        organization_id: int,
        application: NewOrganizationApplication,
    ) -> OrganizationApplication:
        """
        Creates a new organization application.

        Parameters:
            subject: Currently logged in user
            organization_id: ID of the organization being applied to
            application: Application content and details

        Returns:
            OrganizationApplication: Created application

        Raises:
            ResourceNotFoundException: If organization doesn't exist
        """
        # Check if organization exists
        org = self._session.get(OrganizationEntity, organization_id)
        if not org:
            raise ResourceNotFoundException(
                f"No organization found with ID: {organization_id}"
            )

        # Check for existing pending application
        query = select(OrganizationApplicationEntity).where(
            OrganizationApplicationEntity.organization_id == organization_id,
            OrganizationApplicationEntity.applicant_id == subject.id,
            OrganizationApplicationEntity.state == ApplicationState.PENDING,
        )
        existing = self._session.scalars(query).first()

        if existing:
            raise ResourceNotFoundException(
                "You already have a pending application for this organization"
            )

        # Create new application
        application_entity = OrganizationApplicationEntity.from_new_model(
            NewOrganizationApplication(
                answers=application.answers,
                organization_id=organization_id,
                applicant_id=subject.id,
            )
        )

        self._session.add(application_entity)
        self._session.commit()

        return application_entity.to_model()

    def get(self, subject: User, application_id: int) -> OrganizationApplicationDetails:
        """
        Get details of a specific application.

        Parameters:
            subject: Currently logged in user
            application_id: ID of the application to retrieve

        Returns:
            OrganizationApplicationDetails: Application details

        Raises:
            ResourceNotFoundException: If application not found
        """
        query = select(OrganizationApplicationEntity).where(
            OrganizationApplicationEntity.id == application_id
        )
        application = self._session.scalars(query).one_or_none()

        if not application:
            raise ResourceNotFoundException(
                f"No application found with ID: {application_id}"
            )

        # Check permissions
        if application.applicant_id == subject.id:
            self._permission.enforce(
                subject,
                "organization.application.view",
                f"organization/{application.organization_id}/application/{application_id}",
            )

        return application.to_details_model()

    def review(
        self, subject: User, application_id: int, application: OrganizationApplication
    ) -> OrganizationApplication:
        """
        Review an application.

        Parameters:
            subject: Currently logged in user (reviewer)
            application_id: ID of the application
            application: Updated application data

        Returns:
            OrganizationApplication: Updated application

        Raises:
            ResourceNotFoundException: If application not found
        """
        # Check if user has review permissions
        self._permission.enforce(
            subject,
            "organization.application.review",
            f"organization/{application.organization_id}/application/{application_id}",
        )

        application_entity = self._session.get(
            OrganizationApplicationEntity, application_id
        )
        if not application_entity:
            raise ResourceNotFoundException(
                f"No application found with ID: {application_id}"
            )

        # Update application
        application_entity.state = application.state
        application_entity.reviewer_id = subject.id
        application_entity.reviewer_notes = application.reviewer_notes

        self._session.commit()
        return application_entity.to_model()

    def list_by_organization(
        self, subject: User, organization_id: int
    ) -> list[OrganizationApplicationDetails]:
        """
        List all applications for an organization.

        Parameters:
            subject: Currently logged in user
            organization_id: ID of the organization

        Returns:
            list[OrganizationApplicationDetails]: List of applications
        """
        # Check if user has permission to view organization applications
        self._permission.enforce(
            subject,
            "organization.application.list",
            f"organization/{organization_id}/applications",
        )

        query = select(OrganizationApplicationEntity).where(
            OrganizationApplicationEntity.organization_id == organization_id
        )
        applications = self._session.scalars(query).all()

        return [app.to_details_model() for app in applications]

    def list_by_user(self, subject: User) -> list[OrganizationApplicationDetails]:
        """
        List all applications submitted by a user.

        Parameters:
            subject: Currently logged in user

        Returns:
            list[OrganizationApplicationDetails]: List of user's applications
        """
        query = select(OrganizationApplicationEntity).where(
            OrganizationApplicationEntity.applicant_id == subject.id
        )
        applications = self._session.scalars(query).all()

        return [app.to_details_model() for app in applications]

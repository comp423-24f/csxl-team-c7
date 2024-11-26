from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.organization_application import OrganizationApplication, ApplicationStatus
from ..models.organization_details import OrganizationDetails
from ..models.user_details import UserDetails
from ..entities.organization_application_entity import OrganizationApplicationEntity
from ..entities.organization_entity import OrganizationEntity
from ..entities.user_entity import UserEntity
from ..models import User
from .permission import PermissionService
from .exceptions import ResourceNotFoundException


class OrganizationApplicationService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        self._session = session
        self._permission_svc = permission_svc

    def get_organization_applications(
        self, subject: User, organization_slug: str
    ) -> OrganizationDetails:
        """Get organization details including all applications (admin only)"""
        self._permission_svc.enforce(
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

        return organization.to_details_model()

    def get_user_applications(self, user_id: int) -> UserDetails:
        """Get user details including their applications"""
        user = self._session.get(UserEntity, user_id)
        if not user:
            raise ResourceNotFoundException(f"User {user_id} not found")

        return user.to_details_model()

    def create(
        self,
        subject: User,
        organization_slug: str,
        application: OrganizationApplication,
    ) -> OrganizationDetails:
        """Creates a new application and returns updated org details"""
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == organization_slug)
            .one_or_none()
        )

        if not organization:
            raise ResourceNotFoundException(
                f"Organization {organization_slug} not found"
            )

        # Verify organization requires applications
        if not organization.needs_application:
            raise ResourceNotFoundException(
                "This organization does not require applications"
            )

        # Create application
        application_entity = OrganizationApplicationEntity(
            user_id=subject.id,
            organization_id=organization.id,
            interest_statement=application.interest_statement,
            experience=application.experience,
            expected_graduation=application.expected_graduation,
            program_pursued=application.program_pursued,
            additional_info=application.additional_info,
        )

        self._session.add(application_entity)
        self._session.commit()

        return organization.to_details_model()

    def update_status(
        self,
        subject: User,
        application_id: int,
        status: ApplicationStatus,
        admin_response: str | None = None,
    ) -> OrganizationDetails:
        """Update application status and return updated org details"""
        application = self._session.get(OrganizationApplicationEntity, application_id)
        if not application:
            raise ResourceNotFoundException("Application not found")

        organization = self._session.get(
            OrganizationEntity, application.organization_id
        )
        if not organization:
            raise ResourceNotFoundException("Organization not found")

        # Verify admin permissions
        self._permission_svc.enforce(
            subject, "organization.*", f"organization/{organization.slug}"
        )

        application.status = status
        if admin_response:
            application.admin_response = admin_response

        # If approved, add user as member
        if status == ApplicationStatus.APPROVED:
            user = self._session.get(UserEntity, application.user_id)
            if user not in organization.users:
                organization.users.append(user)

        self._session.commit()

        return organization.to_details_model()

    def delete(self, subject: User, application_id: int) -> OrganizationDetails:
        """Delete an application and return updated org details"""
        application = self._session.get(OrganizationApplicationEntity, application_id)
        if not application:
            raise ResourceNotFoundException("Application not found")

        organization = self._session.get(
            OrganizationEntity, application.organization_id
        )
        if not organization:
            raise ResourceNotFoundException("Organization not found")

        # Allow deletion by applicant or admin
        if subject.id != application.user_id:
            self._permission_svc.enforce(
                subject,
                "organization.*",
                f"organization/{organization.slug}",
            )

        self._session.delete(application)
        self._session.commit()

        return organization.to_details_model()

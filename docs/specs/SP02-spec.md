# Organization Application Technical Specification

> Written by [Tejas Chandramouli](https://github.com/tchandr) for the CSXL Web Application.

This document contains the technical specifications for the new Organization features for the CSXL web application. This feature so far adds _5_ new database tables, _15_ new API routes, and _4_ new frontend component to the application.

SP02 focused on adding functionality for the application page on both the member and admin side, which was only a mockup frontend in SP01. Users are now able to apply to organizations, and admins can accept or deny these applications, changes of which are reflected on the organization page.

SP02 also includes a user members list with Academic term listing. This is dynamically reflected with user joining, leaving, and application acceptance/denial.

SP02 also adds an announcements tab, with admin ability to post announcements, and Users viewing announcements if they are a member.

## Descriptions/Sample Data<a name='Descriptions/Sample Data'></a>

There are two new models that was added, OrganizationApplication and OrganizationMessages. We also added an ApplicationStatus Model for enums.

```py
OrganizationApplication:
    "id": int | None = None
    "user_id": int
    "organization_id": int
    "status": ApplicationStatus = ApplicationStatus.PENDING
    "interest_statement": str
    "experience": str
    "expected_graduation": str
    "program_pursued": str
    "additional_info": str
    "admin_response": str | None = None
```

```py
OrganizationMessages:
    "id": int | None = None
    "organization_id": int
    "user_id": int
    "content": str
    "created_at": datetime | None = None
```

Subsequent API routes were created to support these functions, as seen in Organization and Organization_Application.

## Database/Entity Decisions<a name='Database/Entity Decisions'></a>

In addition to the SP01 relationships, the Messages and Applications are a part of the OrganizationDetails model, for further abstraction and SoC. These result in Many-to-Many relationships between Users, OrganizationDetails, and the needed entity. Users are allowed to have applications for multiple organizations, and organizations are able to have applications from multiple users. Same logic applies to the announcements.

## Decisions and TradeOffs<a name='Decisions and Tradeoffs'></a>

**UX Decision-** We decided to disallow admins to be members of an organization, until an admin accepts the application. This is partially because the CSXL website doesn't have a global academic term, and the only way to add this was to retrieve it from the application. This means that only organizations with applications will have the academic term listed. This can be edited for future use, but the level of importance for application-based organization is what led us to this decision.

**Technical Decision-** One technical decision we made was having a universal application for all clubs, in the sense that all organizations would have the same application structure. This was because creating a form-control document that organization-admins themselves could edit and deploy would have taken a lot of time. The middle ground we came with is a compromise between this high level concept, and a google form link.

## Development Decisions<a name='Development Decisions'></a>

**FrontEnd**

Multiple widgets were added, as well as another routing component. This inlcudes organization-application.model.ts, organization-application-review component files, organization-apply component files, and the organization-messages and organization-members-card widgets. All of these work together to fill out the user story.

**Backend**

-As mentioned before, there were two major functionalities created. This includes the OrganizationMessages and OrganizationApplication models, entities, and service functions.

To comprehensively get started, follow this path.

-Backend: Look at the Organization_application and Organization API functions, as these are the closest to the frontend functions.
Organization_Application, Organization_messages, and Organizaiton Entities would be next, as well as these models and services. For the frontend, look at the model files, such as Organization-Application model and Organization-Message model

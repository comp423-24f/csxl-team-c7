# Organization Application Technical Specification

> Written by [Aneesh Sallaram](https://github.com/asallarma) for the CSXL Web Application.

This document contains the technical specifications for the new Organization features for the CSXL web application. This feature so far adds _3_ new database tables, _4_ new API routes, and _1_ new frontend component to the application.

SP01 focused on user functionality on determining the status of an organization between Open, Closed, Apply. It also allows users to join/leave an organization, seeing a button for applying for an organization (functionality for which will be added on another sprint), and viewing membership.

This functionality also allows Admins to determine the state of their organizations, whether it's open, closed, or applicable.

DESCRIPTIONS AND SAMPLE DATA
The OrganizationEntity class in models/organization_entity.py has been updated to support new fields related to the public and application requirements of an organization. These fields are called public and needs_application. An example of the organization entity in a json payload to the front-end is:
{
"id": 1,
"name": "App Team",
"slug": "app-team",
"shorthand": "app",
"logo": "url_to_logo",
"short_description": "An organization focused on mobile app development.",
"long_description": "We create apps for clients who are looking for a specific mobile app design.",
"website": "http://app-team.com",
"email": "contact@app-team.com",
"instagram": "http://instagram.com/app-team",
"linked_in": "http://linkedin.com/company/app-team",
"youtube": "http://youtube.com/app-team",
"heel_life": "http://heel-life.com/app-team",
"public": true,
"needs_application": true
}
Furthermore, we support the ability for the change in publicity or whether or not the club needs an application, for example if App Team wants to go private: A put method used in conjunction with the API to update (for “app-team’)
“public”: true, to “public”: false.
This updates the UI for all potential applicants as the org cannot be applied for and needs_application will also be set to false regardless of what the previous value was.

DATABASE/ENTITY DECISIONS
Many-to-Many Relationship Representation in the database overall: The relationship between users and clubs is inherently many-to-many because a single user can join multiple orgs and a single org can have multiple members. To implement this relationship, we use a table to connect the users to their organizations and then that is then reflected in their personal UI experience.
Some specific entity decisions are that users can apply to many clubs due to specific different attributes and clubs can have many users as we spoke about above, and this allows clubs and users to grow in number without facing number constraints or scalability issues.

DECISIONS/TRADEOFFS
UX Decision- We decided to add the ability to see what an organization’s current application status is directly on the individual organization widget i.e. closed, open, apply. Although a tradeoff for this may be more clustered buttons in the UI page for users, we believe it’s important for users to have information immediately about the application status of clubs instead of having to click through the details every time.
Technical Decision- Ability for users to automatically join clubs whenever they please directly from the CSXL website. A tradeoff is that this may lead to confusion because generally HeelLife has been used to do applications and this is where you are accepted. However, we think this leads closer to an overall CSXL website that can host all these functionalities related to applications.

DEVELOPMENT DECISIONS
Frontend
Take a look at our organization.ts, organization-model.ts, and other modules related to the overall organization. This is where we made changes to add the button that is specific to each user on their application status and allows clubs to have that functionality of being open or closed. Our widgets/organization-card contains functionality on what to display if an organization is open or closed and routes buttons if an organization.slug is indeed set to ‘apply’.
Our frontend also showcases how we are importing functionalities and UX/UI is reflecting our changes in the backend. By first importing a mat-chips module in our organization.model.ts we are able to do this in our organization-card-widget.html:
@if (organization.website !== '') {
<social-media-icon id="events-button" [fontIcon]="'link'" [href]="organization.website" />
}
@if (!organization.open_status) {
<mat-chip>Closed</mat-chip>
} @else if (organization.needs_application) {
<a [routerLink]="['/organizations', organization.slug, 'apply']">
<button mat-flat-button>Apply</button>
</a>
} @else if (organization.public) {
<mat-chip>Open</mat-chip>
}
Overall our front-end is largely seen in our organizations files of html, ts, etc.
Backend
To get started with looking at our backend, look at our OrganizationEntity model in the models/organization.py file, where the public and needs_application fields were added. These fields are used to manage access to organizations, with admins of each org determining whether an organization is open to all users and needs_application indicating if membership needs an application or can be joined by anyone. Next, examine the API endpoint files, such as controllers/organizationController.py and routes/organizationRoutes.py, to understand how these fields are used in API requests. The frontend components, likely found in src/components/OrganizationPage.js or src/pages/OrganizationDetails.js, should also be reviewed to see how the public and needs_application fields affect the UI and user interaction and for an overall view on our end-to-end action. Additionally, reviewing the database migration files in migrations/ will show you these fields are correctly applied to the database. Finally, checking the related tests in tests/organization.test.js will ensure the feature is 100% covered.
I would also recommend looking at models and services for a quick overview of the variables we added and where they are declared. The variables obj.open_status and obj.needs_application further integrate within the overall organization variables and that can be seen there. Overall, the addition of two variables and their functionality can be seen all over the backend in different spots where they connect to the frontend.

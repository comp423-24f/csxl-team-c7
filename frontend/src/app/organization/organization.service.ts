/**
 * The Organization Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, computed, signal } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, tap } from 'rxjs';
import {
  ApplicationStatus,
  OrganizationApplication
} from './organization-application.model';
import { Organization } from './organization.model';
import { PermissionService } from '../permission.service';
import { OrganizationMessage } from './widgets/organization-messages/organization-message.model';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  /** Organizations signal */
  private organizationsSignal: WritableSignal<Organization[]> = signal([]);
  organizations = this.organizationsSignal.asReadonly();

  /** Computed organization signals */
  adminOrganizations = computed(() => {
    return this.organizations().filter((organization) => {
      return this.permissionService.checkSignal(
        'organization.*',
        'organization/' + organization.slug
      );
    });
  });

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar,
    protected permissionService: PermissionService
  ) {
    this.getOrganizations();
  }

  /** Refreshes the organization data emitted by the organizations signal. */
  getOrganizations() {
    this.http
      .get<Organization[]>('/api/organizations')
      .subscribe((organizations) => {
        this.organizationsSignal.set(organizations);
      });
  }

  /** Gets an organization based on its slug.
   * @param slug: String representing the organization slug
   * @returns {Observable<Organization | undefined>}
   */
  getOrganization(slug: string): Observable<Organization | undefined> {
    return this.http.get<Organization>('/api/organizations/' + slug);
  }

  /** Returns the new organization object from the backend database table using the backend HTTP post request
   *  and updates the organizations signal to include the new organization.
   * @param organization: Organization to add
   * @returns {Observable<Organization>}
   */
  createOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .post<Organization>('/api/organizations', organization)
      .pipe(
        tap((organization) =>
          this.organizationsSignal.update((organizations) => [
            ...organizations,
            organization
          ])
        )
      );
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request
   *  and update the organizations signal to include the updated organization.
   * @param organization: Represents the updated organization
   * @returns {Observable<Organization>}
   */
  updateOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .put<Organization>('/api/organizations', organization)
      .pipe(
        tap((updatedOrganization) =>
          this.organizationsSignal.update((organizations) => [
            ...organizations.filter((o) => o.id != updatedOrganization.id),
            updatedOrganization
          ])
        )
      );
  }
  joinOrganization(slug: string): Observable<Organization> {
    return this.http.post<Organization>(`/api/organizations/${slug}/join`, {});
  }

  leaveOrganization(slug: string): Observable<Organization> {
    return this.http.post<Organization>(`/api/organizations/${slug}/leave`, {});
  }

  isMember(slug: string): Observable<boolean> {
    return this.http.get<boolean>(`/api/organizations/${slug}/membership`);
  }

  /** Returns the deleted organization object from the backend database table using the backend HTTP delete request
   *  and updates the organizations signal to exclude the deleted organization.
   * @param organization: Represents the deleted organization
   * @returns {Observable<Organization>}
   */
  deleteOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .delete<Organization>(`/api/organizations/${organization.slug}`)
      .pipe(
        tap((deletedOrganization) => {
          this.organizationsSignal.update((organizations) =>
            organizations.filter((o) => o.id != deletedOrganization.id)
          );
        })
      );
  }
  getOrganizationApplications(slug: string): Observable<Organization> {
    return this.http.get<Organization>(
      `/api/organizations/${slug}/applications`
    );
  }
  submitApplication(
    slug: string,
    application: {
      interest_statement: string;
      experience: string;
      expected_graduation: string;
      program_pursued: string;
      additional_info: any;
    }
  ): Observable<OrganizationApplication> {
    return this.http.post<OrganizationApplication>(
      `/api/organizations/${slug}/apply`,
      {
        interest_statement: application.interest_statement,
        experience: application.experience,
        expected_graduation: application.expected_graduation,
        program_pursued: application.program_pursued,
        additional_info: application.additional_info,

        user_id: 0,
        organization_id: 0,
        status: 'PENDING'
      }
    );
  }
  createMessage(
    slug: string,
    content: string
  ): Observable<OrganizationMessage> {
    return this.http.post<OrganizationMessage>(
      `/api/organizations/${slug}/messages?content=${content}`,
      {}
    );
  }

  updateMessage(
    messageId: number,
    content: string
  ): Observable<OrganizationMessage> {
    return this.http.put<OrganizationMessage>(
      `/api/organizations/messages/${messageId}?content=${content}`,
      {}
    );
  }

  deleteMessage(messageId: number): Observable<void> {
    return this.http.delete<void>(`/api/organizations/messages/${messageId}`);
  }

  updateApplicationStatus(
    applicationId: number,
    status: ApplicationStatus,
    adminResponse?: string
  ): Observable<Organization> {
    const params = {
      status: status,
      admin_response: adminResponse || ''
    };

    return this.http.put<Organization>(
      `/api/organizations/applications/${applicationId}`,
      {},
      { params: params }
    );
  }
}

/**
 * The Organization Application Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Tejas Chandra
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, tap } from 'rxjs';
import { PermissionService } from '../permission.service';
import {
  OrganizationApplication,
  OrganizationApplicationDetails,
  NewOrganizationApplication
} from './organization-application.model';

@Injectable({
  providedIn: 'root'
})
export class OrganizationApplicationService {
  /** Applications signal */
  private applicationsSignal: WritableSignal<OrganizationApplicationDetails[]> =
    signal([]);
  applications = this.applicationsSignal.asReadonly();

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar,
    protected permissionService: PermissionService
  ) {}

  /** Gets all applications for an organization
   * @param organization_id: ID of the organization
   * @returns {Observable<OrganizationApplicationDetails[]>}
   */
  getOrganizationApplications(
    organization_id: number
  ): Observable<OrganizationApplicationDetails[]> {
    return this.http
      .get<
        OrganizationApplicationDetails[]
      >(`/api/organizations/applications/organization/${organization_id}`)
      .pipe(
        tap((applications) => {
          this.applicationsSignal.set(applications);
        })
      );
  }

  /** Gets a specific application by ID
   * @param application_id: ID of the application
   * @returns {Observable<OrganizationApplicationDetails>}
   */
  getApplication(
    application_id: number
  ): Observable<OrganizationApplicationDetails> {
    return this.http.get<OrganizationApplicationDetails>(
      `/api/organizations/applications/${application_id}`
    );
  }

  /** Creates a new application
   * @param organization_id: ID of the organization
   * @param application: Application data to create
   * @returns {Observable<OrganizationApplication>}
   */
  createApplication(
    organization_id: number,
    application: NewOrganizationApplication
  ): Observable<OrganizationApplication> {
    return this.http
      .post<OrganizationApplication>(
        `/api/organizations/applications/${organization_id}`,
        application
      )
      .pipe(
        tap(() => {
          this.snackBar.open('Application submitted successfully', '', {
            duration: 3000
          });
        })
      );
  }

  /** Updates the state of an application (for reviewing)
   * @param application_id: ID of the application
   * @param application: Updated application data
   * @returns {Observable<OrganizationApplication>}
   */
  reviewApplication(
    application_id: number,
    application: OrganizationApplication
  ): Observable<OrganizationApplication> {
    return this.http
      .put<OrganizationApplication>(
        `/api/organizations/applications/${application_id}/review`,
        application
      )
      .pipe(
        tap(() => {
          this.snackBar.open('Application reviewed successfully', '', {
            duration: 3000
          });
        })
      );
  }

  /** Gets all applications for the current user
   * @returns {Observable<OrganizationApplicationDetails[]>}
   */
  getUserApplications(): Observable<OrganizationApplicationDetails[]> {
    return this.http
      .get<
        OrganizationApplicationDetails[]
      >('/api/organizations/applications/user/applications')
      .pipe(
        tap((applications) => {
          this.applicationsSignal.set(applications);
        })
      );
  }
}

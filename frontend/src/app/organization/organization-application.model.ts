/**
 * The Organization Application Models define the shape of application data
 * retrieved from the Organization Application Service and the API.
 *
 * @author Tejas Chandra
 * @copyright 2024
 * @license MIT
 */

import { Organization } from './organization.model';
import { Profile } from '../profile/profile.service';

/** State of an organization application */
export enum ApplicationState {
  PENDING = 'PENDING',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
  WITHDRAWN = 'WITHDRAWN',
  NEEDS_INFO = 'NEEDS_INFO'
}

/** Interface for new application submissions */
export interface NewOrganizationApplication {
  answers: string;
  organization_id: number;
  applicant_id: number;
}

/** Interface for basic application data */
export interface OrganizationApplication {
  id: number;
  answers: string;
  state: ApplicationState;
  created_at: Date;
  reviewed_at: Date | null;
  reviewer_notes: string;
  organization_id: number;
  applicant_id: number;
  reviewer_id: number | null;
}

/** Interface for detailed application view (includes relationships) */
export interface OrganizationApplicationDetails
  extends OrganizationApplication {
  organization: Organization;
  applicant: Profile;
  reviewer: Profile | null;
}

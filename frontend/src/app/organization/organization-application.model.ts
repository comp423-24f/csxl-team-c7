export enum ApplicationStatus {
  PENDING = 'PENDING',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED'
}

export interface OrganizationApplication {
  id?: number;
  user_id: number;
  organization_id: number;
  status: ApplicationStatus;
  interest_statement: string;
  experience: string;
  expected_graduation: string;
  program_pursued: string;
  additional_info: any;
  admin_response?: string;
}

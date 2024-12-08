export interface OrganizationMessage {
  id: number | null;
  organization_id: number;
  user_id: number;
  content: string;
  created_at: Date;
}

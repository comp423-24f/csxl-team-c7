import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.model';

@Component({
  selector: 'organization-members-card',
  templateUrl: './organization-members-card.widget.html',
  styleUrls: ['./organization-members-card.widget.css']
})
export class OrganizationMembersCard {
  @Input() organization!: Organization;
  getExpectedGraduation(userId: number): string | null {
    const application = this.organization.applications?.find(
      (app: any) => app.user_id === userId
    );
    return application ? application.expected_graduation : null;
  }
}

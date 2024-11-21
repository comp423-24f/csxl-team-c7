import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.model';

@Component({
  selector: 'organization-members-card',
  templateUrl: './organization-members-card.widget.html',
  styleUrls: ['./organization-members-card.widget.css']
})
export class OrganizationMembersCard {
  @Input() organization!: Organization;
}

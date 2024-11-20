/**
 * The Organization Card widget abstracts the implementation of each
 * individual organization card from the whole organization page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization } from '../../organization.model';
import { Profile } from '../../../profile/profile.service';
import { OrganizationService } from '../../organization.service';

@Component({
  selector: 'organization-card',
  templateUrl: './organization-card.widget.html',
  styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {
  /** The organization to show */
  @Input() organization!: Organization;
  /** The profile of the currently signed in user */
  @Input() profile?: Profile;

  isMember: boolean = false;

  constructor(private organizationService: OrganizationService) {}

  ngOnInit() {
    this.organizationService
      .isMember(this.organization.slug)
      .subscribe((result) => (this.isMember = result));
  }

  join() {
    this.organizationService
      .joinOrganization(this.organization.slug)
      .subscribe(() => (this.isMember = true));
  }

  leave() {
    this.organizationService
      .leaveOrganization(this.organization.slug)
      .subscribe(() => (this.isMember = false));
  }
}

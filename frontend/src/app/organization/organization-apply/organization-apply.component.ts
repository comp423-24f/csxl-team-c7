import { Component } from '@angular/core';
import { Route } from '@angular/router';

@Component({
  selector: 'app-organization-apply',
  templateUrl: './organization-apply.component.html',
  styleUrls: ['./organization-apply.component.css']
})
export class OrganizationApplyComponent {
  static Route: Route = {
    path: ':slug/apply',
    component: OrganizationApplyComponent
  };
}

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { OrganizationService } from '../organization.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  ORGANIZATION_APPLICATION_FORM,
  ApplicationFormField,
  FormFieldType
} from './organization-application-form';

@Component({
  selector: 'app-organization-apply',
  templateUrl: './organization-apply.component.html',
  styleUrls: ['./organization-apply.component.css']
})
export class OrganizationApplyComponent implements OnInit {
  static Route = {
    path: ':slug/apply',
    component: OrganizationApplyComponent,
    title: 'Apply to Organization'
  };

  applicationForm: FormGroup;
  fields: ApplicationFormField[] = ORGANIZATION_APPLICATION_FORM;
  organizationSlug: any;
  organizationName: any;
  submitting = false;
  FormFieldType = FormFieldType;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private organizationService: OrganizationService,
    private snackBar: MatSnackBar
  ) {
    this.applicationForm = this.fb.group({
      interest_statement: ['', [Validators.required, Validators.minLength(50)]],
      experience: ['', [Validators.required]],
      expected_graduation: ['', [Validators.required]],
      program_pursued: ['', [Validators.required]],
      additional_info: ['']
    });
  }

  ngOnInit() {
    this.organizationSlug = this.route.snapshot.params['slug'];
    this.organizationService.getOrganization(this.organizationSlug)
        .subscribe(org => {
            if (org) {
                this.organizationName = org.name;
            }
        });
}

  onSubmit() {
    if (this.applicationForm.valid && !this.submitting) {
      this.submitting = true;
      this.organizationService
        .submitApplication(this.organizationSlug, this.applicationForm.value)
        .subscribe({
          next: () => {
            this.snackBar.open('Application submitted successfully', '', {
              duration: 3000
            });
            this.router.navigate(['/organizations', this.organizationSlug]);
          },
          error: () => {
            this.submitting = false;
            this.snackBar.open('Error submitting application', '', {
              duration: 3000
            });
          }
        });
    }
  }
}

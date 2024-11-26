import { Component, OnInit } from '@angular/core';
import { OrganizationService } from '../organization.service';
import { ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { ApplicationViewDialogComponent } from './application-view-widget/application-view-dialog.widget';
import { ApplicationStatus } from '../organization-application.model';
@Component({
  selector: 'app-organization-application-review',
  templateUrl: './organization-application-review.component.html',
  styleUrls: ['./organization-application-review.component.css']
})
export class OrganizationApplicationReviewComponent implements OnInit {
  applications: any[] = [];
  organizationSlug: any;
  displayedColumns: string[] = [
    'user',
    'interest',
    'experience',
    'expected_graduation',
    'program_pursued',
    'additional_info',
    'status',
    'actions'
  ];

  constructor(
    private route: ActivatedRoute,
    private organizationService: OrganizationService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.organizationSlug = this.route.snapshot.params['slug'];
    this.loadApplications();
  }

  loadApplications() {
    this.organizationService
      .getOrganizationApplications(this.organizationSlug)
      .subscribe((org) => {
        this.applications = org.applications;
      });
  }

  viewApplication(application: any) {
    const dialogRef = this.dialog.open(ApplicationViewDialogComponent, {
      width: '600px',
      data: application
    });
  }

  acceptApplication(application: any) {
    this.organizationService
      .updateApplicationStatus(application.id, ApplicationStatus.APPROVED)
      .subscribe({
        next: () => {
          this.snackBar.open('Application approved', '', { duration: 3000 });
          this.loadApplications();
        },
        error: () => {
          this.snackBar.open('Error approving application', '', {
            duration: 3000
          });
        }
      });
  }

  denyApplication(application: any) {
    this.organizationService
      .updateApplicationStatus(application.id, ApplicationStatus.REJECTED)
      .subscribe({
        next: () => {
          this.snackBar.open('Application rejected', '', { duration: 3000 });
          this.loadApplications();
        },
        error: () => {
          this.snackBar.open('Error rejecting application', '', {
            duration: 3000
          });
        }
      });
  }
}

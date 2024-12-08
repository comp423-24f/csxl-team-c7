import { Component, Input, OnInit } from '@angular/core';
import { OrganizationMessage } from './organization-message.model';
import { OrganizationService } from '../../organization.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PermissionService } from 'src/app/permission.service';
import { Organization } from '../../organization.model';

@Component({
  selector: 'organization-messages',
  templateUrl: './organization-messages.widget.html',
  styleUrls: ['./organization-messages.widget.css']
})
export class OrganizationMessagesWidget implements OnInit {
  @Input() organization!: Organization;
  isAdmin = false;
  newMessage = '';
  isMember = false;
  editingMessage: OrganizationMessage | null = null;

  constructor(
    private organizationService: OrganizationService,
    private permissionService: PermissionService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.checkPermissions();
    this.checkMembership();
  }

  checkPermissions() {
    this.isAdmin = this.permissionService.checkSignal(
      'organization.*',
      `organization/${this.organization.slug}`
    );
  }
  checkMembership() {
    this.organizationService
      .isMember(this.organization.slug)
      .subscribe((isMember) => {
        this.isMember = isMember;
      });
  }

  sendMessage() {
    if (this.newMessage?.trim()) {
      this.organizationService
        .createMessage(this.organization.slug, this.newMessage.trim())
        .subscribe({
          next: () => {
            this.snackBar.open('Message posted', '', { duration: 3000 });
            this.newMessage = '';
            this.refreshOrganization();
          },
          error: () => {
            this.snackBar.open('Error posting message', '', { duration: 3000 });
          }
        });
    }
  }

  editMessage(message: OrganizationMessage) {
    this.editingMessage = { ...message };
  }

  saveEdit() {
    if (this.editingMessage) {
      this.organizationService
        .updateMessage(this.editingMessage.id!, this.editingMessage.content)
        .subscribe({
          next: () => {
            this.snackBar.open('Message updated', '', { duration: 3000 });
            this.editingMessage = null;
            this.refreshOrganization();
          },
          error: () => {
            this.snackBar.open('Error updating message', '', {
              duration: 3000
            });
          }
        });
    }
  }

  cancelEdit() {
    this.editingMessage = null;
  }

  deleteMessage(message: OrganizationMessage) {
    const confirmation = confirm(
      'Are you sure you want to delete this message?'
    );
    if (confirmation) {
      this.organizationService.deleteMessage(message.id!).subscribe({
        next: () => {
          this.snackBar.open('Message deleted', '', { duration: 3000 });
          this.refreshOrganization();
        },
        error: () => {
          this.snackBar.open('Error deleting message', '', { duration: 3000 });
        }
      });
    }
  }

  private refreshOrganization() {
    this.organizationService
      .getOrganization(this.organization.slug)
      .subscribe((org) => {
        if (org) {
          this.organization = org;
        }
      });
  }
}

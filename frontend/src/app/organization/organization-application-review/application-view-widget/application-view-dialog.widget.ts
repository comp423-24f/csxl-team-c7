import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-application-view-dialog',
  templateUrl: './application-view-dialog.widget.html',
  styleUrls: ['./application-view-dialog.widget.css']
})
export class ApplicationViewDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ApplicationViewDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}
}

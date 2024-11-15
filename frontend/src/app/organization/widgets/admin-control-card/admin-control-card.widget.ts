import { Component, Input } from '@angular/core';
import { SharedModule } from '../../../shared/shared.module';

@Component({
  selector: 'admin-control-card',
  templateUrl: './admin-control-card.widget.html',
  styleUrls: ['./admin-control-card.widget.css'],
  imports: [SharedModule],
  standalone: true
})
export class AdminControlCard {
  //TODO: Functionality

  constructor() {}
}

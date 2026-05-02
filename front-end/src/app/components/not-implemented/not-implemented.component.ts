import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-not-implemented',
  standalone: false,
  templateUrl: './not-implemented.component.html',
  styleUrl: './not-implemented.component.css'
})
export class NotImplementedComponent {
  pageTitle = '';

  constructor(private readonly route: ActivatedRoute) {
    this.pageTitle = this.route.snapshot.data['title'] ?? '';
  }
}

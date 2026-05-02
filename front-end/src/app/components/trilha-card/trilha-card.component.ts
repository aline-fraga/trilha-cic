import { Component, Input } from '@angular/core';
import { Trilha } from '../../models/trilha';

@Component({
  selector: 'app-trilha-card',
  standalone: false,
  templateUrl: './trilha-card.component.html',
  styleUrl: './trilha-card.component.css'
})
export class TrilhaCardComponent {
  @Input({ required: true }) trilha!: Trilha;
  isExpanded = false;

  toggleDisciplinas(): void {
    this.isExpanded = !this.isExpanded;
  }
}

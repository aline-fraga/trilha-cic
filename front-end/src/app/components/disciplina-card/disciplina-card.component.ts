import { Component, Input } from '@angular/core';
import { Disciplina } from '../../models/trilha';

@Component({
  selector: 'app-disciplina-card',
  standalone: false,
  templateUrl: './disciplina-card.component.html',
  styleUrl: './disciplina-card.component.css'
})
export class DisciplinaCardComponent {
  @Input({ required: true }) disciplina!: Disciplina;
}

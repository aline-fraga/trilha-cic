import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
  readonly aluno = {
    nome: 'Pedro Emilio Diello Kuhn',
    matricula: '00323638'
  };

  readonly navigationItems = [
    { label: 'Ver trilhas disponíveis', route: '/trilhas' },
    { label: 'Solicitar trilhas', route: '/solicitar-trilhas' },
    { label: 'Sugerir novas trilhas', route: '/sugerir-trilhas' },
    { label: 'Abrir chamado com a COMGRAD', route: '/chamado-comgrad' },
    { label: 'Área da COMGRAD', route: '/comgrad/painel' }
  ];
}

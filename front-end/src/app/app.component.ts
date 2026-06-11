import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';
import { UserInfo } from './models/auth';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  currentUser: UserInfo | null = null;

  private readonly allNavigationItems = [
    { label: 'Ver trilhas disponíveis', route: '/trilhas', roles: ['ALUNO', 'COMGRAD', 'ADMIN'] },
    { label: 'Solicitar trilhas', route: '/solicitar-trilhas', roles: ['ALUNO'] },
    { label: 'Abrir chamado com a COMGRAD', route: '/chamado-comgrad', roles: ['ALUNO'] },
    { label: 'Gerenciar currículo', route: '/curriculo', roles: ['COMGRAD'] },
    { label: 'Gerenciar trilhas', route: '/gerenciar-trilhas', roles: ['COMGRAD'] },
    { label: 'Chamados', route: '/comgrad/painel', roles: ['COMGRAD', 'ADMIN'] },
    { label: 'Relatórios', route: '/relatorios', roles: ['COMGRAD', 'ADMIN'] },
  ];

  get navigationItems() {
    const role = this.currentUser?.role;
    if (!role) return [];
    return this.allNavigationItems.filter(item => item.roles.includes(role));
  }

  constructor(
    readonly authService: AuthService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe((user) => (this.currentUser = user));
    this.authService.loadCurrentUser();
  }

  logout(): void {
    this.authService.logout();
  }

  get isLoginPage(): boolean {
    return this.router.url === '/login';
  }
}

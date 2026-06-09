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

  readonly navigationItems = [
    { label: 'Ver trilhas disponíveis', route: '/trilhas' },
    { label: 'Solicitar trilhas', route: '/solicitar-trilhas' },
    { label: 'Sugerir novas trilhas', route: '/sugerir-trilhas' },
    { label: 'Abrir chamado com a COMGRAD', route: '/chamado-comgrad' },
  ];

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

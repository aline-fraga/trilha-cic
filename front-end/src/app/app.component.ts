import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';
import { UserInfo } from './models/auth';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('topbar') topbarRef?: ElementRef<HTMLElement>;

  currentUser: UserInfo | null = null;
  private resizeObserver?: ResizeObserver;

  private readonly allNavigationItems = [
    { label: 'Ver trilhas disponíveis', route: '/trilhas', roles: ['ALUNO', 'COMGRAD', 'ADMIN'] },
    { label: 'Currículo Vigente', route: '/curriculo-vigente', roles: ['ALUNO', 'COMGRAD', 'ADMIN'] },
    { label: 'Solicitar trilhas', route: '/solicitar-trilhas', roles: ['ALUNO'] },
    { label: 'Sugerir nova trilha', route: '/sugerir-trilhas', roles: ['ALUNO'] },
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

  ngAfterViewInit(): void {
    this.atualizarAlturaTopbar();

    if (typeof ResizeObserver !== 'undefined' && this.topbarRef?.nativeElement) {
      this.resizeObserver = new ResizeObserver(() => this.atualizarAlturaTopbar());
      this.resizeObserver.observe(this.topbarRef.nativeElement);
    }
  }

  ngOnDestroy(): void {
    this.resizeObserver?.disconnect();
  }

  private atualizarAlturaTopbar(): void {
    const altura = this.topbarRef?.nativeElement.offsetHeight ?? 92;
    document.documentElement.style.setProperty('--topbar-height', `${altura}px`);
  }
}

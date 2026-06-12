import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { LoginRequest, TokenResponse, UserInfo } from '../models/auth';

const TOKEN_KEY = 'auth_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly loginUrl = '/auth/login';
  private readonly meUrl = '/auth/me';

  currentUser$ = new BehaviorSubject<UserInfo | null>(null);

  constructor(private readonly http: HttpClient, private readonly router: Router) {}

  login(email: string, password: string): Observable<TokenResponse> {
    const body: LoginRequest = { email, password };
    return this.http.post<TokenResponse>(this.loginUrl, body).pipe(
      tap((res) => {
        localStorage.setItem(TOKEN_KEY, res.access_token);
        this.loadCurrentUser();
      })
    );
  }

  loadCurrentUser(): void {
    if (!this.getToken()) return;
    this.http.get<UserInfo>(this.meUrl).subscribe({
      next: (user) => this.currentUser$.next(user),
      error: () => this.logout(),
    });
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    this.currentUser$.next(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}

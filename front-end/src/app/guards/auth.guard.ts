import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable, filter, map, take } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private readonly authService: AuthService, private readonly router: Router) {}

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean> | boolean {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return false;
    }

    const expectedRoles = route.data['roles'] as Array<string>;
    if (!expectedRoles || expectedRoles.length === 0) {
      return true;
    }

    return this.authService.currentUser$.pipe(
      filter(user => !!user),
      take(1),
      map(user => {
        if (expectedRoles.includes(user!.role)) {
          return true;
        } else {
          this.router.navigate(['/trilhas']);
          return false;
        }
      })
    );
  }
}

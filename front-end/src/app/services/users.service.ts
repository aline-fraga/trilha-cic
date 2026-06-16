import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  UserAdminResponse,
  UserCreate,
  UserRole,
  UserUpdate,
} from '../models/user';

@Injectable({ providedIn: 'root' })
export class UsersService {
  private readonly url = '/users';

  constructor(private readonly http: HttpClient) {}

  listar(filters?: {
    role?: UserRole | '';
    is_active?: boolean | '';
  }): Observable<UserAdminResponse[]> {
    let params = new HttpParams();

    if (filters?.role) {
      params = params.set('role', filters.role);
    }

    if (filters?.is_active !== '' && filters?.is_active !== undefined) {
      params = params.set('is_active', String(filters.is_active));
    }

    return this.http.get<UserAdminResponse[]>(`${this.url}/get`, { params });
  }

  criar(payload: UserCreate): Observable<UserAdminResponse> {
    return this.http.post<UserAdminResponse>(`${this.url}/create`, payload);
  }

  atualizar(userId: number, payload: UserUpdate): Observable<UserAdminResponse> {
    return this.http.patch<UserAdminResponse>(`${this.url}/update/${userId}`, payload);
  }

  excluir(userId: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/delete/${userId}`);
  }
}

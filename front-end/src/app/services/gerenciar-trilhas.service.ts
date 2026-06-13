import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Trilha } from '../models/trilha';

export interface TrilhaCreate {
  nome: string;
  resumo: string;
  disciplinas_ids: number[];
}

export interface TrilhaUpdate {
  nome?: string;
  resumo?: string;
  disciplinas_ids?: number[];
}

@Injectable({ providedIn: 'root' })
export class GerenciarTrilhasService {
  private readonly url = '/trilhas';

  constructor(private readonly http: HttpClient) {}

  listar(): Observable<Trilha[]> {
    return this.http.get<Trilha[]>(`${this.url}/get`);
  }

  criar(data: TrilhaCreate): Observable<Trilha> {
    return this.http.post<Trilha>(`${this.url}/create`, data);
  }

  atualizar(id: number, data: TrilhaUpdate): Observable<Trilha> {
    return this.http.patch<Trilha>(`${this.url}/update/${id}`, data);
  }

  excluir(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/delete/${id}`);
  }
}

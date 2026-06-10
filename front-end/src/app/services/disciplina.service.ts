import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Disciplina, DisciplinaCreate, DisciplinaUpdate } from '../models/disciplina';

@Injectable({ providedIn: 'root' })
export class DisciplinaService {
  private readonly url = '/disciplinas';

  constructor(private readonly http: HttpClient) {}

  listar(): Observable<Disciplina[]> {
    return this.http.get<Disciplina[]>(this.url);
  }

  criar(data: DisciplinaCreate): Observable<Disciplina> {
    return this.http.post<Disciplina>(this.url, data);
  }

  atualizar(id: number, data: DisciplinaUpdate): Observable<Disciplina> {
    return this.http.put<Disciplina>(`${this.url}/${id}`, data);
  }

  excluir(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}

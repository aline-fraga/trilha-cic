import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Disciplina, DisciplinaCreate, DisciplinaUpdate } from '../models/disciplina';

@Injectable({ providedIn: 'root' })
export class DisciplinaService {
  private readonly url = '/disciplinas';

  constructor(private readonly http: HttpClient) {}

  listar(isActive?: boolean): Observable<Disciplina[]> {
    let params = new HttpParams();
    if (isActive !== undefined) {
      params = params.set('is_active', isActive);
    }
    return this.http.get<Disciplina[]>(`${this.url}/get`, { params });
  }

  criar(data: DisciplinaCreate): Observable<Disciplina> {
    return this.http.post<Disciplina>(`${this.url}/create`, data);
  }

  atualizar(id: number, data: DisciplinaUpdate): Observable<Disciplina> {
    return this.http.put<Disciplina>(`${this.url}/update/${id}`, data);
  }

  excluir(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/delete/${id}`);
  }
}

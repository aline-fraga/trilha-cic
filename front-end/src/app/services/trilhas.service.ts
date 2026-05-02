import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Trilha } from '../models/trilha';
import { TRILHAS_MOCK } from '../mocks/trilhas.mock';

@Injectable({
  providedIn: 'root'
})
export class TrilhasService {
  private readonly useMockData = true;
  private readonly trilhasUrl = 'trilhas/get';

  constructor(private readonly http: HttpClient) {}

  getTrilhas(): Observable<Trilha[]> {
    if (this.useMockData) {
      return this.getMockTrilhas();
    }

    return this.http.get<Trilha[]>(this.trilhasUrl);
  }

  searchTrilhasByDisciplina(disciplina: string): Observable<Trilha[]> {
    const params = new HttpParams().set('disciplina', disciplina.trim());

    if (this.useMockData) {
      return this.getMockTrilhas(disciplina);
    }

    return this.http.get<Trilha[]>(this.trilhasUrl, { params });
  }

  private getMockTrilhas(disciplina?: string): Observable<Trilha[]> {
    if (!disciplina?.trim()) {
      return of(TRILHAS_MOCK);
    }

    const filtro = disciplina.trim().toLowerCase();
    const trilhasFiltradas = TRILHAS_MOCK.filter((trilha) =>
      trilha.disciplinas.some((disciplinaItem) =>
        disciplinaItem.nome.toLowerCase().includes(filtro)
      )
    );

    return of(trilhasFiltradas);
  }
}

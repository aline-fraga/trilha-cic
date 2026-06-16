import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Relatorio, RelatorioCreateRequest } from '../models/relatorio';

@Injectable({ providedIn: 'root' })
export class RelatoriosService {
  private readonly url = '/relatorios';

  constructor(private readonly http: HttpClient) {}

  listar(): Observable<Relatorio[]> {
    return this.http.get<Relatorio[]>(`${this.url}/get`);
  }

  obter(relatorioId: number): Observable<Relatorio> {
    return this.http.get<Relatorio>(`${this.url}/get/${relatorioId}`);
  }

  criar(payload: RelatorioCreateRequest): Observable<Relatorio> {
    return this.http.post<Relatorio>(`${this.url}/create`, payload);
  }

  baixarPdf(relatorioId: number): Observable<Blob> {
    return this.http.get(`${this.url}/get/${relatorioId}/pdf`, {
      responseType: 'blob',
    });
  }
}

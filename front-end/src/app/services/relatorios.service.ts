import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TrilhaBrief {
  id: number;
  nome: string;
}

export interface RelatorioItem {
  trilha_id: number;
  aceites: number;
  rejeicoes: number;
  trilha: TrilhaBrief;
}

export interface RelatorioResponse {
  id: number;
  gerado_por_id: number;
  periodo_inicio: string;
  periodo_fim: string;
  total_solicitacoes: number;
  total_aceites: number;
  total_rejeicoes: number;
  created_at: string;
  itens: RelatorioItem[];
}

export interface RelatorioCreate {
  periodo_inicio: string;
  periodo_fim: string;
}

@Injectable({
  providedIn: 'root'
})
export class RelatoriosService {
  private readonly baseUrl = 'relatorios';

  constructor(private http: HttpClient) {}

  listarRelatorios(): Observable<RelatorioResponse[]> {
    return this.http.get<RelatorioResponse[]>(`${this.baseUrl}/get`);
  }

  obterRelatorio(id: number): Observable<RelatorioResponse> {
    return this.http.get<RelatorioResponse>(`${this.baseUrl}/get/${id}`);
  }

  gerarRelatorio(payload: RelatorioCreate): Observable<RelatorioResponse> {
    return this.http.post<RelatorioResponse>(`${this.baseUrl}/create`, payload);
  }

  baixarPdf(id: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/get/${id}/pdf`, {
      responseType: 'blob'
    });
  }
}

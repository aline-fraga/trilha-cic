import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  SolicitarTrilhaRequest,
  SolicitarTrilhaResponse,
} from '../models/solicitacao';

@Injectable({ providedIn: 'root' })
export class SolicitacoesService {
  private readonly url = '/solicitacoes';

  constructor(private readonly http: HttpClient) {}

  listar(status?: 'PENDENTE' | 'ACEITA' | 'REJEITADA'): Observable<SolicitarTrilhaResponse[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set('status', status);
    }
    return this.http.get<SolicitarTrilhaResponse[]>(`${this.url}/get`, { params });
  }

  criar(payload: SolicitarTrilhaRequest): Observable<SolicitarTrilhaResponse> {
    return this.http.post<SolicitarTrilhaResponse>(`${this.url}/create`, payload);
  }

  aceitar(solicitacaoId: number, trilhaId: number): Observable<SolicitarTrilhaResponse> {
    return this.http.patch<SolicitarTrilhaResponse>(
      `${this.url}/aceitar/${solicitacaoId}`,
      { trilha_id: trilhaId }
    );
  }

  rejeitar(solicitacaoId: number): Observable<SolicitarTrilhaResponse> {
    return this.http.patch<SolicitarTrilhaResponse>(
      `${this.url}/rejeitar/${solicitacaoId}`,
      {}
    );
  }

  baixarMaterial(solicitacaoId: number): Observable<Blob> {
    return this.http.get(`${this.url}/material/${solicitacaoId}`, {
      responseType: 'blob',
    });
  }
}

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Chamado {
  id: number;
  aluno_id: number;
  aluno_nome?: string;
  tipo: string;
  assunto: string;
  mensagem: string;
  status: string;
  resposta?: string;
  respondido_em?: string;
  trilha_id?: number;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChamadoService {
  private apiUrl = '/chamados';

  constructor(private http: HttpClient) {}

  getChamados(status?: string): Observable<Chamado[]> {
    let params = new HttpParams();
    if (status) {
      params = params.set('status', status);
    }
    return this.http.get<Chamado[]>(this.apiUrl, { params });
  }

  criarChamado(dados: { assunto: string; mensagem: string; tipo: string }): Observable<Chamado> {
    return this.http.post<Chamado>(this.apiUrl, dados);
  }

  responderChamado(id: number, resposta: string): Observable<Chamado> {
    return this.http.put<Chamado>(`${this.apiUrl}/${id}/responder`, { resposta });
  }
}

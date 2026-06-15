import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Pergunta } from '../models/pergunta';

@Injectable({ providedIn: 'root' })
export class PerguntasService {
  private readonly url = '/perguntas/get';

  constructor(private readonly http: HttpClient) {}

  listar(isActive?: boolean): Observable<Pergunta[]> {
    let params = new HttpParams();
    if (isActive !== undefined) {
      params = params.set('is_active', isActive);
    }
    return this.http.get<Pergunta[]>(this.url, { params });
  }
}

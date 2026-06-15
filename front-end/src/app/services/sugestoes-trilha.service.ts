import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  SugestaoTrilhaCreate,
  SugestaoTrilhaResponse,
} from '../models/sugestao-trilha';

@Injectable({ providedIn: 'root' })
export class SugestoesTrilhaService {
  private readonly url = '/sugestoes-trilha';

  constructor(private readonly http: HttpClient) {}

  listar(): Observable<SugestaoTrilhaResponse[]> {
    return this.http.get<SugestaoTrilhaResponse[]>(`${this.url}/get`);
  }

  criar(data: SugestaoTrilhaCreate): Observable<SugestaoTrilhaResponse> {
    return this.http.post<SugestaoTrilhaResponse>(`${this.url}/create`, data);
  }
}

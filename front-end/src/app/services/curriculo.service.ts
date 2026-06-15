import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Curriculo } from '../models/curriculo';

@Injectable({ providedIn: 'root' })
export class CurriculoService {
  private readonly url = '/curriculos';

  constructor(private readonly http: HttpClient) {}

  listar(isActive?: boolean): Observable<Curriculo[]> {
    let params = new HttpParams();
    if (isActive !== undefined) {
      params = params.set('is_active', isActive);
    }
    return this.http.get<Curriculo[]>(`${this.url}/get`, { params });
  }
}

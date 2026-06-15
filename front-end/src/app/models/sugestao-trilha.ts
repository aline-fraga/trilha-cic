import { Chamado } from '../services/chamado.service';
import { Disciplina } from './disciplina';

export interface SugestaoTrilhaCreate {
  nome: string;
  disciplinas_ids: number[];
}

export interface SugestaoTrilhaResponse {
  id: number;
  nome_proposto: string;
  aluno_id: number;
  aluno_nome: string;
  chamado: Chamado;
  disciplinas: Disciplina[];
  created_at: string;
}

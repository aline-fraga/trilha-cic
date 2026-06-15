import { Disciplina } from './disciplina';

export interface Curriculo {
  id: number;
  curso: string;
  codigo: string;
  ano_vigencia: number;
  is_active: boolean;
  disciplinas: Disciplina[];
}

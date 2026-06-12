export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  carga_horaria: number;
  is_active: boolean;
}

export interface DisciplinaCreate {
  nome: string;
  codigo: string;
  carga_horaria: number;
}

export interface DisciplinaUpdate {
  nome?: string;
  codigo?: string;
  carga_horaria?: number;
}

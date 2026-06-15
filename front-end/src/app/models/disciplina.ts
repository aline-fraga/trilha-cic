export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  tipo: 'OBRIGATORIA' | 'ELETIVA';
  carga_horaria: number;
  link_plano_ensino?: string | null;
  is_active: boolean;
}

export interface DisciplinaCreate {
  nome: string;
  codigo: string;
  tipo?: 'OBRIGATORIA' | 'ELETIVA';
  carga_horaria: number;
  link_plano_ensino?: string | null;
}

export interface DisciplinaUpdate {
  nome?: string;
  codigo?: string;
  tipo?: 'OBRIGATORIA' | 'ELETIVA';
  carga_horaria?: number;
  link_plano_ensino?: string | null;
}

export type DisciplinaTipo = 'OBRIGATORIA' | 'ELETIVA';

export interface DisciplinaPrerequisito {
  id: number;
  nome: string;
  codigo: string;
}

export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  tipo: DisciplinaTipo;
  carga_horaria: number;
  link_plano_ensino: string | null;
  is_active: boolean;
  prerequisitos: DisciplinaPrerequisito[];
}

export interface DisciplinaCreate {
  nome: string;
  codigo: string;
  tipo: DisciplinaTipo;
  carga_horaria: number;
  link_plano_ensino?: string;
  prerequisito_ids: number[];
}

export interface DisciplinaUpdate {
  nome?: string;
  codigo?: string;
  tipo?: DisciplinaTipo;
  carga_horaria?: number;
  link_plano_ensino?: string;
  prerequisito_ids?: number[];
}

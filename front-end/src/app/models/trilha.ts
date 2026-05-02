export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  tipo: string;
  carga_horaria: number;
  link_plano_ensino: string;
}

export interface Trilha {
  id: number;
  nome: string;
  resumo: string;
  disciplinas: Disciplina[];
}

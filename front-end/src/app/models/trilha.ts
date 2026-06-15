export interface Disciplina {
  id: number;
  nome: string;
  codigo: string;
  carga_horaria: number;
}

export interface PesoPergunta {
  pergunta_id: number;
  peso: number;
}

export interface Trilha {
  id: number;
  nome: string;
  resumo: string;
  disciplinas: Disciplina[];
  pesos?: PesoPergunta[];
}

export interface TrilhaBrief {
  id: number;
  nome: string;
}

export interface RelatorioItem {
  trilha_id: number;
  aceites: number;
  rejeicoes: number;
  trilha: TrilhaBrief;
}

export interface Relatorio {
  id: number;
  gerado_por_id: number;
  periodo_inicio: string;
  periodo_fim: string;
  total_solicitacoes: number;
  total_aceites: number;
  total_rejeicoes: number;
  created_at: string;
  itens: RelatorioItem[];
}

export interface RelatorioCreateRequest {
  periodo_inicio: string;
  periodo_fim: string;
}

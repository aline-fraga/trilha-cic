import { Chamado } from '../services/chamado.service';
import { Trilha } from './trilha';

export interface RespostaPerguntaInput {
  pergunta_id: number;
  valor: number;
}

export interface SolicitarTrilhaRequest {
  respostas: RespostaPerguntaInput[];
}

export interface SolicitarTrilhaResponse {
  id: number;
  aluno_id: number;
  aluno_nome: string;
  trilhas_candidatas: Trilha[];
  trilha_aceita: Trilha | null;
  chamado: Chamado | null;
  status: 'PENDENTE' | 'ACEITA' | 'REJEITADA';
  created_at: string;
  resolvido_em: string | null;
}

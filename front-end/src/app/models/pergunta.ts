export interface Pergunta {
  id: number;
  enunciado: string;
  tipo: 'CONCEITUAL' | 'PRATICA';
  ordem: number;
  is_active: boolean;
}

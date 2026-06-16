export type UserRole = 'ALUNO' | 'COMGRAD' | 'ADMIN';

export interface AlunoData {
  cartao_ufrgs: string;
  semestre_ingresso: string;
}

export interface UserAdminResponse {
  id: number;
  email: string;
  nome: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  aluno?: AlunoData | null;
}

export interface UserCreate {
  email: string;
  nome: string;
  password: string;
  role: UserRole;
  aluno?: AlunoData | null;
}

export interface UserUpdate {
  email?: string;
  nome?: string;
  is_active?: boolean;
  aluno?: AlunoData | null;
}

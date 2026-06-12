export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserInfo {
  id: number;
  nome: string;
  email: string;
  role: 'ALUNO' | 'COMGRAD' | 'ADMIN';
  cartao_ufrgs?: string;
}

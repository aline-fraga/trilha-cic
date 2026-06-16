import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ChamadoService, Chamado } from '../../services/chamado.service';

@Component({
  selector: 'app-chamado-comgrad',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chamado-comgrad.component.html',
  styleUrls: ['./chamado-comgrad.component.css']
})
export class ChamadoComgradComponent implements OnInit {
  visaoAtual: 'lista' | 'novo' | 'detalhes' = 'lista';
  chamados: Chamado[] = [];
  chamadoSelecionado: Chamado | null = null;
  isLoading = true;

  novoChamado = {
    assunto: 'Revisão de Trilha Sugerida',
    mensagem: '',
    tipo: 'TRILHA_REJEITADA'
  };

  isSubmitting = false;
  successMessage = '';
  errorMessage = '';

  // RNF #12: o comentário do chamado deve ter entre 50 e 2000 caracteres.
  readonly comentarioMin = 50;
  readonly comentarioMax = 2000;

  get mensagemValida(): boolean {
    const tamanho = this.novoChamado.mensagem.trim().length;
    return tamanho >= this.comentarioMin && tamanho <= this.comentarioMax;
  }

  constructor(
    private chamadoService: ChamadoService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.carregarChamados();
  }

  carregarChamados(): void {
    this.isLoading = true;
    this.chamadoService.getChamados().subscribe({
      next: (data) => {
        this.chamados = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error(err);
        this.isLoading = false;
      }
    });
  }

  get podeAbrirChamado(): boolean {
    return !this.chamados.some(c => c.status === 'ABERTO');
  }

  abrirFormulario(): void {
    if (this.podeAbrirChamado) {
      this.visaoAtual = 'novo';
      this.successMessage = '';
      this.errorMessage = '';
    }
  }

  verDetalhes(chamado: Chamado): void {
    this.chamadoSelecionado = chamado;
    this.visaoAtual = 'detalhes';
  }

  voltarParaLista(): void {
    this.visaoAtual = 'lista';
    this.chamadoSelecionado = null;
    this.successMessage = '';
    this.errorMessage = '';
  }

  submitChamado(): void {
    if (!this.novoChamado.assunto.trim()) {
      this.errorMessage = 'Por favor, preencha o título do chamado.';
      return;
    }
    if (!this.mensagemValida) {
      this.errorMessage =
        `O comentário deve ter entre ${this.comentarioMin} e ${this.comentarioMax} caracteres.`;
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';
    
    this.chamadoService.criarChamado(this.novoChamado).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.successMessage = 'Chamado enviado com sucesso! A COMGRAD analisará sua solicitação em breve.';
        this.novoChamado = { assunto: 'Revisão de Trilha Sugerida', mensagem: '', tipo: 'TRILHA_REJEITADA' };
        this.carregarChamados();
        setTimeout(() => {
          this.voltarParaLista();
        }, 3000);
      },
      error: (err) => {
        this.isSubmitting = false;
        console.error(err);
        this.errorMessage = err.error?.detail || 'Erro ao conectar com o servidor. Tente novamente mais tarde.';
      }
    });
  }

  voltarParaTrilhas(): void {
    this.router.navigate(['/trilhas']);
  }
}

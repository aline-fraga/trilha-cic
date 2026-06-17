import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChamadoService, Chamado } from '../../services/chamado.service';

@Component({
  selector: 'app-comgrad-painel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comgrad-painel.component.html',
  styleUrl: './comgrad-painel.component.css'
})
export class ComgradPainelComponent implements OnInit {
  chamados: Chamado[] = [];
  isLoading = true;

  chamadoSelecionado: Chamado | null = null;
  respostaTexto = '';
  erroResposta = '';
  isSubmitting = false;

  termoBusca: string = '';
  filtroStatus: 'TODOS' | 'ABERTO' | 'FECHADO' = 'TODOS';
  ordenacao: 'RECENTES' | 'ANTIGOS' = 'RECENTES';

  constructor(private chamadoService: ChamadoService) {}

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

  get chamadosFiltrados(): Chamado[] {
    return this.aplicarFiltros(this.chamados);
  }

  private aplicarFiltros(lista: Chamado[]): Chamado[] {
    let filtrada = lista.filter(c => {
      if (this.filtroStatus !== 'TODOS' && c.status !== this.filtroStatus) {
        return false;
      }
      
      if (this.termoBusca.trim()) {
        const termo = this.termoBusca.toLowerCase();
        const assunto = c.assunto.toLowerCase();
        const email = c.aluno_nome?.toLowerCase() || '';
        
        if (!assunto.includes(termo) && !email.includes(termo)) {
          return false;
        }
      }
      
      return true;
    });

    filtrada.sort((a, b) => {
      const dataA = new Date(a.created_at).getTime();
      const dataB = new Date(b.created_at).getTime();
      return this.ordenacao === 'RECENTES' ? dataB - dataA : dataA - dataB;
    });

    return filtrada;
  }



  selecionarChamado(chamado: Chamado): void {
    this.chamadoSelecionado = chamado;
    this.respostaTexto = '';
    this.erroResposta = '';
  }

  voltarParaLista(): void {
    this.chamadoSelecionado = null;
    this.respostaTexto = '';
    this.erroResposta = '';
  }

  enviarResposta(): void {
    if (!this.chamadoSelecionado) return;

    const resposta = this.respostaTexto.trim();
    if (!resposta) {
      this.erroResposta = 'Informe uma mensagem antes de encerrar o chamado.';
      return;
    }

    this.erroResposta = '';
    this.isSubmitting = true;

    this.chamadoService
      .responderChamado(this.chamadoSelecionado.id, resposta)
      .subscribe({
      next: () => {
        this.isSubmitting = false;
        this.carregarChamados();
        this.voltarParaLista();
      },
      error: (err) => {
        console.error(err);
        this.isSubmitting = false;
        alert('Erro ao enviar a resposta. Tente novamente.');
      }
    });
  }
}

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
  abaAtual: 'responder' | 'sugestoes' | 'cadeiras' | 'curriculo' = 'responder';
  
  chamados: Chamado[] = [];
  isLoading = true;
  
  chamadoSelecionado: Chamado | null = null;
  respostaTexto: string = '';
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

  mudarAba(aba: 'responder' | 'sugestoes' | 'cadeiras' | 'curriculo'): void {
    this.abaAtual = aba;
    this.chamadoSelecionado = null;
    this.respostaTexto = '';
    this.termoBusca = '';
    this.filtroStatus = 'TODOS';
    this.ordenacao = 'RECENTES';
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

  get chamadosResponder(): Chamado[] {
    const base = this.chamados.filter(c => c.tipo !== 'NOVA_TRILHA');
    return this.aplicarFiltros(base);
  }

  get chamadosSugestoes(): Chamado[] {
    const base = this.chamados.filter(c => c.tipo === 'NOVA_TRILHA');
    return this.aplicarFiltros(base);
  }

  selecionarChamado(chamado: Chamado): void {
    this.chamadoSelecionado = chamado;
    this.respostaTexto = '';
  }

  voltarParaLista(): void {
    this.chamadoSelecionado = null;
    this.respostaTexto = '';
  }

  enviarResposta(): void {
    if (!this.chamadoSelecionado || !this.respostaTexto.trim()) return;

    this.isSubmitting = true;
    this.chamadoService.responderChamado(this.chamadoSelecionado.id, this.respostaTexto).subscribe({
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

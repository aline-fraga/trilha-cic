import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { Pergunta } from '../../models/pergunta';
import { SolicitarTrilhaResponse } from '../../models/solicitacao';
import { Trilha } from '../../models/trilha';
import { ChamadoService } from '../../services/chamado.service';
import { PerguntasService } from '../../services/perguntas.service';
import { SolicitacoesService } from '../../services/solicitacoes.service';

@Component({
  selector: 'app-solicitar-trilhas',
  standalone: false,
  templateUrl: './solicitar-trilhas.component.html',
  styleUrl: './solicitar-trilhas.component.css',
})
export class SolicitarTrilhasComponent implements OnInit {
  perguntas: Pergunta[] = [];
  solicitacoes: SolicitarTrilhaResponse[] = [];
  form!: FormGroup;

  carregando = true;
  enviando = false;
  processandoAcaoId: number | null = null;
  baixandoMaterialId: number | null = null;
  salvandoChamadoId: number | null = null;
  erroGeral = '';
  mensagemSucesso = '';
  errosChamado: Record<number, string> = {};
  mensagensChamado: Record<number, string> = {};
  editorChamadoAberto: Record<number, boolean> = {};

  readonly escalaResposta = [
    { valor: 0, label: '0' },
    { valor: 1, label: '1' },
    { valor: 2, label: '2' },
    { valor: 3, label: '3' },
    { valor: 4, label: '4' },
    { valor: 5, label: '5' },
  ];

  constructor(
    private readonly fb: FormBuilder,
    private readonly chamadoService: ChamadoService,
    private readonly perguntasService: PerguntasService,
    private readonly solicitacoesService: SolicitacoesService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarPagina();
  }

  get respostasArray(): FormArray {
    return this.form.get('respostas') as FormArray;
  }

  get solicitacaoPendente(): SolicitarTrilhaResponse | null {
    return this.solicitacoes.find((item) => item.status === 'PENDENTE') ?? null;
  }

  get solicitacaoAceita(): SolicitarTrilhaResponse | null {
    return this.solicitacoes.find((item) => item.status === 'ACEITA') ?? null;
  }

  get chamadoTrilhaRejeitadaAberto(): SolicitarTrilhaResponse | null {
    return (
      this.solicitacoes.find(
        (item) =>
          item.chamado?.status === 'ABERTO' &&
          item.chamado?.tipo === 'TRILHA_REJEITADA'
      ) ?? null
    );
  }

  get podeEnviarNovaSolicitacao(): boolean {
    return (
      !this.solicitacaoPendente &&
      !this.solicitacaoAceita &&
      !this.chamadoTrilhaRejeitadaAberto
    );
  }

  get questionarioBloqueado(): boolean {
    return (
      !!this.solicitacaoPendente ||
      !!this.solicitacaoAceita ||
      !!this.chamadoTrilhaRejeitadaAberto
    );
  }

  private inicializarForm(): void {
    this.form = this.fb.group({
      respostas: this.fb.array([]),
    });
  }

  private carregarPagina(): void {
    this.carregando = true;
    this.erroGeral = '';

    forkJoin({
      perguntas: this.perguntasService.listar(true),
      solicitacoes: this.solicitacoesService.listar(),
    }).subscribe({
      next: ({ perguntas, solicitacoes }) => {
        this.perguntas = [...perguntas].sort(
          (a, b) => a.ordem - b.ordem || a.id - b.id
        );
        this.solicitacoes = [...solicitacoes].sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        this.sincronizarMensagensChamado();
        this.reconstruirRespostas();
        this.carregando = false;
      },
      error: (err) => {
        console.error(err);
        this.carregando = false;
        this.erroGeral = 'Não foi possível carregar os dados da solicitação.';
      },
    });
  }

  private reconstruirRespostas(): void {
    this.respostasArray.clear();
    this.perguntas.forEach(() => {
      this.respostasArray.push(this.fb.control(null, Validators.required));
    });
  }

  selecionarResposta(index: number, valor: number): void {
    if (this.questionarioBloqueado) {
      return;
    }
    this.respostasArray.at(index).setValue(valor);
    this.respostasArray.at(index).markAsTouched();
  }

  respostaSelecionada(index: number, valor: number): boolean {
    return this.respostasArray.at(index).value === valor;
  }

  enviarSolicitacao(): void {
    this.mensagemSucesso = '';
    this.erroGeral = '';

    if (!this.podeEnviarNovaSolicitacao) {
      this.erroGeral =
        'Você já possui uma solicitação em andamento ou uma trilha aceita.';
      return;
    }

    if (!this.perguntas.length) {
      this.erroGeral = 'Não há perguntas ativas cadastradas no sistema.';
      return;
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const respostas = this.perguntas.map((pergunta, index) => ({
      pergunta_id: pergunta.id,
      valor: Number(this.respostasArray.at(index).value),
    }));

    this.enviando = true;
    this.solicitacoesService.criar({ respostas }).subscribe({
      next: (solicitacao) => {
        this.enviando = false;
        this.solicitacoes = [solicitacao, ...this.solicitacoes];
        this.sincronizarMensagensChamado();
        this.form.reset();
        this.reconstruirRespostas();
        this.mensagemSucesso =
          'Solicitação enviada. Revise abaixo as trilhas candidatas sugeridas.';
      },
      error: (err) => {
        this.enviando = false;
        console.error(err);
        this.erroGeral =
          err?.error?.detail ?? 'Erro ao enviar solicitação de trilha.';
      },
    });
  }

  aceitarTrilha(solicitacao: SolicitarTrilhaResponse, trilha: Trilha): void {
    this.processandoAcaoId = solicitacao.id;
    this.erroGeral = '';
    this.mensagemSucesso = '';

    this.solicitacoesService.aceitar(solicitacao.id, trilha.id).subscribe({
      next: (atualizada) => {
        this.processandoAcaoId = null;
        this.atualizarSolicitacaoNaLista(atualizada);
        this.mensagemSucesso = `Trilha "${trilha.nome}" aceita com sucesso.`;
      },
      error: (err) => {
        this.processandoAcaoId = null;
        console.error(err);
        this.erroGeral = err?.error?.detail ?? 'Erro ao aceitar trilha.';
      },
    });
  }

  rejeitarTrilhas(solicitacao: SolicitarTrilhaResponse): void {
    this.processandoAcaoId = solicitacao.id;
    this.erroGeral = '';
    this.mensagemSucesso = '';

    this.solicitacoesService.rejeitar(solicitacao.id).subscribe({
      next: (atualizada) => {
        this.processandoAcaoId = null;
        this.atualizarSolicitacaoNaLista(atualizada);
        this.mensagemSucesso =
          'As trilhas sugeridas foram rejeitadas. Agora você pode editar o chamado aberto para detalhar sua solicitação.';
      },
      error: (err) => {
        this.processandoAcaoId = null;
        console.error(err);
        this.erroGeral = err?.error?.detail ?? 'Erro ao rejeitar trilhas.';
      },
    });
  }

  baixarMaterial(solicitacao: SolicitarTrilhaResponse): void {
    this.baixandoMaterialId = solicitacao.id;
    this.erroGeral = '';

    this.solicitacoesService.baixarMaterial(solicitacao.id).subscribe({
      next: (blob) => {
        this.baixandoMaterialId = null;
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `material_trilha_${solicitacao.id}.pdf`;
        link.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        this.baixandoMaterialId = null;
        console.error(err);
        this.erroGeral = err?.error?.detail ?? 'Erro ao baixar material da trilha.';
      },
    });
  }

  atualizarMensagemChamado(chamadoId: number, mensagem: string): void {
    this.mensagensChamado[chamadoId] = mensagem;
    delete this.errosChamado[chamadoId];
    this.erroGeral = '';
    this.mensagemSucesso = '';
  }

  abrirEditorChamado(chamadoId: number): void {
    this.editorChamadoAberto[chamadoId] = true;
    delete this.errosChamado[chamadoId];
    this.erroGeral = '';
    this.mensagemSucesso = '';
  }

  salvarMensagemChamado(solicitacao: SolicitarTrilhaResponse): void {
    const chamado = solicitacao.chamado;
    if (!chamado) {
      return;
    }

    const mensagem = (this.mensagensChamado[chamado.id] ?? chamado.mensagem).trim();
    if (!mensagem) {
      this.errosChamado[chamado.id] = 'Informe uma mensagem para o chamado.';
      return;
    }

    this.salvandoChamadoId = chamado.id;
    delete this.errosChamado[chamado.id];
    this.erroGeral = '';
    this.mensagemSucesso = '';

    this.chamadoService.editarMensagem(chamado.id, mensagem).subscribe({
      next: (chamadoAtualizado) => {
        this.salvandoChamadoId = null;
        this.mensagensChamado[chamado.id] = chamadoAtualizado.mensagem;
        this.editorChamadoAberto[chamado.id] = false;
        this.solicitacoes = this.solicitacoes.map((item) =>
          item.id === solicitacao.id ? { ...item, chamado: chamadoAtualizado } : item
        );
        this.mensagemSucesso = 'Chamado atualizado com sucesso.';
      },
      error: (err) => {
        this.salvandoChamadoId = null;
        console.error(err);
        this.errosChamado[chamado.id] =
          err?.error?.detail ?? 'Erro ao atualizar a mensagem do chamado.';
      },
    });
  }

  private atualizarSolicitacaoNaLista(atualizada: SolicitarTrilhaResponse): void {
    this.solicitacoes = this.solicitacoes.map((item) =>
      item.id === atualizada.id ? atualizada : item
    );
    this.sincronizarMensagensChamado();
  }

  podeAdicionarDescricao(solicitacao: SolicitarTrilhaResponse): boolean {
    const chamado = solicitacao.chamado;
    if (!chamado || chamado.status !== 'ABERTO') {
      return false;
    }

    return !this.editorChamadoAberto[chamado.id];
  }

  exibirEditorChamado(solicitacao: SolicitarTrilhaResponse): boolean {
    const chamado = solicitacao.chamado;
    if (!chamado || chamado.status !== 'ABERTO') {
      return false;
    }

    return this.editorChamadoAberto[chamado.id] === true;
  }

  private sincronizarMensagensChamado(): void {
    const mensagensAtualizadas: Record<number, string> = {};

    this.solicitacoes.forEach((solicitacao) => {
      if (solicitacao.chamado) {
        mensagensAtualizadas[solicitacao.chamado.id] =
          this.mensagensChamado[solicitacao.chamado.id] ?? solicitacao.chamado.mensagem;
      }
    });

    this.mensagensChamado = mensagensAtualizadas;
  }

  tipoPerguntaLabel(tipo: Pergunta['tipo']): string {
    return tipo === 'PRATICA' ? 'Prática' : 'Conceitual';
  }

  statusLabel(status: SolicitarTrilhaResponse['status']): string {
    if (status === 'ACEITA') return 'Aceita';
    if (status === 'REJEITADA') return 'Rejeitada';
    return 'Pendente';
  }
}

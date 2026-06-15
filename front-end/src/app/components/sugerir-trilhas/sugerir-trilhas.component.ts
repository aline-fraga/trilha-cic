import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { Disciplina } from '../../models/disciplina';
import { SugestaoTrilhaResponse } from '../../models/sugestao-trilha';
import { DisciplinaService } from '../../services/disciplina.service';
import { SugestoesTrilhaService } from '../../services/sugestoes-trilha.service';

@Component({
  selector: 'app-sugerir-trilhas',
  standalone: false,
  templateUrl: './sugerir-trilhas.component.html',
  styleUrl: './sugerir-trilhas.component.css',
})
export class SugerirTrilhasComponent implements OnInit {
  disciplinas: Disciplina[] = [];
  sugestoes: SugestaoTrilhaResponse[] = [];
  sugestaoConfirmada: SugestaoTrilhaResponse | null = null;
  erroModalTitulo = '';
  erroModalMensagem = '';
  filtroDisciplina = '';
  form!: FormGroup;

  carregando = true;
  enviando = false;
  erroGeral = '';
  mensagemSucesso = '';
  erros: Record<string, string> = {};

  constructor(
    private readonly fb: FormBuilder,
    private readonly disciplinaService: DisciplinaService,
    private readonly sugestoesTrilhaService: SugestoesTrilhaService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarPagina();
  }

  get disciplinasSelecionadasIds(): number[] {
    return this.form.get('disciplinas_ids')?.value ?? [];
  }

  get disciplinasFiltradas(): Disciplina[] {
    const filtro = this.normalizarTexto(this.filtroDisciplina);
    if (!filtro) {
      return this.disciplinas;
    }

    return this.disciplinas.filter((disciplina) => {
      const alvo = this.normalizarTexto(
        `${disciplina.codigo} ${disciplina.nome} ${this.formatarTipo(disciplina.tipo)}`
      );
      return alvo.includes(filtro);
    });
  }

  get possuiChamadoAberto(): boolean {
    return this.sugestoes.some((sugestao) => sugestao.chamado?.status === 'ABERTO');
  }

  private inicializarForm(): void {
    this.form = this.fb.group({
      nome: ['', [Validators.required]],
      disciplinas_ids: [[] as number[]],
    });
  }

  private carregarPagina(): void {
    this.carregando = true;
    this.erroGeral = '';

    forkJoin({
      disciplinas: this.disciplinaService.listar(true),
      sugestoes: this.sugestoesTrilhaService.listar(),
    }).subscribe({
      next: ({ disciplinas, sugestoes }) => {
        this.disciplinas = [...disciplinas].sort((a, b) =>
          a.nome.localeCompare(b.nome, 'pt-BR')
        );
        this.sugestoes = [...sugestoes].sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        this.carregando = false;
      },
      error: () => {
        this.carregando = false;
        this.erroGeral = 'Não foi possível carregar o formulário de sugestão.';
        this.abrirModalErro(
          'Erro ao carregar formulário',
          'Não foi possível carregar o formulário de sugestão.'
        );
      },
    });
  }

  enviarSugestao(): void {
    this.erroGeral = '';
    this.mensagemSucesso = '';
    this.erros = {};

    if (this.form.invalid) {
      this.form.markAllAsTouched();
    }

    if (!this.form.get('nome')?.value?.trim()) {
      this.erros['nome'] = 'Informe o nome da trilha.';
    }

    const disciplinasIds = this.disciplinasSelecionadasIds;
    if (!disciplinasIds.length) {
      this.erros['disciplinas_ids'] = 'Selecione ao menos uma disciplina.';
    } else if (disciplinasIds.length > 4) {
      this.erros['disciplinas_ids'] =
        'Selecione no máximo 4 disciplinas para a sugestão.';
    }

    if (Object.keys(this.erros).length > 0 || this.form.invalid) {
      this.abrirModalErro(
        'Dados incompletos',
        this.montarMensagemValidacao()
      );
      return;
    }

    if (this.possuiChamadoAberto) {
      this.abrirModalErro(
        'Chamado já em aberto',
        'Você já possui um chamado em aberto para sugestão de trilha. Aguarde a resposta da COMGRAD antes de enviar outra sugestão.'
      );
      return;
    }

    this.enviando = true;
    this.sugestoesTrilhaService
      .criar({
        nome: this.form.get('nome')?.value.trim(),
        disciplinas_ids: disciplinasIds,
      })
      .subscribe({
        next: (sugestao) => {
          this.enviando = false;
          this.sugestoes = [sugestao, ...this.sugestoes];
          this.sugestaoConfirmada = sugestao;
          this.form.reset({ nome: '', disciplinas_ids: [] });
          this.filtroDisciplina = '';
        },
        error: (err) => {
          this.enviando = false;
          this.aplicarErroBackend(err);
        },
      });
  }

  toggleDisciplina(id: number, event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    const atual = [...this.disciplinasSelecionadasIds];
    this.erros['disciplinas_ids'] = '';
    this.erroGeral = '';

    if (checked) {
      this.form.get('disciplinas_ids')?.setValue([...atual, id]);
      return;
    }

    this.form.get('disciplinas_ids')?.setValue(atual.filter((valor) => valor !== id));
  }

  disciplinaSelecionada(id: number): boolean {
    return this.disciplinasSelecionadasIds.includes(id);
  }

  disciplinaDesabilitada(id: number): boolean {
    return (
      this.disciplinasSelecionadasIds.length >= 4 &&
      !this.disciplinasSelecionadasIds.includes(id)
    );
  }

  limparErrosGerais(): void {
    this.erroGeral = '';
    this.mensagemSucesso = '';
  }

  fecharModalConfirmacao(): void {
    this.sugestaoConfirmada = null;
  }

  fecharModalErro(): void {
    this.erroModalTitulo = '';
    this.erroModalMensagem = '';
  }

  formatarTipo(tipo: string): string {
    return tipo === 'OBRIGATORIA' ? 'Obrigatória' : 'Eletiva';
  }

  formatarStatusChamado(status: string): string {
    return status === 'FECHADO' ? 'Fechado' : 'Aberto';
  }

  private aplicarErroBackend(err: any): void {
    const detail = err?.error?.detail;

    if (typeof detail === 'string') {
      if (detail.toLowerCase().includes('nome')) {
        this.erros['nome'] = detail;
        this.abrirModalErro('Nome da trilha inválido', detail);
      } else if (detail.toLowerCase().includes('disciplina')) {
        this.erros['disciplinas_ids'] = detail;
        this.abrirModalErro('Disciplinas inválidas', detail);
      } else {
        this.erroGeral = detail;
        this.abrirModalErro('Não foi possível enviar a sugestão', detail);
      }
      return;
    }

    if (Array.isArray(detail) && detail.length > 0) {
      this.erroGeral = detail.map((item) => item?.msg).filter(Boolean).join(' ');
      this.abrirModalErro(
        'Não foi possível enviar a sugestão',
        this.erroGeral
      );
      return;
    }

    this.erroGeral = 'Erro ao enviar sugestão de trilha.';
    this.abrirModalErro(
      'Não foi possível enviar a sugestão',
      this.erroGeral
    );
  }

  private normalizarTexto(texto: string): string {
    return texto
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();
  }

  private abrirModalErro(titulo: string, mensagem: string): void {
    this.erroModalTitulo = titulo;
    this.erroModalMensagem = mensagem;
  }

  private montarMensagemValidacao(): string {
    if (this.erros['nome']) {
      return this.erros['nome'];
    }

    if (this.erros['disciplinas_ids']) {
      return this.erros['disciplinas_ids'];
    }

    return 'Revise os dados informados antes de enviar a sugestão.';
  }
}

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Disciplina } from '../../models/disciplina';
import { Trilha } from '../../models/trilha';
import { DisciplinaService } from '../../services/disciplina.service';
import { GerenciarTrilhasService } from '../../services/gerenciar-trilhas.service';

@Component({
  selector: 'app-gerenciar-trilhas',
  standalone: false,
  templateUrl: './gerenciar-trilhas.component.html',
  styleUrl: './gerenciar-trilhas.component.css',
})
export class GerenciarTrilhasComponent implements OnInit {
  trilhas: Trilha[] = [];
  disciplinas: Disciplina[] = [];
  editando: Trilha | null = null;
  mostrarFormulario = false;
  erroGeral = '';
  erros: Record<string, string> = {};
  form!: FormGroup;

  constructor(
    private readonly fb: FormBuilder,
    private readonly trilhasService: GerenciarTrilhasService,
    private readonly disciplinaService: DisciplinaService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarTrilhas();
    this.carregarDisciplinas();
  }

  private inicializarForm(trilha?: Trilha): void {
    this.form = this.fb.group({
      nome: [trilha?.nome ?? '', [Validators.required]],
      resumo: [trilha?.resumo ?? '', [Validators.required]],
      disciplinas_ids: [trilha?.disciplinas.map((d) => d.id) ?? []],
    });
    this.erros = {};
    this.erroGeral = '';
  }

  private carregarTrilhas(): void {
    this.trilhasService.listar().subscribe({
      next: (t) => (this.trilhas = t),
      error: () => (this.erroGeral = 'Erro ao carregar trilhas.'),
    });
  }

  private carregarDisciplinas(): void {
    this.disciplinaService.listar().subscribe({
      next: (d) => (this.disciplinas = d),
      error: () => {},
    });
  }

  abrirCadastro(): void {
    this.editando = null;
    this.inicializarForm();
    this.mostrarFormulario = true;
  }

  abrirEdicao(trilha: Trilha): void {
    this.editando = trilha;
    this.inicializarForm(trilha);
    this.mostrarFormulario = true;
  }

  fecharFormulario(): void {
    this.mostrarFormulario = false;
    this.editando = null;
  }

  salvar(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const ids: number[] = this.form.get('disciplinas_ids')?.value ?? [];
    if (ids.length > 4) {
      this.erros['disciplinas_ids'] = 'Uma trilha pode ter no máximo 4 disciplinas.';
      return;
    }
    this.erros = {};
    this.erroGeral = '';

    const valor = this.form.value;

    const request$ = this.editando
      ? this.trilhasService.atualizar(this.editando.id, valor)
      : this.trilhasService.criar(valor);

    request$.subscribe({
      next: () => {
        this.fecharFormulario();
        this.carregarTrilhas();
      },
      error: (err) => {
        const detail = err?.error?.detail;
        if (detail?.campo) {
          this.erros[detail.campo] = detail.mensagem;
        } else {
          this.erroGeral = detail ?? 'Erro ao salvar trilha.';
        }
      },
    });
  }

  excluir(trilha: Trilha): void {
    if (!confirm(`Excluir "${trilha.nome}"?`)) return;
    this.trilhasService.excluir(trilha.id).subscribe({
      next: () => this.carregarTrilhas(),
      error: () => (this.erroGeral = 'Erro ao excluir trilha.'),
    });
  }

  campoInvalido(campo: string): boolean {
    const c = this.form.get(campo);
    return !!(c && c.invalid && c.touched);
  }

  disciplinaSelecionada(id: number): boolean {
    return (this.form.get('disciplinas_ids')?.value as number[]).includes(id);
  }

  disciplinaDesabilitada(id: number): boolean {
    const selecionadas: number[] = this.form.get('disciplinas_ids')?.value ?? [];
    return selecionadas.length >= 4 && !selecionadas.includes(id);
  }

  toggleDisciplina(id: number, event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    const atual: number[] = [...(this.form.get('disciplinas_ids')?.value ?? [])];
    if (checked) {
      this.form.get('disciplinas_ids')?.setValue([...atual, id]);
    } else {
      this.form.get('disciplinas_ids')?.setValue(atual.filter((v) => v !== id));
    }
  }

  disciplinasSelecionadas(trilha: Trilha): string {
    return trilha.disciplinas.length > 0
      ? trilha.disciplinas.map((d) => d.codigo).join(', ')
      : '—';
  }
}

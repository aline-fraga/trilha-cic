import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Disciplina, DisciplinaTipo } from '../../models/disciplina';
import { DisciplinaService } from '../../services/disciplina.service';

@Component({
  selector: 'app-curriculo',
  standalone: false,
  templateUrl: './curriculo.component.html',
  styleUrl: './curriculo.component.css',
})
export class CurriculoComponent implements OnInit {
  disciplinas: Disciplina[] = [];
  editando: Disciplina | null = null;
  mostrarFormulario = false;
  erroGeral = '';
  erros: Record<string, string> = {};
  form!: FormGroup;

  readonly tipos: DisciplinaTipo[] = ['OBRIGATORIA', 'ELETIVA'];

  constructor(
    private readonly fb: FormBuilder,
    private readonly disciplinaService: DisciplinaService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarDisciplinas();
  }

  private inicializarForm(disciplina?: Disciplina): void {
    this.form = this.fb.group({
      nome: [disciplina?.nome ?? '', [Validators.required]],
      codigo: [disciplina?.codigo ?? '', [Validators.required]],
      tipo: [disciplina?.tipo ?? 'ELETIVA', [Validators.required]],
      carga_horaria: [disciplina?.carga_horaria ?? null, [Validators.required, Validators.min(1)]],
      link_plano_ensino: [disciplina?.link_plano_ensino ?? ''],
      prerequisito_ids: [disciplina?.prerequisitos.map((p) => p.id) ?? []],
    });
    this.erros = {};
    this.erroGeral = '';
  }

  private carregarDisciplinas(): void {
    this.disciplinaService.listar().subscribe({
      next: (d) => (this.disciplinas = d),
      error: () => (this.erroGeral = 'Erro ao carregar disciplinas.'),
    });
  }

  abrirCadastro(): void {
    this.editando = null;
    this.inicializarForm();
    this.mostrarFormulario = true;
  }

  abrirEdicao(disciplina: Disciplina): void {
    this.editando = disciplina;
    this.inicializarForm(disciplina);
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
    this.erros = {};
    this.erroGeral = '';

    const valor = this.form.value;
    const body = {
      ...valor,
      link_plano_ensino: valor.link_plano_ensino || undefined,
      prerequisito_ids: valor.prerequisito_ids ?? [],
    };

    const request$ = this.editando
      ? this.disciplinaService.atualizar(this.editando.id, body)
      : this.disciplinaService.criar(body);

    request$.subscribe({
      next: () => {
        this.fecharFormulario();
        this.carregarDisciplinas();
      },
      error: (err) => {
        const detail = err?.error?.detail;
        if (detail?.campo) {
          this.erros[detail.campo] = detail.mensagem;
        } else {
          this.erroGeral = detail ?? 'Erro ao salvar disciplina.';
        }
      },
    });
  }

  excluir(disciplina: Disciplina): void {
    if (!confirm(`Excluir "${disciplina.nome}"?`)) return;
    this.disciplinaService.excluir(disciplina.id).subscribe({
      next: () => this.carregarDisciplinas(),
      error: () => (this.erroGeral = 'Erro ao excluir disciplina.'),
    });
  }

  campoInvalido(campo: string): boolean {
    const c = this.form.get(campo);
    return !!(c && c.invalid && c.touched);
  }
}

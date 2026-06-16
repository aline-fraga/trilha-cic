import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserAdminResponse, UserCreate, UserRole, UserUpdate } from '../../models/user';
import { UsersService } from '../../services/users.service';

@Component({
  selector: 'app-gerenciar-usuarios',
  standalone: false,
  templateUrl: './gerenciar-usuarios.component.html',
  styleUrl: './gerenciar-usuarios.component.css',
})
export class GerenciarUsuariosComponent implements OnInit {
  usuarios: UserAdminResponse[] = [];
  form!: FormGroup;
  editando: UserAdminResponse | null = null;
  mostrarFormulario = false;
  carregando = false;
  salvando = false;
  erroGeral = '';
  erros: Record<string, string> = {};

  filtroRole: UserRole | '' = '';
  filtroStatus: boolean | '' = true;

  readonly roles: UserRole[] = ['ALUNO', 'COMGRAD', 'ADMIN'];

  constructor(
    private readonly fb: FormBuilder,
    private readonly usersService: UsersService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarUsuarios();
  }

  get roleSelecionada(): UserRole | null {
    return (this.form.get('role')?.value as UserRole | null) ?? null;
  }

  get exibindoCamposAluno(): boolean {
    return this.roleSelecionada === 'ALUNO';
  }

  abrirCadastro(): void {
    this.editando = null;
    this.inicializarForm();
    this.mostrarFormulario = true;
  }

  abrirEdicao(usuario: UserAdminResponse): void {
    this.editando = usuario;
    this.inicializarForm(usuario);
    this.mostrarFormulario = true;
  }

  fecharFormulario(): void {
    this.mostrarFormulario = false;
    this.editando = null;
    this.salvando = false;
    this.erros = {};
    this.erroGeral = '';
  }

  carregarUsuarios(): void {
    this.carregando = true;
    this.erroGeral = '';
    this.usersService
      .listar({
        role: this.filtroRole,
        is_active: this.filtroStatus,
      })
      .subscribe({
        next: (usuarios) => {
          this.usuarios = usuarios;
          this.carregando = false;
        },
        error: () => {
          this.erroGeral = 'Erro ao carregar usuários.';
          this.carregando = false;
        },
      });
  }

  salvar(): void {
    this.atualizarValidacoesAluno();

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.salvando = true;
    this.erros = {};
    this.erroGeral = '';

    const request$ = this.editando
      ? this.usersService.atualizar(this.editando.id, this.montarPayloadEdicao())
      : this.usersService.criar(this.montarPayloadCriacao());

    request$.subscribe({
      next: () => {
        this.salvando = false;
        this.fecharFormulario();
        this.carregarUsuarios();
      },
      error: (err) => {
        this.salvando = false;
        const detail = this.extrairMensagemErro(err);
        if (this.isErroCampo(detail)) {
          this.erros[detail.campo] = detail.mensagem;
          return;
        }
        this.erroGeral = detail ?? 'Erro ao salvar usuário.';
      },
    });
  }

  excluir(usuario: UserAdminResponse): void {
    if (!confirm(`Desativar o usuário "${usuario.nome}"?`)) {
      return;
    }

    this.usersService.excluir(usuario.id).subscribe({
      next: () => this.carregarUsuarios(),
      error: () => {
        this.erroGeral = 'Erro ao desativar usuário.';
      },
    });
  }

  onRoleChange(): void {
    this.atualizarValidacoesAluno();
    this.limparErroGeral();
  }

  limparErroGeral(): void {
    this.erroGeral = '';
  }

  campoInvalido(campo: string): boolean {
    const controle = this.form.get(campo);
    return !!(controle && controle.invalid && controle.touched);
  }

  alunoLabel(usuario: UserAdminResponse): string {
    if (!usuario.aluno) {
      return '—';
    }

    return `${usuario.aluno.cartao_ufrgs} · ${usuario.aluno.semestre_ingresso}`;
  }

  roleLabel(role: UserRole): string {
    if (role === 'ALUNO') {
      return 'Aluno';
    }

    if (role === 'COMGRAD') {
      return 'COMGRAD';
    }

    return 'Admin';
  }

  statusLabel(isActive: boolean): string {
    return isActive ? 'Ativo' : 'Inativo';
  }

  private inicializarForm(usuario?: UserAdminResponse): void {
    this.form = this.fb.group({
      nome: [usuario?.nome ?? '', [Validators.required, Validators.maxLength(150)]],
      email: [usuario?.email ?? '', [Validators.required, Validators.email]],
      password: ['', usuario ? [] : [Validators.required, Validators.minLength(8)]],
      role: [usuario?.role ?? 'ALUNO', [Validators.required]],
      is_active: [usuario?.is_active ?? true],
      aluno: this.fb.group({
        cartao_ufrgs: [usuario?.aluno?.cartao_ufrgs ?? ''],
        semestre_ingresso: [usuario?.aluno?.semestre_ingresso ?? ''],
      }),
    });

    if (usuario) {
      this.form.get('role')?.disable();
    }

    this.atualizarValidacoesAluno();
    this.erros = {};
    this.erroGeral = '';
  }

  private atualizarValidacoesAluno(): void {
    const alunoGroup = this.form.get('aluno') as FormGroup;
    const cartao = alunoGroup.get('cartao_ufrgs');
    const semestre = alunoGroup.get('semestre_ingresso');

    if (this.roleSelecionada === 'ALUNO') {
      cartao?.setValidators([Validators.required, Validators.maxLength(20)]);
      semestre?.setValidators([
        Validators.required,
        Validators.maxLength(7),
        Validators.pattern(/^\d{4}\/\d{2}$/),
      ]);
    } else {
      cartao?.clearValidators();
      semestre?.clearValidators();
      alunoGroup.reset(
        {
          cartao_ufrgs: '',
          semestre_ingresso: '',
        },
        { emitEvent: false }
      );
    }

    cartao?.updateValueAndValidity({ emitEvent: false });
    semestre?.updateValueAndValidity({ emitEvent: false });
  }

  private montarPayloadCriacao(): UserCreate {
    const value = this.form.getRawValue();

    return {
      nome: value.nome.trim(),
      email: value.email.trim(),
      password: value.password,
      role: value.role,
      aluno: value.role === 'ALUNO' ? this.montarAlunoPayload(value.aluno) : undefined,
    };
  }

  private montarPayloadEdicao(): UserUpdate {
    const value = this.form.getRawValue();

    return {
      nome: value.nome.trim(),
      email: value.email.trim(),
      is_active: value.is_active,
      aluno: value.role === 'ALUNO' ? this.montarAlunoPayload(value.aluno) : undefined,
    };
  }

  private montarAlunoPayload(alunoValue: {
    cartao_ufrgs: string;
    semestre_ingresso: string;
  }) {
    return {
      cartao_ufrgs: alunoValue.cartao_ufrgs.trim(),
      semestre_ingresso: alunoValue.semestre_ingresso.trim(),
    };
  }

  private extrairMensagemErro(err: unknown): { campo: string; mensagem: string } | string | null {
    const detail = (err as { error?: { detail?: unknown } })?.error?.detail;

    if (typeof detail === 'string') {
      return detail;
    }

    if (
      detail &&
      typeof detail === 'object' &&
      'campo' in detail &&
      'mensagem' in detail &&
      typeof detail.campo === 'string' &&
      typeof detail.mensagem === 'string'
    ) {
      return {
        campo: detail.campo,
        mensagem: detail.mensagem,
      };
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (item && typeof item === 'object' && 'msg' in item && typeof item.msg === 'string') {
            return item.msg;
          }

          return null;
        })
        .filter((item): item is string => !!item)
        .join(' ');
    }

    return null;
  }

  private isErroCampo(
    detail: { campo: string; mensagem: string } | string | null
  ): detail is { campo: string; mensagem: string } {
    return !!detail && typeof detail !== 'string';
  }
}

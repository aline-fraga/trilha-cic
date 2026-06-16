import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Relatorio } from '../../models/relatorio';
import { RelatoriosService } from '../../services/relatorios.service';

@Component({
  selector: 'app-relatorios',
  standalone: false,
  templateUrl: './relatorios.component.html',
  styleUrl: './relatorios.component.css',
})
export class RelatoriosComponent implements OnInit {
  form!: FormGroup;
  relatorios: Relatorio[] = [];
  relatorioSelecionado: Relatorio | null = null;
  ultimoRelatorioGeradoId: number | null = null;

  carregando = true;
  carregandoDetalhes = false;
  gerando = false;
  baixandoPdfId: number | null = null;
  erroGeral = '';
  mensagemSucesso = '';

  constructor(
    private readonly fb: FormBuilder,
    private readonly relatoriosService: RelatoriosService
  ) {}

  ngOnInit(): void {
    this.inicializarForm();
    this.carregarRelatorios();
  }

  private inicializarForm(): void {
    this.form = this.fb.group({
      periodo_inicio: [this.formatarParaInput(this.calcularInicioPadrao()), Validators.required],
      periodo_fim: [this.formatarParaInput(new Date()), Validators.required],
    });
  }

  carregarRelatorios(): void {
    this.carregando = true;
    this.erroGeral = '';

    this.relatoriosService.listar().subscribe({
      next: (relatorios) => {
        this.relatorios = this.ordenarRelatorios(relatorios);
        this.relatorioSelecionado = this.relatorios[0] ?? null;
        this.carregando = false;
      },
      error: (err) => {
        console.error(err);
        this.carregando = false;
        this.erroGeral = 'Não foi possível carregar os relatórios.';
      },
    });
  }

  selecionarRelatorio(relatorioId: number): void {
    if (this.relatorioSelecionado?.id === relatorioId) {
      return;
    }

    this.carregandoDetalhes = true;
    this.erroGeral = '';

    this.relatoriosService.obter(relatorioId).subscribe({
      next: (relatorio) => {
        this.relatorioSelecionado = relatorio;
        this.atualizarRelatorioNaLista(relatorio);
        this.carregandoDetalhes = false;
      },
      error: (err) => {
        console.error(err);
        this.carregandoDetalhes = false;
        this.erroGeral =
          err?.error?.detail ??
          'Não foi possível carregar os detalhes do relatório.';
      },
    });
  }

  gerarRelatorio(): void {
    this.mensagemSucesso = '';
    this.erroGeral = '';

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const periodoInicio = this.form.value.periodo_inicio as string;
    const periodoFim = this.form.value.periodo_fim as string;

    if (!this.periodoValido(periodoInicio, periodoFim)) {
      return;
    }

    this.gerando = true;
    this.relatoriosService
      .criar({
        periodo_inicio: this.normalizarDatetime(periodoInicio),
        periodo_fim: this.normalizarDatetime(periodoFim),
      })
      .subscribe({
        next: (relatorio) => {
          this.gerando = false;
          this.relatorios = this.ordenarRelatorios([relatorio, ...this.relatorios]);
          this.relatorioSelecionado = relatorio;
          this.ultimoRelatorioGeradoId = relatorio.id;
          this.mensagemSucesso = `Relatório #${relatorio.id} gerado com sucesso.`;
        },
        error: (err) => {
          console.error(err);
          this.gerando = false;
          this.erroGeral = err?.error?.detail ?? 'Erro ao gerar relatório.';
        },
      });
  }

  onSubmit(event: Event): void {
    event.preventDefault();
    this.gerarRelatorio();
  }

  baixarPdf(relatorio: Relatorio): void {
    this.baixandoPdfId = relatorio.id;
    this.erroGeral = '';

    this.relatoriosService.baixarPdf(relatorio.id).subscribe({
      next: (blob) => {
        this.baixandoPdfId = null;
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `relatorio_${relatorio.id}.pdf`;
        link.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error(err);
        this.baixandoPdfId = null;
        this.erroGeral = err?.error?.detail ?? 'Erro ao baixar PDF do relatório.';
      },
      });
  }

  baixarPdfDoSelecionado(): void {
    if (!this.relatorioSelecionado) {
      return;
    }

    this.baixarPdf(this.relatorioSelecionado);
  }

  trackByRelatorioId(_index: number, relatorio: Relatorio): number {
    return relatorio.id;
  }

  private periodoValido(periodoInicio: string, periodoFim: string): boolean {
    const inicio = new Date(periodoInicio);
    const fim = new Date(periodoFim);
    const agora = new Date();

    if (Number.isNaN(inicio.getTime()) || Number.isNaN(fim.getTime())) {
      this.erroGeral = 'Informe datas válidas para gerar o relatório.';
      return false;
    }

    if (inicio >= fim) {
      this.erroGeral = 'O início do período deve ser anterior ao fim do período.';
      return false;
    }

    if (fim > agora) {
      this.erroGeral = 'O fim do período deve estar no passado.';
      return false;
    }

    return true;
  }

  private atualizarRelatorioNaLista(relatorioAtualizado: Relatorio): void {
    this.relatorios = this.ordenarRelatorios(
      this.relatorios.map((item) =>
        item.id === relatorioAtualizado.id ? relatorioAtualizado : item
      )
    );
  }

  private ordenarRelatorios(relatorios: Relatorio[]): Relatorio[] {
    const unicos = new Map<number, Relatorio>();
    relatorios.forEach((relatorio) => unicos.set(relatorio.id, relatorio));

    return Array.from(unicos.values()).sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );
  }

  private calcularInicioPadrao(): Date {
    const data = new Date();
    data.setMonth(data.getMonth() - 1);
    return data;
  }

  private formatarParaInput(data: Date): string {
    const ano = data.getFullYear();
    const mes = `${data.getMonth() + 1}`.padStart(2, '0');
    const dia = `${data.getDate()}`.padStart(2, '0');
    const horas = `${data.getHours()}`.padStart(2, '0');
    const minutos = `${data.getMinutes()}`.padStart(2, '0');
    return `${ano}-${mes}-${dia}T${horas}:${minutos}`;
  }

  private normalizarDatetime(valor: string): string {
    return valor.length === 16 ? `${valor}:00` : valor;
  }
}

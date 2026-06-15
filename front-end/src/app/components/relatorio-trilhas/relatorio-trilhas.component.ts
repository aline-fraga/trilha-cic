import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { RelatoriosService, RelatorioResponse, RelatorioItem } from '../../services/relatorios.service';

@Component({
  selector: 'app-relatorio-trilhas',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './relatorio-trilhas.component.html',
  styleUrls: ['./relatorio-trilhas.component.css']
})
export class RelatorioTrilhasComponent implements OnInit {
  relatorios: RelatorioResponse[] = [];
  relatorioSelecionado: RelatorioResponse | null = null;
  
  isLoading = false;
  isGenerating = false;
  errorMessage = '';
  successMessage = '';

  gerarForm: FormGroup;

  constructor(
    private relatoriosService: RelatoriosService,
    private authService: AuthService,
    private router: Router,
    private fb: FormBuilder
  ) {
    this.gerarForm = this.fb.group({
      periodo_inicio: ['', Validators.required],
      periodo_fim: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    const user = this.authService.currentUser$.getValue();
    if (!user || (user.role !== 'COMGRAD' && user.role !== 'ADMIN')) {
      this.router.navigate(['/trilhas']);
      return;
    }

    this.loadRelatorios();
  }

  loadRelatorios() {
    this.isLoading = true;
    this.relatoriosService.listarRelatorios().subscribe({
      next: (data) => {
        this.relatorios = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erro ao carregar o histórico de relatórios.';
        this.isLoading = false;
      }
    });
  }

  onGerar() {
    if (this.gerarForm.invalid) {
      this.errorMessage = 'Preencha o período de início e fim.';
      return;
    }

    this.errorMessage = '';
    this.successMessage = '';
    this.isGenerating = true;

    const formValues = this.gerarForm.value;
    const pInicio = new Date(formValues.periodo_inicio);
    pInicio.setHours(0, 0, 0, 0);
    const pFim = new Date(formValues.periodo_fim);
    pFim.setHours(23, 59, 59, 999);

    if (pInicio >= pFim) {
      this.errorMessage = 'A data de início deve ser anterior à data de fim.';
      this.isGenerating = false;
      return;
    }

    const payload = {
      periodo_inicio: pInicio.toISOString(),
      periodo_fim: pFim.toISOString()
    };

    this.relatoriosService.gerarRelatorio(payload).subscribe({
      next: (novoRelatorio) => {
        this.successMessage = 'Relatório gerado com sucesso!';
        this.gerarForm.reset();
        this.isGenerating = false;
        this.loadRelatorios();
      },
      error: (err) => {
        this.errorMessage = err.error?.detail || 'Erro ao gerar relatório.';
        this.isGenerating = false;
      }
    });
  }

  verDetalhes(id: number) {
    this.isLoading = true;
    this.relatorioSelecionado = null;
    this.relatoriosService.obterRelatorio(id).subscribe({
      next: (data) => {
        this.relatorioSelecionado = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Erro ao buscar detalhes do relatório.';
        this.isLoading = false;
      }
    });
  }

  voltarParaLista() {
    this.relatorioSelecionado = null;
    this.errorMessage = '';
    this.successMessage = '';
  }

  baixarPdf(id: number, event?: Event) {
    if (event) {
      event.stopPropagation();
    }
    
    this.errorMessage = '';
    this.relatoriosService.baixarPdf(id).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `relatorio_${id}.pdf`;
        document.body.appendChild(a);
        a.click();
        
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      },
      error: () => {
        this.errorMessage = 'Erro ao baixar o PDF. Tente novamente.';
      }
    });
  }

  getTaxaAceitacao(item: RelatorioItem): number {
    const total = item.aceites + item.rejeicoes;
    if (total === 0) return 0;
    return (item.aceites / total) * 100;
  }
}

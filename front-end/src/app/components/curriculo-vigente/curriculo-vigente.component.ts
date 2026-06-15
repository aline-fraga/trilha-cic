import { Component, OnInit } from '@angular/core';
import { Disciplina } from '../../models/disciplina';
import { DisciplinaService } from '../../services/disciplina.service';

@Component({
  selector: 'app-curriculo-vigente',
  standalone: false,
  templateUrl: './curriculo-vigente.component.html',
  styleUrl: './curriculo-vigente.component.css',
})
export class CurriculoVigenteComponent implements OnInit {
  disciplinas: Disciplina[] = [];
  carregando = true;
  erroGeral = '';

  constructor(private readonly disciplinaService: DisciplinaService) {}

  ngOnInit(): void {
    this.carregarDisciplinas();
  }

  get totalDisciplinas(): number {
    return this.disciplinas.length;
  }

  get cargaHorariaTotal(): number {
    return this.disciplinas.reduce(
      (total, disciplina) => total + disciplina.carga_horaria,
      0
    );
  }

  get totalAtivas(): number {
    return this.disciplinas.filter((disciplina) => disciplina.is_active).length;
  }

  formatarTipo(tipo: string): string {
    return tipo === 'OBRIGATORIA' ? 'Obrigatória' : 'Eletiva';
  }

  formatarStatus(isActive: boolean): string {
    return isActive ? 'Ativa' : 'Inativa';
  }

  private carregarDisciplinas(): void {
    this.disciplinaService.listar().subscribe({
      next: (disciplinas) => {
        this.disciplinas = [...disciplinas].sort((a, b) =>
          a.nome.localeCompare(b.nome, 'pt-BR')
        );
        this.carregando = false;
      },
      error: () => {
        this.erroGeral = 'Erro ao carregar as disciplinas.';
        this.carregando = false;
      },
    });
  }
}

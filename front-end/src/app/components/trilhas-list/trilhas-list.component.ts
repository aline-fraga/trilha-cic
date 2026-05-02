import { Component, OnInit } from '@angular/core';
import { Trilha } from '../../models/trilha';
import { TrilhasService } from '../../services/trilhas.service';

@Component({
  selector: 'app-trilhas-list',
  standalone: false,
  templateUrl: './trilhas-list.component.html',
  styleUrl: './trilhas-list.component.css'
})
export class TrilhasListComponent implements OnInit {
  trilhas: Trilha[] = [];
  private trilhasRecebidas: Trilha[] = [];
  searchTerm = '';
  ultimaBusca = '';
  sortOption: 'alfabetica' | 'carga-horaria' = 'alfabetica';

  constructor(private readonly trilhasService: TrilhasService) {}

  ngOnInit(): void {
    this.carregarTrilhas();
  }

  buscarTrilhas(): void {
    const disciplina = this.searchTerm.trim();
    this.ultimaBusca = disciplina;

    if (!disciplina) {
      this.carregarTrilhas();
      return;
    }

    this.trilhasService.searchTrilhasByDisciplina(disciplina).subscribe((trilhas) => {
      this.atualizarTrilhas(trilhas);
    });
  }

  limparBusca(): void {
    this.searchTerm = '';
    this.ultimaBusca = '';
    this.carregarTrilhas();
  }

  private carregarTrilhas(): void {
    this.trilhasService.getTrilhas().subscribe((trilhas) => {
      this.atualizarTrilhas(trilhas);
    });
  }

  ordenarTrilhas(): void {
    this.trilhas = [...this.trilhasRecebidas].sort((trilhaA, trilhaB) => {
      if (this.sortOption === 'carga-horaria') {
        return this.getCargaHorariaTotal(trilhaB) - this.getCargaHorariaTotal(trilhaA);
      }

      return trilhaA.nome.localeCompare(trilhaB.nome, 'pt-BR');
    });
  }

  private atualizarTrilhas(trilhas: Trilha[]): void {
    this.trilhasRecebidas = trilhas;
    this.ordenarTrilhas();
  }

  private getCargaHorariaTotal(trilha: Trilha): number {
    return trilha.disciplinas.reduce(
      (total, disciplina) => total + disciplina.carga_horaria,
      0
    );
  }
}

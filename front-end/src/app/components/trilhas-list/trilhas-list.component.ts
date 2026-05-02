import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Trilha } from '../../models/trilha';
import { TrilhasService } from '../../services/trilhas.service';

@Component({
  selector: 'app-trilhas-list',
  standalone: false,
  templateUrl: './trilhas-list.component.html',
  styleUrl: './trilhas-list.component.css'
})
export class TrilhasListComponent implements OnInit {
  trilhas$!: Observable<Trilha[]>;
  searchTerm = '';
  ultimaBusca = '';

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

    this.trilhas$ = this.trilhasService.searchTrilhasByDisciplina(disciplina);
  }

  limparBusca(): void {
    this.searchTerm = '';
    this.ultimaBusca = '';
    this.carregarTrilhas();
  }

  private carregarTrilhas(): void {
    this.trilhas$ = this.trilhasService.getTrilhas();
  }
}

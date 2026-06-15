import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { CurriculoComponent } from './components/curriculo/curriculo.component';
import { LoginComponent } from './components/login/login.component';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';
import { NotImplementedComponent } from './components/not-implemented/not-implemented.component';
import { GerenciarTrilhasComponent } from './components/gerenciar-trilhas/gerenciar-trilhas.component';
import { SolicitarTrilhasComponent } from './components/solicitar-trilhas/solicitar-trilhas.component';
import { CurriculoVigenteComponent } from './components/curriculo-vigente/curriculo-vigente.component';
import { SugerirTrilhasComponent } from './components/sugerir-trilhas/sugerir-trilhas.component';

import { ChamadoComgradComponent } from './components/chamado-comgrad/chamado-comgrad.component';
import { ComgradPainelComponent } from './components/comgrad-painel/comgrad-painel.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: 'trilhas', pathMatch: 'full' },
  { path: 'trilhas', component: TrilhasListComponent, canActivate: [AuthGuard] },
  { path: 'curriculo', component: CurriculoComponent, canActivate: [AuthGuard] },
  {
    path: 'curriculo-vigente',
    component: CurriculoVigenteComponent,
    canActivate: [AuthGuard],
    data: { title: 'Currículo vigente' },
  },
  {
    path: 'solicitar-trilhas',
    component: SolicitarTrilhasComponent,
    canActivate: [AuthGuard],
    data: { title: 'Solicitar trilhas' },
  },
  {
    path: 'sugerir-trilhas',
    component: SugerirTrilhasComponent,
    canActivate: [AuthGuard],
    data: { title: 'Sugerir novas trilhas' },
  },
  {
    path: 'chamado-comgrad',
    component: ChamadoComgradComponent,
    canActivate: [AuthGuard],
    data: { title: 'Abrir chamado com a COMGRAD' },
  },
  {
    path: 'comgrad/painel',
    component: ComgradPainelComponent,
    canActivate: [AuthGuard],
    data: { title: 'Área da COMGRAD' },
  },
  {
    path: 'gerenciar-trilhas',
    component: GerenciarTrilhasComponent,
    canActivate: [AuthGuard],
    data: { title: 'Gerenciar trilhas' },
  },
  {
    path: 'chamados',
    component: NotImplementedComponent,
    canActivate: [AuthGuard],
    data: { title: 'Chamados' },
  },
  {
    path: 'relatorios',
    component: NotImplementedComponent,
    canActivate: [AuthGuard],
    data: { title: 'Relatórios' },
  },
  { path: '**', redirectTo: 'trilhas' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

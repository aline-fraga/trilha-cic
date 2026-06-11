import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './components/login/login.component';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';
import { NotImplementedComponent } from './components/not-implemented/not-implemented.component';

import { ChamadoComgradComponent } from './components/chamado-comgrad/chamado-comgrad.component';
import { ComgradPainelComponent } from './components/comgrad-painel/comgrad-painel.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: 'trilhas', pathMatch: 'full' },
  { path: 'trilhas', component: TrilhasListComponent, canActivate: [AuthGuard] },
  {
    path: 'solicitar-trilhas',
    component: NotImplementedComponent,
    canActivate: [AuthGuard],
    data: { title: 'Solicitar trilhas' },
  },
  {
    path: 'sugerir-trilhas',
    component: NotImplementedComponent,
    canActivate: [AuthGuard],
    data: { title: 'Sugerir novas trilhas' },
  },
  {
    path: 'chamado-comgrad',
    component: ChamadoComgradComponent,
    canActivate: [AuthGuard],
    data: { title: 'Abrir chamado com a COMGRAD' }
  },
  {
    path: 'comgrad/painel',
    component: ComgradPainelComponent,
    canActivate: [AuthGuard],
    data: { title: 'Área da COMGRAD' }
  },
  { path: '**', redirectTo: 'trilhas' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

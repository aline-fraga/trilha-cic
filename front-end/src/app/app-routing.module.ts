import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';
import { NotImplementedComponent } from './components/not-implemented/not-implemented.component';

import { ChamadoComgradComponent } from './components/chamado-comgrad/chamado-comgrad.component';
import { ComgradPainelComponent } from './components/comgrad-painel/comgrad-painel.component';

const routes: Routes = [
  { path: '', redirectTo: 'trilhas', pathMatch: 'full' },
  { path: 'trilhas', component: TrilhasListComponent },
  {
    path: 'solicitar-trilhas',
    component: NotImplementedComponent,
    data: { title: 'Solicitar trilhas' }
  },
  {
    path: 'sugerir-trilhas',
    component: NotImplementedComponent,
    data: { title: 'Sugerir novas trilhas' }
  },
  {
    path: 'chamado-comgrad',
    component: ChamadoComgradComponent,
    data: { title: 'Abrir chamado com a COMGRAD' }
  },
  {
    path: 'comgrad/painel',
    component: ComgradPainelComponent,
    data: { title: 'Área da COMGRAD' }
  },
  { path: '**', redirectTo: 'trilhas' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';

const routes: Routes = [
  { path: '', component: TrilhasListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

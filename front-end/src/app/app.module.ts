import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { CurriculoComponent } from './components/curriculo/curriculo.component';
import { LoginComponent } from './components/login/login.component';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';
import { TrilhaCardComponent } from './components/trilha-card/trilha-card.component';
import { DisciplinaCardComponent } from './components/disciplina-card/disciplina-card.component';
import { NotImplementedComponent } from './components/not-implemented/not-implemented.component';
import { GerenciarTrilhasComponent } from './components/gerenciar-trilhas/gerenciar-trilhas.component';

@NgModule({
  declarations: [
    AppComponent,
    CurriculoComponent,
    LoginComponent,
    TrilhasListComponent,
    TrilhaCardComponent,
    DisciplinaCardComponent,
    NotImplementedComponent,
    GerenciarTrilhasComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}

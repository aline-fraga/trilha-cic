import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TrilhasListComponent } from './components/trilhas-list/trilhas-list.component';
import { TrilhaCardComponent } from './components/trilha-card/trilha-card.component';
import { DisciplinaCardComponent } from './components/disciplina-card/disciplina-card.component';
import { NotImplementedComponent } from './components/not-implemented/not-implemented.component';

@NgModule({
  declarations: [
    AppComponent,
    TrilhasListComponent,
    TrilhaCardComponent,
    DisciplinaCardComponent,
    NotImplementedComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

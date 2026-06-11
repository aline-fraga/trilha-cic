import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComgradPainelComponent } from './comgrad-painel.component';

describe('ComgradPainelComponent', () => {
  let component: ComgradPainelComponent;
  let fixture: ComponentFixture<ComgradPainelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComgradPainelComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ComgradPainelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

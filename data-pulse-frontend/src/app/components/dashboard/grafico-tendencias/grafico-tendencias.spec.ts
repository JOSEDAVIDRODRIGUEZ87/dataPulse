import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraficoTendencias } from './grafico-tendencias';

describe('GraficoTendencias', () => {
  let component: GraficoTendencias;
  let fixture: ComponentFixture<GraficoTendencias>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GraficoTendencias],
    }).compileComponents();

    fixture = TestBed.createComponent(GraficoTendencias);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

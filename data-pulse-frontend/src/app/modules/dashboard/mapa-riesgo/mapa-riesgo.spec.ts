import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaRiesgo } from './mapa-riesgo';

describe('MapaRiesgo', () => {
  let component: MapaRiesgo;
  let fixture: ComponentFixture<MapaRiesgo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapaRiesgo],
    }).compileComponents();

    fixture = TestBed.createComponent(MapaRiesgo);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

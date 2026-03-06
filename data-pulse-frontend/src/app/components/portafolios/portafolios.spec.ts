import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Portafolios } from './portafolios';

describe('Portafolios', () => {
  let component: Portafolios;
  let fixture: ComponentFixture<Portafolios>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Portafolios],
    }).compileComponents();

    fixture = TestBed.createComponent(Portafolios);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

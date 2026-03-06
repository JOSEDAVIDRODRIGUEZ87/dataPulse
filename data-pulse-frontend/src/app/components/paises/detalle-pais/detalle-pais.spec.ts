import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetallePais } from './detalle-pais';

describe('DetallePais', () => {
  let component: DetallePais;
  let fixture: ComponentFixture<DetallePais>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DetallePais],
    }).compileComponents();

    fixture = TestBed.createComponent(DetallePais);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

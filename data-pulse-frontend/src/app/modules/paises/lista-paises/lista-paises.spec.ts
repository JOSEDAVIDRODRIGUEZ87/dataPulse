import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaPaises } from './lista-paises';

describe('ListaPaises', () => {
  let component: ListaPaises;
  let fixture: ComponentFixture<ListaPaises>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaPaises],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaPaises);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

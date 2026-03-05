import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TablaRanking } from './tabla-ranking';

describe('TablaRanking', () => {
  let component: TablaRanking;
  let fixture: ComponentFixture<TablaRanking>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TablaRanking],
    }).compileComponents();

    fixture = TestBed.createComponent(TablaRanking);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { TestBed } from '@angular/core/testing';

import { Riesgo } from './riesgo';

describe('Riesgo', () => {
  let service: Riesgo;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Riesgo);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

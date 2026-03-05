import { TestBed } from '@angular/core/testing';

import { Portafolio } from './portafolio';

describe('Portafolio', () => {
  let service: Portafolio;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Portafolio);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

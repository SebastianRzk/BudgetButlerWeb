import { TestBed } from '@angular/core/testing';

import { KategorieService } from './kategorie.service';

describe('KategorieService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: KategorieService = TestBed.get(KategorieService);
    expect(service).toBeTruthy();
  });
});

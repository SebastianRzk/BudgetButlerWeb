import { TestBed } from '@angular/core/testing';

import { KategorieService } from './kategorie.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('KategorieService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule]
  }));

  it('should be created', () => {
    const service: KategorieService = TestBed.get(KategorieService);
    expect(service).toBeTruthy();
  });
});

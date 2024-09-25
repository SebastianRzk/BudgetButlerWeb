import { TestBed } from '@angular/core/testing';

import { KategorieService } from './kategorie.service';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('KategorieService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [],
    providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
}));

  it('should be created', () => {
    const service: KategorieService = TestBed.get(KategorieService);
    expect(service).toBeTruthy();
  });
});

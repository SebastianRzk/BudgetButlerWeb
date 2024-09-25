import {TestBed} from '@angular/core/testing';

import {EinzelbuchungService} from './einzelbuchung.service';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('EinzelbuchungService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [MatSnackBarModule],
    providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
}));

  it('should be created', () => {
    const service: EinzelbuchungService = TestBed.get(EinzelbuchungService);
    expect(service).toBeTruthy();
  });
});

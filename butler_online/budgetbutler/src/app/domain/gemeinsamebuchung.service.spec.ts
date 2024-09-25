import {TestBed} from '@angular/core/testing';

import {GemeinsamebuchungService} from './gemeinsamebuchung.service';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('GemeinsamebuchungService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [MatSnackBarModule],
    providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
}));

  it('should be created', () => {
    const service: GemeinsamebuchungService = TestBed.get(GemeinsamebuchungService);
    expect(service).toBeTruthy();
  });
});

import {TestBed} from '@angular/core/testing';

import {PartnerService} from './partner.service';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import {RouterTestingModule} from '@angular/router/testing';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('PartnerService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [MatSnackBarModule,
        RouterTestingModule],
    providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
}));

  it('should be created', () => {
    const service: PartnerService = TestBed.get(PartnerService);
    expect(service).toBeTruthy();
  });
});

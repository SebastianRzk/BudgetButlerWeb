import { TestBed } from '@angular/core/testing';

import { EinzelbuchungserviceService } from './einzelbuchungservice.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatSnackBarModule } from '@angular/material';

describe('EinzelbuchungserviceService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule,
      MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: EinzelbuchungserviceService = TestBed.get(EinzelbuchungserviceService);
    expect(service).toBeTruthy();
  });
});

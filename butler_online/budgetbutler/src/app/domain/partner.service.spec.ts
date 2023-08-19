import {TestBed} from '@angular/core/testing';

import {PartnerService} from './partner.service';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {RouterTestingModule} from '@angular/router/testing';

describe('PartnerService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [
      MatSnackBarModule,
      HttpClientTestingModule,
      RouterTestingModule
    ]
  }));

  it('should be created', () => {
    const service: PartnerService = TestBed.get(PartnerService);
    expect(service).toBeTruthy();
  });
});

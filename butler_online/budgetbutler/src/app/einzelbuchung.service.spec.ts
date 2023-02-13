import {TestBed} from '@angular/core/testing';

import {EinzelbuchungService} from './einzelbuchung.service';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';

describe('EinzelbuchungService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule,
      MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: EinzelbuchungService = TestBed.get(EinzelbuchungService);
    expect(service).toBeTruthy();
  });
});

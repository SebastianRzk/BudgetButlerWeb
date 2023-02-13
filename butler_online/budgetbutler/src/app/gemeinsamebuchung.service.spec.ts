import {TestBed} from '@angular/core/testing';

import {GemeinsamebuchungService} from './gemeinsamebuchung.service';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';

describe('GemeinsamebuchungService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule,
      MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: GemeinsamebuchungService = TestBed.get(GemeinsamebuchungService);
    expect(service).toBeTruthy();
  });
});

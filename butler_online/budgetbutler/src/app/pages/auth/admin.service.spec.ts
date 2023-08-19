import {TestBed} from '@angular/core/testing';

import {AdminService} from './admin.service';
import {HttpClientTestingModule} from '@angular/common/http/testing';
import {RouterTestingModule} from '@angular/router/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';

describe('AdminService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule,
      RouterTestingModule,
      MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: AdminService = TestBed.inject(AdminService);
    expect(service).toBeTruthy();
  });
});

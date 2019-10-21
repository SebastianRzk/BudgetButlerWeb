import { TestBed } from '@angular/core/testing';

import { ApiproviderService } from './apiprovider.service';

describe('ApiproviderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ApiproviderService = TestBed.get(ApiproviderService);
    expect(service).toBeTruthy();
  });
});

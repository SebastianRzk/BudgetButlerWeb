import { TestBed } from '@angular/core/testing';

import { ApiProviderService } from './api-provider.service';

describe('ApiProviderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ApiProviderService = TestBed.inject(ApiProviderService);
    expect(service).toBeTruthy();
  });
});

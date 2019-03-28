import { TestBed } from '@angular/core/testing';

import { EinzelbuchungserviceService } from './einzelbuchungservice.service';

describe('EinzelbuchungserviceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: EinzelbuchungserviceService = TestBed.get(EinzelbuchungserviceService);
    expect(service).toBeTruthy();
  });
});

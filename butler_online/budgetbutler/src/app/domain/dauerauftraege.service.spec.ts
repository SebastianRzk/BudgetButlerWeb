import { TestBed } from '@angular/core/testing';

import { DauerauftraegeService } from './dauerauftraege.service';

describe('DauerauftraegeService', () => {
  let service: DauerauftraegeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DauerauftraegeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

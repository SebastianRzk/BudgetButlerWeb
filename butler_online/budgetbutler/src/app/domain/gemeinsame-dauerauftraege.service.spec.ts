import { TestBed } from '@angular/core/testing';

import { GemeinsameDauerauftraegeService } from './gemeinsame-dauerauftraege.service';

describe('GemeinsameDauerauftraegeService', () => {
  let service: GemeinsameDauerauftraegeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GemeinsameDauerauftraegeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

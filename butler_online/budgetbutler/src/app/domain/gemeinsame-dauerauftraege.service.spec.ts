import { TestBed } from '@angular/core/testing';

import { GemeinsameDauerauftraegeService } from './gemeinsame-dauerauftraege.service';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { provideHttpClientTesting } from "@angular/common/http/testing";

describe('GemeinsameDauerauftraegeService', () => {
  let service: GemeinsameDauerauftraegeService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
    });
    service = TestBed.inject(GemeinsameDauerauftraegeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

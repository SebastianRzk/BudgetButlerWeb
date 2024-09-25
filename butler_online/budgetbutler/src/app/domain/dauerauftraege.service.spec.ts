import { TestBed } from '@angular/core/testing';

import { DauerauftraegeService } from './dauerauftraege.service';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { provideHttpClientTesting } from "@angular/common/http/testing";

describe('DauerauftraegeService', () => {
  let service: DauerauftraegeService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
    });
    service = TestBed.inject(DauerauftraegeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

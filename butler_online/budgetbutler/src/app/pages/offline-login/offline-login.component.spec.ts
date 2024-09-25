import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OfflineLoginComponent } from './offline-login.component';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { provideHttpClientTesting } from "@angular/common/http/testing";

describe('OfflineLoginComponent', () => {
  let component: OfflineLoginComponent;
  let fixture: ComponentFixture<OfflineLoginComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()],
      imports: [OfflineLoginComponent]
    });
    fixture = TestBed.createComponent(OfflineLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

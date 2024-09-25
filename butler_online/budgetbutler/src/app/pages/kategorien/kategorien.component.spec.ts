import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KategorienComponent } from './kategorien.component';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { provideHttpClientTesting } from "@angular/common/http/testing";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";

describe('KategorienComponent', () => {
  let component: KategorienComponent;
  let fixture: ComponentFixture<KategorienComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()],
      imports: [KategorienComponent, NoopAnimationsModule]
    });
    fixture = TestBed.createComponent(KategorienComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

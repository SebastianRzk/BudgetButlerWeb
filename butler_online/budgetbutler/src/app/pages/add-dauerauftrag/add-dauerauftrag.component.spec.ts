import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddDauerauftragComponent } from './add-dauerauftrag.component';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";
import { provideHttpClientTesting } from "@angular/common/http/testing";
import { provideNativeDateAdapter } from "@angular/material/core";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";

describe('AdddauerauftragComponent', () => {
  let component: AddDauerauftragComponent;
  let fixture: ComponentFixture<AddDauerauftragComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting(), provideNativeDateAdapter()],
      imports: [AddDauerauftragComponent, NoopAnimationsModule]
    });
    fixture = TestBed.createComponent(AddDauerauftragComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

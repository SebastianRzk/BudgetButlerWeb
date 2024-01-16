import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OfflineLoginComponent } from './offline-login.component';

describe('OfflineLoginComponent', () => {
  let component: OfflineLoginComponent;
  let fixture: ComponentFixture<OfflineLoginComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OfflineLoginComponent]
    });
    fixture = TestBed.createComponent(OfflineLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

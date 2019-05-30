import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PartnernameComponent } from './partnername.component';

describe('PartnernameComponent', () => {
  let component: PartnernameComponent;
  let fixture: ComponentFixture<PartnernameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PartnernameComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PartnernameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

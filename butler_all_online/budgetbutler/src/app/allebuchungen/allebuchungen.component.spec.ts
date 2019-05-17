import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllebuchungenComponent } from './allebuchungen.component';

describe('AllebuchungenComponent', () => {
  let component: AllebuchungenComponent;
  let fixture: ComponentFixture<AllebuchungenComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllebuchungenComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllebuchungenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

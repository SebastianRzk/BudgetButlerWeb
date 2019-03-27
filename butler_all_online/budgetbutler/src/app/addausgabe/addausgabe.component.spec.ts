import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddausgabeComponent } from './addausgabe.component';

describe('AddausgabeComponent', () => {
  let component: AddausgabeComponent;
  let fixture: ComponentFixture<AddausgabeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddausgabeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddausgabeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

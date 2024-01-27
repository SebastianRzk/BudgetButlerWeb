import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddDauerauftragComponent } from './add-dauerauftrag.component';

describe('AdddauerauftragComponent', () => {
  let component: AddDauerauftragComponent;
  let fixture: ComponentFixture<AddDauerauftragComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddDauerauftragComponent]
    });
    fixture = TestBed.createComponent(AddDauerauftragComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErweiterteBuchungComponent } from './erweiterte-buchung.component';

describe('ErweiterteBuchungComponent', () => {
  let component: ErweiterteBuchungComponent;
  let fixture: ComponentFixture<ErweiterteBuchungComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ErweiterteBuchungComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ErweiterteBuchungComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

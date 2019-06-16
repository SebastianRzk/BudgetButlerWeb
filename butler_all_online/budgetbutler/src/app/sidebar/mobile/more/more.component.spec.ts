import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MoreComponent } from './more.component';
import { RouterTestingModule } from '@angular/router/testing';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

describe('MoreComponent', () => {
  let component: MoreComponent;
  let fixture: ComponentFixture<MoreComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MoreComponent],
      imports: [RouterTestingModule,
        MatButtonModule,
        MatIconModule]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MoreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

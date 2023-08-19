import {TestBed} from '@angular/core/testing';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {NotificationService} from './notification.service';


describe('NotificationService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: NotificationService = TestBed.inject(NotificationService);
    expect(service).toBeTruthy();
  });
});

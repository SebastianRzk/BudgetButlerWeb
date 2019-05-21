import { TestBed } from '@angular/core/testing';
import { MatSnackBarModule } from '@angular/material';
import { NotificationService } from './notification.service';


describe('NotificationService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [MatSnackBarModule]
  }));

  it('should be created', () => {
    const service: NotificationService = TestBed.get(NotificationService);
    expect(service).toBeTruthy();
  });
});

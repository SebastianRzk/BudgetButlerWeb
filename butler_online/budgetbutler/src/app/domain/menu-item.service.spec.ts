import { TestBed } from '@angular/core/testing';

import { MenuItemService } from './menu-item.service';

describe('MenuitemService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MenuItemService = TestBed.inject(MenuItemService);
    expect(service).toBeTruthy();
  });
});

import { Injectable } from '@angular/core';

const apiUrl = '/api/';
@Injectable({
  providedIn: 'root'
})
export class ApiproviderService {

  constructor() { }

  getBaseUrl(): string {
    return apiUrl;
  }

  getUrl(relPath: string): string {
    return apiUrl + relPath;
  }
}

import { Component, OnInit } from '@angular/core';
import { Sort } from '@angular/material';
import { Einzelbuchung } from '../model';
import { EinzelbuchungserviceService as EinzelbuchungService } from '../einzelbuchungservice.service';
import { NotificationService } from '../notification.service';

@Component({
  selector: 'app-allebuchungen',
  templateUrl: './allebuchungen.component.html',
  styleUrls: ['./allebuchungen.component.css']
})
export class AllebuchungenComponent implements OnInit {

  displayedColumns: string[] = ['Datum', 'Name', 'Kategorie', 'Wert'];
  einzelbuchungen: Einzelbuchung[];

  constructor(private einzelbuchungService: EinzelbuchungService, private notificationService: NotificationService) {
  }

  ngOnInit(): void {
    this.einzelbuchungService.getAll().subscribe(
      data => this.einzelbuchungen = data,
      error => this.notificationService.handleServerResult(error, 'Laden aller Einzelbuchungen'));
  }

  toLocaleString(date: string){
    return new Date(date).toLocaleDateString('de-DE');
  }
}

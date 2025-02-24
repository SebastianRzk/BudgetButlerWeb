import {Component, Input} from '@angular/core';
import {BuchungsUebersicht} from '../../../domain/model';
import {DecimalPipe, KeyValuePipe} from '@angular/common';
import {MatCard, MatCardContent, MatCardHeader, MatCardTitle} from '@angular/material/card';
import {MatDivider} from "@angular/material/divider";

@Component({
  selector: 'app-ausgaben-uebersicht',
  templateUrl: './ausgaben-uebersicht.component.html',
  styleUrls: ['./ausgaben-uebersicht.component.css'],
  imports: [MatCard, MatCardTitle, MatCardContent, DecimalPipe, KeyValuePipe, MatCardHeader, MatDivider]
})
export class AusgabenUebersichtComponent {
  @Input({required: true})
  uebersicht!: BuchungsUebersicht;

}

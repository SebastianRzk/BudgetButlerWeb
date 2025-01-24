import { Component, inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { KategorieService } from '../../domain/kategorie.service';
import { MatIcon } from '@angular/material/icon';
import {
  MatCell, MatCellDef,
  MatColumnDef,
  MatHeaderCell,
  MatHeaderCellDef,
  MatHeaderRow, MatHeaderRowDef,
  MatRow, MatRowDef,
  MatTable
} from '@angular/material/table';
import { MatButton } from '@angular/material/button';
import { MatInput } from '@angular/material/input';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';

@Component({
    selector: 'app-kategorien',
    templateUrl: './kategorien.component.html',
    styleUrls: ['./kategorien.component.css'],
  imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, FormsModule, ReactiveFormsModule, MatFormField, MatLabel, MatInput, MatButton, MatTable, MatColumnDef, MatHeaderCell, MatCell, MatIcon, MatHeaderRow, MatRow, MatHeaderCellDef, MatCellDef, MatHeaderRowDef, MatRowDef]
})
export class KategorienComponent implements OnInit{

  private kategorienService = inject(KategorieService);

  kategorienForm = new FormGroup({
    name: new FormControl('', Validators.required),
  });


  displayedColumns: string[] = ['Datum', 'Aktion'];
  kategorien$ = this.kategorienService.kategorien$;

  ngOnInit() {
    this.kategorienService.refresh();
  }

  onFormSubmit() {
    if (!this.kategorienForm.valid) {
      return;
    }

    this.kategorienService.add(this.kategorienForm.get('name')!.value!);
    this.kategorienForm.reset();
  }

  delete(id: string) {
    this.kategorienService.delete(id);
  }


}

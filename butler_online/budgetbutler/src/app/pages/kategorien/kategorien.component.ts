import { Component, inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { KategorieService } from '../../domain/kategorie.service';
import { AsyncPipe } from '@angular/common';
import { MatIcon } from '@angular/material/icon';
import { MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow } from '@angular/material/table';
import { MatButton } from '@angular/material/button';
import { MatInput } from '@angular/material/input';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatCard, MatCardHeader, MatCardTitle, MatCardContent } from '@angular/material/card';

@Component({
    selector: 'app-kategorien',
    templateUrl: './kategorien.component.html',
    styleUrls: ['./kategorien.component.css'],
    standalone: true,
    imports: [MatCard, MatCardHeader, MatCardTitle, MatCardContent, FormsModule, ReactiveFormsModule, MatFormField, MatLabel, MatInput, MatButton, MatTable, MatColumnDef, MatHeaderCellDef, MatHeaderCell, MatCellDef, MatCell, MatIcon, MatHeaderRowDef, MatHeaderRow, MatRowDef, MatRow, AsyncPipe]
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

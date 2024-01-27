import { Component, inject, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { KategorieService } from '../../domain/kategorie.service';

@Component({
  selector: 'app-kategorien',
  templateUrl: './kategorien.component.html',
  styleUrls: ['./kategorien.component.css']
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

    this.kategorienService.add(this.kategorienForm.get('name').value);
    this.kategorienForm.reset();
  }

  delete(id: string) {
    this.kategorienService.delete(id);
  }


}

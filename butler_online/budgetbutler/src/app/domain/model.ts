export class Einzelbuchung {
  public id: number;
  public name: string;
  public datum: Date;
  public kategorie: string;
  public wert: number;
}

export class EinzelbuchungAnlegen {
  public name: string;
  public datum: Date;
  public kategorie: string;
  public wert: number;
}

export class EinzelbuchungLoeschen {
  public id: number;
}

export interface GemeinsameBuchungAnlegen {
  readonly name: string;
  readonly datum: Date;
  readonly kategorie: string;
  readonly wert: number;
  readonly zielperson: string;
}

export interface GemeinsameBuchung {
  readonly name: string;
  readonly datum: Date;
  readonly kategorie: string;
  readonly wert: number;
  readonly zielperson: string;
  readonly id: number;
  readonly user: string;
  readonly isCreatedByDifferentPerson: boolean;
}


export class GemeinsameBuchungLoeschen {
  public id: number;
}

export class Result {
  public result: string;
  public message: string;
}

export const ERROR_RESULT: Result = {result: 'ERROR', message: 'Fehler beim Erstellen der Buchung'};
export const ERROR_LOADING_EINZELBUCHUNGEN: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der Einzelbuchungen'
};
export const ERROR_LOADING_GEMEINSAME_BUCHUNGEN: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der gemeinsamen Buchungen'
};
export const ERROR_LOGIN_RESULT: Result = {result: 'FEHLER', message: 'Fehler beim Login'};

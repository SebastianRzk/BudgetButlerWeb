export interface Einzelbuchung {
   id: string;
   name: string;
   datum: Date;
   kategorie: string;
   wert: number;
}

export interface EinzelbuchungAnlegen {
   name: string;
   datum: Date;
   kategorie: string;
   wert: number;
}

export interface EinzelbuchungLoeschen {
   id: string;
}

export interface DauerauftragLoeschen {
   id: string;
}

export interface GemeinsameBuchungAnlegen {
  readonly name: string;
  readonly datum: Date;
  readonly kategorie: string;
  readonly wert: number;
  readonly eigeneBuchung: boolean;
}

export interface GemeinsameBuchung {
  readonly name: string;
  readonly datum: Date;
  readonly kategorie: string;
  readonly wert: number;
  readonly zielperson: string;
  readonly id: string;
  readonly user: string;
  readonly isCreatedByDifferentPerson: boolean;
}

export interface DauerauftragAnlegen {
   name: string;
   startDatum: Date;
   endeDatum: Date;
   kategorie: string;
   wert: number;
   rhythmus: string;
}

export interface GemeinsamerDauerauftragAnlegen {
   name: string;
   startDatum: Date;
   endeDatum: Date;
   kategorie: string;
   wert: number;
   rhythmus: string;
   eigeneBuchung: boolean;
}

export interface Dauerauftrag {
   id: string;
   name: string;
   startDatum: Date;
   endeDatum: Date;
   kategorie: string;
   wert: number;
   rhythmus: string;
}

export interface GemeinsamerDauerauftrag {
   id: string;
   name: string;
   startDatum: Date;
   endeDatum: Date;
   kategorie: string;
   wert: number;
   rhythmus: string;
   user: string;
   zielperson: string;
}


export interface GemeinsameBuchungLoeschen {
   id: string;
}

export interface Result {
   result: string;
   message: string;
}

export const ERROR_RESULT: Result = {result: 'ERROR', message: 'Fehler beim Erstellen der Buchung'};
export const ERROR_LOADING_EINZELBUCHUNGEN: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der Einzelbuchungen'
};
export const ERROR_LOADING_DAUERAUFTRAEGE: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der Daueraufträge'
};
export const ERROR_LOADING_GEMEINSME_DAUERAUFTRAEGE: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der gemeinsamen Daueraufträge'
};
export const ERROR_LOADING_GEMEINSAME_BUCHUNGEN: Result = {
  result: 'ERROR',
  message: 'Fehler beim Laden der gemeinsamen Buchungen'
};
export const ERROR_LOGIN_RESULT: Result = {result: 'FEHLER', message: 'Fehler beim Login'};

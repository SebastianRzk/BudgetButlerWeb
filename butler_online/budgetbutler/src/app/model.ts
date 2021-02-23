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

export class GemeinsameBuchungAnlegen {
    public name: string;
    public datum: Date;
    public kategorie: string;
    public wert: number;
    public zielperson: string;
}

export class GemeinsameBuchung extends GemeinsameBuchungAnlegen {
    public id: number;
    public user: string;
}

export class GemeinsameBuchungLoeschen {
    public id: number;
}

export class Result {
    public result: string;
    public message: string;
}

export const ERROR_RESULT: Result = { result: 'ERROR', message: 'Fehler beim Erstellen der Buchung' };
export const ERROR_LOADING_EINZELBUCHUNGEN: Result = { result: 'ERROR', message: 'Fehler beim Laden der Einzelbuchungen' };
export const ERROR_LOADING_GEMEINSAME_BUCHUNGEN: Result = { result: 'ERROR', message: 'Fehler beim Laden der gemeinsamen Buchungen' };
export const ERROR_LOGIN_RESULT: Result = { result: 'FEHLER', message: 'Fehler beim Login' };

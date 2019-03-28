export class Einzelbuchung {
    public id: number;
    public name: string;
    public datum: Date;
    public kategorie: string;
    public wert: number;
}

export class Result {
    public result: string;
    public message: string;
}

export const ERROR_RESULT: Result = {result: 'ERROR', message: 'Übertragen der Daten'};
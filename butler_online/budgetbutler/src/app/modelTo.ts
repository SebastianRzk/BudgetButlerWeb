export class EinzelbuchungTO {
    public id: number;
    public name: string;
    public datum: string;
    public kategorie: string;
    public wert: number;
}

export class EinzelbuchungAnlegenTO {
    public name: string;
    public datum: string;
    public kategorie: string;
    public wert: number;
}

export class GemeinsameBuchungAnlegenTO {
    public name: string;
    public datum: string;
    public kategorie: string;
    public wert: number;
    public zielperson: string;
}
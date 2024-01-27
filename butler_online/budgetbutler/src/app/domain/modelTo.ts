export class EinzelbuchungTO {
  public id: string;
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
  public eigeneBuchung: boolean;
}


export interface GemeinsameBuchungTO {
  readonly name: string;
  readonly datum: Date;
  readonly kategorie: string;
  readonly wert: number;
  readonly zielperson: string;
  readonly id: string;
  readonly user: string;
}

export interface AddUserDataTo {
  readonly username: string;
  readonly email: string;
  readonly password: string;
}

export class DauerauftragAnlegenTO {
  public name: string;
  public startDatum: string;
  public endeDatum: string;
  public kategorie: string;
  public wert: number;
  public rhythmus: string;
}

export class DauerauftragTO {
  public id: string;
  public name: string;
  public startDatum: string;
  public endeDatum: string;
  public kategorie: string;
  public wert: number;
  public rhythmus: string;
}

export class GemeinsamerDauerauftragAnlegenTO {
  public name: string;
  public startDatum: string;
  public endeDatum: string;
  public kategorie: string;
  public wert: number;
  public rhythmus: string;
  public eigeneBuchung: boolean;
}

export class GemeinsamerDauerauftragTO {
  public id: string;
  public name: string;
  public startDatum: string;
  public endeDatum: string;
  public kategorie: string;
  public wert: number;
  public rhythmus: string;
  public user: string;
  public zielperson: string;
}


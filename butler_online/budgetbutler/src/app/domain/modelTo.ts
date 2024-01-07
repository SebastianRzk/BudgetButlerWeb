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


export interface KategorieTo {
  readonly id: string;
  readonly name: string;
  readonly user: string;
}

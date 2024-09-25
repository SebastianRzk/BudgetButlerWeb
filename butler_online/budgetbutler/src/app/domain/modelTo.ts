export interface EinzelbuchungTO {
  id: string;
  name: string;
  datum: string;
  kategorie: string;
  wert: number;
}

export interface EinzelbuchungAnlegenTO {
  name: string;
  datum: string;
  kategorie: string;
  wert: number;
}

export interface GemeinsameBuchungAnlegenTO {
  name: string;
  datum: string;
  kategorie: string;
  wert: number;
  eigeneBuchung: boolean;
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

export interface DauerauftragAnlegenTO {
  name: string;
  startDatum: string;
  endeDatum: string;
  kategorie: string;
  wert: number;
  rhythmus: string;
}

export interface DauerauftragTO {
  id: string;
  name: string;
  startDatum: string;
  endeDatum: string;
  kategorie: string;
  wert: number;
  rhythmus: string;
}

export interface GemeinsamerDauerauftragAnlegenTO {
  name: string;
  startDatum: string;
  endeDatum: string;
  kategorie: string;
  wert: number;
  rhythmus: string;
  eigeneBuchung: boolean;
}

export interface GemeinsamerDauerauftragTO {
  id: string;
  name: string;
  startDatum: string;
  endeDatum: string;
  kategorie: string;
  wert: number;
  rhythmus: string;
  user: string;
  zielperson: string;
}


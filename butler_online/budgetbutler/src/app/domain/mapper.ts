import {
  Dauerauftrag,
  DauerauftragAnlegen, Einzelbuchung,
  EinzelbuchungAnlegen,
  GemeinsameBuchung,
  GemeinsameBuchungAnlegen, GemeinsamerDauerauftrag,
  GemeinsamerDauerauftragAnlegen
} from './model';
import {
  DauerauftragAnlegenTO, DauerauftragTO,
  EinzelbuchungAnlegenTO, EinzelbuchungTO,
  GemeinsameBuchungAnlegenTO,
  GemeinsameBuchungTO, GemeinsamerDauerauftragAnlegenTO, GemeinsamerDauerauftragTO
} from './modelTo';

const toISOFormat = (datum: Date) => [
  datum.getFullYear(),
  ('0' + (datum.getMonth() + 1)).slice(-2),
  ('0' + datum.getDate()).slice(-2)
].join('-');

export function toEinzelbuchungAnlegenTO(einzelbuchung: EinzelbuchungAnlegen): EinzelbuchungAnlegenTO {
  return {
    datum: toISOFormat(einzelbuchung.datum),
    name: einzelbuchung.name,
    kategorie: einzelbuchung.kategorie,
    wert: einzelbuchung.wert
  };
}

export const toGemeinsameBuchungAnlegenTO = (gemeinsameBuchungAnlegen: GemeinsameBuchungAnlegen): GemeinsameBuchungAnlegenTO => {
  return {
    name: gemeinsameBuchungAnlegen.name,
    datum: toISOFormat(gemeinsameBuchungAnlegen.datum),
    kategorie: gemeinsameBuchungAnlegen.kategorie,
    wert: gemeinsameBuchungAnlegen.wert,
    eigeneBuchung: gemeinsameBuchungAnlegen.eigeneBuchung,
  };
};

export function toGemeinsameBuchung(gemeinsameBuchungTO: GemeinsameBuchungTO): GemeinsameBuchung {
  return {
    name: gemeinsameBuchungTO.name,
    datum: gemeinsameBuchungTO.datum,
    user: gemeinsameBuchungTO.user,
    zielperson: gemeinsameBuchungTO.zielperson,
    wert: gemeinsameBuchungTO.wert,
    kategorie: gemeinsameBuchungTO.kategorie,
    id: gemeinsameBuchungTO.id,
    isCreatedByDifferentPerson: gemeinsameBuchungTO.user !== gemeinsameBuchungTO.zielperson
  };
}

export const toDauerauftragAnlegenTO = (dauerauftragAnlegen: DauerauftragAnlegen): DauerauftragAnlegenTO => {
  return {
    name: dauerauftragAnlegen.name,
    kategorie: dauerauftragAnlegen.kategorie,
    wert: dauerauftragAnlegen.wert,
    endeDatum: toISOFormat(dauerauftragAnlegen.endeDatum),
    startDatum: toISOFormat(dauerauftragAnlegen.startDatum),
    rhythmus: dauerauftragAnlegen.rhythmus
  }
}

export const toGemeinsamerDauerauftragAnlegenTO = (dauerauftragAnlegen: GemeinsamerDauerauftragAnlegen): GemeinsamerDauerauftragAnlegenTO => {
  return {
    name: dauerauftragAnlegen.name,
    kategorie: dauerauftragAnlegen.kategorie,
    wert: dauerauftragAnlegen.wert,
    endeDatum: toISOFormat(dauerauftragAnlegen.endeDatum),
    startDatum: toISOFormat(dauerauftragAnlegen.startDatum),
    rhythmus: dauerauftragAnlegen.rhythmus,
    eigeneBuchung: dauerauftragAnlegen.eigeneBuchung
  }
}

export const toDauerauftrag = (dauerauftragTo: DauerauftragTO): Dauerauftrag => {
  return {
    id: dauerauftragTo.id,
    name: dauerauftragTo.name,
    kategorie: dauerauftragTo.kategorie,
    wert: dauerauftragTo.wert,
    endeDatum: new Date(dauerauftragTo.endeDatum),
    startDatum: new Date(dauerauftragTo.startDatum),
    rhythmus: dauerauftragTo.rhythmus
  }
}
export const toGemeinsamerDauerauftrag = (dauerauftragTo: GemeinsamerDauerauftragTO): GemeinsamerDauerauftrag => {
  return {
    id: dauerauftragTo.id,
    name: dauerauftragTo.name,
    kategorie: dauerauftragTo.kategorie,
    wert: dauerauftragTo.wert,
    endeDatum: new Date(dauerauftragTo.endeDatum),
    startDatum: new Date(dauerauftragTo.startDatum),
    rhythmus: dauerauftragTo.rhythmus,
    user: dauerauftragTo.user,
    zielperson: dauerauftragTo.zielperson
  }
}

export const toEinzelbuchung = (einzelbuchungTo: EinzelbuchungTO): Einzelbuchung => {
  return {
    id: einzelbuchungTo.id,
    datum: new Date(einzelbuchungTo.datum),
    name: einzelbuchungTo.name,
    kategorie: einzelbuchungTo.kategorie,
    wert: einzelbuchungTo.wert,
  }
}

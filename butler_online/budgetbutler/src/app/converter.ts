import {EinzelbuchungAnlegen, GemeinsameBuchungAnlegen} from './model';
import {EinzelbuchungAnlegenTO, GemeinsameBuchungAnlegenTO} from './modelTo';

const toISOFormat = (datum: Date) => '' + datum.getFullYear() + '-' + (datum.getMonth() + 1) + '-' + datum.getDate();

export function toEinzelbuchungAnlegenTO(einzelbuchung: EinzelbuchungAnlegen): EinzelbuchungAnlegenTO {
  if (typeof einzelbuchung.datum === 'string') {
    return {
      datum: einzelbuchung.datum,
      name: einzelbuchung.name,
      kategorie: einzelbuchung.kategorie,
      wert: einzelbuchung.wert
    };
  }
  return {
    datum: toISOFormat(einzelbuchung.datum),
    name: einzelbuchung.name,
    kategorie: einzelbuchung.kategorie,
    wert: einzelbuchung.wert
  };
}

export const toGemeinsameBuchungAnlegenTO = (gemeinsameBuchungAnlegen: GemeinsameBuchungAnlegen): GemeinsameBuchungAnlegenTO => {
  if (typeof gemeinsameBuchungAnlegen.datum === 'string') {
    return {
      name: gemeinsameBuchungAnlegen.name,
      datum: gemeinsameBuchungAnlegen.datum,
      kategorie: gemeinsameBuchungAnlegen.kategorie,
      wert: gemeinsameBuchungAnlegen.wert,
      zielperson: gemeinsameBuchungAnlegen.zielperson,
    };
  }
  return {
    name: gemeinsameBuchungAnlegen.name,
    datum: toISOFormat(gemeinsameBuchungAnlegen.datum),
    kategorie: gemeinsameBuchungAnlegen.kategorie,
    wert: gemeinsameBuchungAnlegen.wert,
    zielperson: gemeinsameBuchungAnlegen.zielperson,
  };

};


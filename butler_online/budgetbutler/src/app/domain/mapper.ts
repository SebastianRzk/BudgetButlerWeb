import {EinzelbuchungAnlegen, GemeinsameBuchung, GemeinsameBuchungAnlegen} from './model';
import {EinzelbuchungAnlegenTO, GemeinsameBuchungAnlegenTO, GemeinsameBuchungTO} from './modelTo';

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

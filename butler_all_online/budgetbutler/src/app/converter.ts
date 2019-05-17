import { Einzelbuchung } from "./model";
import { EinzelbuchungTO } from './modelTo';

const toISOFormat = (datum: Date) => "" + datum.getFullYear() + "-" + (datum.getMonth() + 1) + "-" + datum.getDate();

export const toEinzelbuchungTO = (einzelbuchung: Einzelbuchung): EinzelbuchungTO => {
    return {
        id: einzelbuchung.id,
        datum: toISOFormat(einzelbuchung.datum),
        name: einzelbuchung.name,
        kategorie: einzelbuchung.kategorie,
        wert: einzelbuchung.wert
    }
}


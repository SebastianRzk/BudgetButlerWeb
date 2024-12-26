use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;

pub fn map_positive(value: &Indiziert<Einzelbuchung>) -> Indiziert<Einzelbuchung> {
    Indiziert {
        value: Einzelbuchung {
            betrag: value.value.betrag.abs(),
            datum: value.value.datum.clone(),
            kategorie: value.value.kategorie.clone(),
            name: value.value.name.clone(),
        },
        dynamisch: value.dynamisch,
        index: value.index,
    }
}

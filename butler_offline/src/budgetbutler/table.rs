use crate::budgetbutler::database::select::functions::grouper::betrag_summe_gruppierung;
use crate::budgetbutler::database::select::functions::keyextractors::kategorie_aggregation;
use crate::budgetbutler::database::select::selector::Selector;
use crate::budgetbutler::view::farbe::FarbenSelektor;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::metamodel::chart::AusgabeAusKategorie;
use crate::model::primitives::kategorie::Kategorie;

pub fn berechne_buchungen_nach_kategorie(
    slektion: Selector<Indiziert<Einzelbuchung>>,
    farben_selektor: &FarbenSelektor,
) -> Vec<AusgabeAusKategorie> {
    let buchungen = slektion.group_by(kategorie_aggregation, betrag_summe_gruppierung);
    let mut sortierte_kategorien = buchungen.keys().into_iter().collect::<Vec<&Kategorie>>();
    sortierte_kategorien.sort();

    let mut result: Vec<AusgabeAusKategorie> = Vec::new();
    for kategorie in sortierte_kategorien {
        let buchung = buchungen.get(kategorie).unwrap();
        result.push(AusgabeAusKategorie {
            color: farben_selektor.get(kategorie).clone(),
            wert: buchung.clone(),
            kategorie: kategorie.clone(),
        });
    }
    result
}

use crate::budgetbutler::pages::sparen::uebersicht_sparbuchungen::{
    MonatsZusammenfassung, UebersichtSparbuchungenViewResult,
};
use crate::io::disk::primitive::sparbuchungtyp::write_sparbuchungtyp;
use crate::io::html::input::select::Select;
use crate::model::database::sparbuchung::Sparbuchung;
use crate::model::indiziert::Indiziert;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_sparbuchungen.html")]
pub struct UebersichtSparbuchungTemplate {
    pub database_id: String,
    pub jahre: Select<i32>,
    pub alles: Vec<MonatTemplate>,
}

pub struct MonatTemplate {
    pub name: String,
    pub sparbuchungen: Vec<SparbuchungTemplate>,
}

pub struct SparbuchungTemplate {
    pub index: u32,
    pub datum: String,
    pub name: String,
    pub konto: String,
    pub wert: String,
    pub typ: String,
    pub dynamisch: bool,
}

pub fn render_uebersicht_sparbuchungen_template(
    view_result: UebersichtSparbuchungenViewResult,
) -> String {
    let as_template: UebersichtSparbuchungTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_monat_to_template(monat: &MonatsZusammenfassung) -> MonatTemplate {
    MonatTemplate {
        name: monat.monat.monat.clone(),
        sparbuchungen: monat
            .buchungen
            .iter()
            .map(|x| map_buchung_to_template(x))
            .collect(),
    }
}

fn map_buchung_to_template(buchung: &Indiziert<Sparbuchung>) -> SparbuchungTemplate {
    SparbuchungTemplate {
        datum: buchung.value.datum.to_german_string(),
        index: buchung.index,
        wert: buchung.value.wert.to_german_string(),
        dynamisch: buchung.dynamisch,
        name: buchung.value.name.get_name().clone(),
        konto: buchung.value.konto.konto_name.name.clone(),
        typ: write_sparbuchungtyp(&buchung.value.typ).element,
    }
}

fn map_to_template(
    view_result: UebersichtSparbuchungenViewResult,
) -> UebersichtSparbuchungTemplate {
    let alles: Vec<MonatTemplate> = view_result
        .liste
        .iter()
        .map(|x| map_monat_to_template(&x))
        .collect();
    UebersichtSparbuchungTemplate {
        alles,
        database_id: view_result.database_version.as_string(),
        jahre: Select::new(
            view_result.verfuegbare_jahre.clone(),
            Some(view_result.selektiertes_jahr),
        ),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_sparbuchungen::{
        MonatsZusammenfassung, UebersichtSparbuchungenViewResult,
    };
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::builder::u_betrag;
    use crate::model::primitives::datum::{monats_name, Datum};
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    fn test_map_to_template() {
        let view_result = UebersichtSparbuchungenViewResult {
            liste: vec![MonatsZusammenfassung {
                monat: monats_name("Januar"),
                buchungen: vec![Indiziert {
                    index: 0,
                    dynamisch: false,
                    value: Sparbuchung {
                        datum: Datum::new(1, 1, 2024),
                        name: name("Normal"),
                        wert: u_betrag(123, 12),
                        konto: konto_referenz("Konto"),
                        typ: SparbuchungTyp::SonstigeKosten,
                    },
                }],
            }],
            verfuegbare_jahre: vec![2020],
            selektiertes_jahr: 2020,
            database_version: DatabaseVersion {
                name: "asdf".to_string(),
                version: 0,
                session_random: 0,
            },
        };

        let template = super::map_to_template(view_result);

        assert_eq!(template.jahre.items[0].value, 2020);
        assert_eq!(template.jahre.items[0].selected, true);
        assert_eq!(template.database_id, "asdf-0-0");

        let erster_monat = &template.alles[0];
        assert_eq!(erster_monat.name, "Januar");
        assert_eq!(erster_monat.sparbuchungen[0].datum, "01.01.2024");
        assert_eq!(erster_monat.sparbuchungen[0].name, "Normal");
        assert_eq!(erster_monat.sparbuchungen[0].wert, "123,12");
        assert_eq!(erster_monat.sparbuchungen[0].dynamisch, false);
        assert_eq!(erster_monat.sparbuchungen[0].konto, "Konto");
        assert_eq!(erster_monat.sparbuchungen[0].typ, "Sonstige Kosten");
    }
}

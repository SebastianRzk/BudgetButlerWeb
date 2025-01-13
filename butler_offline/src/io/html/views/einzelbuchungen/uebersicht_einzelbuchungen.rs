use crate::budgetbutler::pages::einzelbuchungen::uebersicht_einzelbuchungen::{
    MonatsZusammenfassung, UebersichtEinzelbuchungenViewResult,
};
use crate::budgetbutler::view::routes::{
    EINZELBUCHUNGEN_AUSGABE_ADD, EINZELBUCHUNGEN_EINNAHME_ADD,
};
use crate::io::html::input::select::Select;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::{Betrag, Vorzeichen};
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/uebersicht_einzelbuchungen.html")]
pub struct UebersichtEinzelbuchungenTemplate {
    pub jahre: Select<i32>,
    pub alles: Vec<MonatsZusammenfassungTemplate>,
    pub leer: bool,
    pub selektiertes_jahr: i32,
    pub id: String,
}

pub struct MonatsZusammenfassungTemplate {
    pub name: String,
    pub buchungen: Vec<BuchungMitLinkTemplate>,
}

pub struct BuchungMitLinkTemplate {
    pub index: u32,
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
    pub link: String,
    pub dynamisch: bool,
}

pub fn render_uebersicht_einzelbuchungen_template(
    template: UebersichtEinzelbuchungenViewResult,
) -> String {
    let as_template: UebersichtEinzelbuchungenTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_monat_to_template(monat: &MonatsZusammenfassung) -> MonatsZusammenfassungTemplate {
    MonatsZusammenfassungTemplate {
        name: monat.monat.monat.clone(),
        buchungen: monat
            .buchungen
            .iter()
            .map(|x| map_buchung_to_template(x))
            .collect(),
    }
}

fn map_buchung_to_template(buchung: &Indiziert<Einzelbuchung>) -> BuchungMitLinkTemplate {
    BuchungMitLinkTemplate {
        kategorie: buchung.value.kategorie.kategorie.clone(),
        datum: buchung.value.datum.to_german_string(),
        index: buchung.index,
        wert: buchung.value.betrag.to_german_string(),
        dynamisch: buchung.dynamisch,
        link: map_betrag_to_link(&buchung.value.betrag),
        name: buchung.value.name.get_name().clone(),
    }
}

fn map_betrag_to_link(betrag: &Betrag) -> String {
    if betrag.vorzeichen == Vorzeichen::Negativ {
        return EINZELBUCHUNGEN_AUSGABE_ADD.to_string();
    }
    EINZELBUCHUNGEN_EINNAHME_ADD.to_string()
}

fn map_to_template(
    view_result: UebersichtEinzelbuchungenViewResult,
) -> UebersichtEinzelbuchungenTemplate {
    let alles: Vec<MonatsZusammenfassungTemplate> = view_result
        .liste
        .iter()
        .map(|x| map_monat_to_template(&x))
        .collect();
    UebersichtEinzelbuchungenTemplate {
        leer: alles.is_empty(),
        alles,
        id: view_result.database_version.as_string(),
        jahre: Select::new(
            view_result.verfuegbare_jahre.clone(),
            Some(view_result.selektiertes_jahr),
        ),
        selektiertes_jahr: view_result.selektiertes_jahr,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_einzelbuchungen::{
        MonatsZusammenfassung, UebersichtEinzelbuchungenViewResult,
    };
    use crate::io::html::views::einzelbuchungen::uebersicht_einzelbuchungen::map_to_template;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::{monats_name, Datum};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    fn test_map_to_template() {
        let view_result = UebersichtEinzelbuchungenViewResult {
            liste: vec![MonatsZusammenfassung {
                monat: monats_name("Januar"),
                buchungen: vec![
                    Indiziert {
                        index: 0,
                        dynamisch: false,
                        value: Einzelbuchung {
                            datum: Datum::new(1, 1, 2024),
                            name: name("Normal"),
                            kategorie: kategorie("NeueKategorie"),
                            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
                        },
                    },
                    Indiziert {
                        index: 0,
                        dynamisch: false,
                        value: Einzelbuchung {
                            datum: Datum::new(1, 1, 2024),
                            name: name("Normal"),
                            kategorie: kategorie("NeueKategorie"),
                            betrag: Betrag::new(Vorzeichen::Positiv, 123, 12),
                        },
                    },
                ],
            }],
            verfuegbare_jahre: vec![2020],
            selektiertes_jahr: 2020,
            database_version: DatabaseVersion {
                name: "asdf".to_string(),
                version: 0,
                session_random: 0,
            },
        };

        let template = map_to_template(view_result);

        assert_eq!(template.jahre.items[0].value, 2020);
        assert_eq!(template.jahre.items[0].selected, true);
        assert_eq!(template.id, "asdf-0-0");
        assert_eq!(template.leer, false);
        assert_eq!(template.selektiertes_jahr, 2020);

        let erster_monat = &template.alles[0];
        assert_eq!(erster_monat.name, "Januar");
        assert_eq!(erster_monat.buchungen[0].datum, "01.01.2024");
        assert_eq!(erster_monat.buchungen[0].name, "Normal");
        assert_eq!(erster_monat.buchungen[0].kategorie, "NeueKategorie");
        assert_eq!(erster_monat.buchungen[0].wert, "-123,12");
        assert_eq!(erster_monat.buchungen[0].link, "/addausgabe/");
        assert_eq!(erster_monat.buchungen[0].dynamisch, false);

        assert_eq!(erster_monat.buchungen[1].link, "/addeinnahme/");
    }

    #[test]
    fn test_map_to_template_with_empty_should_enable_leer() {
        let view_result = UebersichtEinzelbuchungenViewResult {
            liste: vec![],
            verfuegbare_jahre: vec![2020],
            selektiertes_jahr: 2020,
            database_version: DatabaseVersion {
                name: "asdf".to_string(),
                version: 0,
                session_random: 0,
            },
        };

        let template = map_to_template(view_result);

        assert_eq!(template.leer, true);
        assert_eq!(template.selektiertes_jahr, 2020);
    }
}

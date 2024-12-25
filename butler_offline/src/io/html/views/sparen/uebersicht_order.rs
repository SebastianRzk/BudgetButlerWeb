use crate::budgetbutler::pages::sparen::uebersicht_order::{
    BeschriebeneOrder, MonatsZusammenfassung, UebersichtOrderViewResult,
};
use crate::io::disk::primitive::order_typ::write_ordertyp;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_order.html")]
pub struct UebersichtSparbuchungTemplate {
    pub database_version: String,
    pub jahre: Select<i32>,
    pub alles: Vec<MonatTemplate>,
}

pub struct MonatTemplate {
    pub name: String,
    pub order: Vec<OrderTemplate>,
}

pub struct OrderTemplate {
    pub index: u32,
    pub datum: String,
    pub konto: String,
    pub name: String,
    pub depotwert: String,
    pub typ: String,
    pub wert: String,
    pub dynamisch: bool,
}

pub fn render_uebersicht_order_template(view_result: UebersichtOrderViewResult) -> String {
    let as_template: UebersichtSparbuchungTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_monat_to_template(monat: &MonatsZusammenfassung) -> MonatTemplate {
    MonatTemplate {
        name: monat.monat.monat.clone(),
        order: monat
            .buchungen
            .iter()
            .map(|x| map_buchung_to_template(x))
            .collect(),
    }
}

fn map_buchung_to_template(buchung: &BeschriebeneOrder) -> OrderTemplate {
    OrderTemplate {
        datum: buchung.datum.to_german_string(),
        depotwert: buchung.depotwertbeschreibung.clone(),
        index: buchung.index,
        wert: buchung.wert.get_realer_wert().to_german_string(),
        dynamisch: buchung.dynamisch,
        name: buchung.name.get_name().clone(),
        konto: buchung.konto.konto_name.name.clone(),
        typ: write_ordertyp(buchung.wert.get_typ()).element,
    }
}

fn map_to_template(view_result: UebersichtOrderViewResult) -> UebersichtSparbuchungTemplate {
    let alles: Vec<MonatTemplate> = view_result
        .liste
        .iter()
        .map(|x| map_monat_to_template(&x))
        .collect();
    UebersichtSparbuchungTemplate {
        alles,
        database_version: view_result.database_version.as_string(),
        jahre: Select::new(
            view_result.verfuegbare_jahre.clone(),
            Some(view_result.selektiertes_jahr),
        ),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_order::{
        BeschriebeneOrder, MonatsZusammenfassung, UebersichtOrderViewResult,
    };
    use crate::model::database::order::OrderTyp::Kauf;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::{monats_name, Datum};
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    fn test_map_to_template() {
        let view_result = UebersichtOrderViewResult {
            liste: vec![MonatsZusammenfassung {
                monat: monats_name("Januar"),
                buchungen: vec![BeschriebeneOrder {
                    index: 0,
                    dynamisch: false,
                    datum: Datum::new(1, 1, 2024),
                    name: name("Normal"),
                    wert: OrderBetrag::new(BetragOhneVorzeichen::new(123, 12), Kauf),
                    konto: konto_referenz("Konto"),
                    depotwertbeschreibung: "DepotwertBeschreibung".to_string(),
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
        assert_eq!(template.database_version, "asdf-0-0");

        let erster_monat = &template.alles[0];
        assert_eq!(erster_monat.name, "Januar");
        assert_eq!(erster_monat.order[0].datum, "01.01.2024");
        assert_eq!(erster_monat.order[0].name, "Normal");
        assert_eq!(erster_monat.order[0].wert, "123,12");
        assert_eq!(erster_monat.order[0].dynamisch, false);
        assert_eq!(erster_monat.order[0].konto, "Konto");
        assert_eq!(erster_monat.order[0].typ, "Kauf");
        assert_eq!(erster_monat.order[0].depotwert, "DepotwertBeschreibung");
    }
}

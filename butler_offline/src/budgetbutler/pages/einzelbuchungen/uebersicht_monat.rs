use crate::budgetbutler::chart::berechne_pie_chart;
use crate::budgetbutler::database::select::functions::datatypes::TagesAggregationsIndex;
use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_ausgaben, filter_auf_das_jahr, filter_auf_einnahmen, filter_auf_jahr_und_monat,
};
use crate::budgetbutler::database::select::functions::grouper::betrag_summe_gruppierung;
use crate::budgetbutler::database::select::functions::keyextractors::{
    einnahmen_ausgaben_aggregation, kategorie_aggregation, monatsweise_aggregation,
    tagesweise_aggregation,
};
use crate::budgetbutler::database::select::functions::sum_by::sum_einzelbuchungen;
use crate::budgetbutler::database::select::selector::Selector;
use crate::budgetbutler::table::berechne_buchungen_nach_kategorie;
use crate::budgetbutler::view::farbe::FarbenSelektor;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::metamodel::chart::{AusgabeAusKategorie, PieChart};
use crate::model::primitives::betrag::{Betrag, Vorzeichen};
use crate::model::primitives::datum::Datum;
use crate::model::primitives::farbe::{gray, green, red, Farbe};
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::state::persistent_application_state::Database;

pub struct UebersichtMonatViewResult {
    pub monate: Vec<String>,
    pub selected_date: String,
    pub selected_year: String,

    pub monat_chart: PlusMinusChart,
    pub jahr_chart: PlusMinusChart,

    pub ausgaben_chart: PieChart,
    pub einnahmen_chart: PieChart,

    pub gesamt_ausgaben: Betrag,
    pub gesamt_einnahmen: Betrag,

    pub zusammenfassung: Vec<Tag>,

    pub einnahmen: Vec<AusgabeAusKategorie>,
    pub ausgaben: Vec<AusgabeAusKategorie>,
}

pub struct PlusMinusChart {
    pub name_uebersicht_gruppe_1: String,
    pub name_uebersicht_gruppe_2: String,

    pub color_uebersicht_gruppe_1: Farbe,
    pub color_uebersicht_gruppe_2: Farbe,

    pub wert_uebersicht_gruppe_1: Betrag,
    pub wert_uebersicht_gruppe_2: Betrag,
}

pub struct Tag {
    pub name: String,
    pub items: Vec<Buchung>,
}

pub struct Buchung {
    pub color: Farbe,
    pub name: Name,
    pub wert: Betrag,
    pub kategorie: Kategorie,
}

pub struct UebersichtMonatContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub angeforderter_monat: Option<u32>,
    pub konfigurierte_farben: Vec<Farbe>,
    pub today: Datum,
}

pub fn handle_view(context: UebersichtMonatContext) -> UebersichtMonatViewResult {
    let selektiertes_jahr = context.angefordertes_jahr.unwrap_or(context.today.jahr);
    let selektierter_monat = context.angeforderter_monat.unwrap_or(context.today.monat);
    let farben_selektor = FarbenSelektor::new(
        context
            .database
            .einzelbuchungen
            .select()
            .extract_unique_values(kategorie_aggregation),
        context.konfigurierte_farben,
    );

    let daten_auf_monat_gefiltert =
        context
            .database
            .einzelbuchungen
            .select()
            .filter(filter_auf_jahr_und_monat(
                selektiertes_jahr,
                selektierter_monat,
            ));
    let einnahmen_auf_monat_gefiltert = daten_auf_monat_gefiltert
        .clone()
        .filter(filter_auf_einnahmen);
    let ausgaben_auf_monat_gefiltert = daten_auf_monat_gefiltert
        .clone()
        .filter(filter_auf_ausgaben);

    let verfuegbare_jahre = context
        .database
        .einzelbuchungen
        .select()
        .extract_unique_values(monatsweise_aggregation)
        .iter()
        .map(|x| format!("{}-{:02}", x.jahr, x.monat))
        .collect();

    UebersichtMonatViewResult {
        selected_date: format!("{}-{:02}", selektiertes_jahr, selektierter_monat,),
        selected_year: selektiertes_jahr.to_string(),
        monate: verfuegbare_jahre,

        monat_chart: berechne_monats_plus_minus_chart(
            context.database,
            selektiertes_jahr,
            selektierter_monat,
        ),
        jahr_chart: berechne_jahres_plus_minus_chart(context.database, selektiertes_jahr),

        einnahmen_chart: berechne_pie_chart(
            einnahmen_auf_monat_gefiltert.clone(),
            &farben_selektor,
        ),
        ausgaben_chart: berechne_pie_chart(ausgaben_auf_monat_gefiltert.clone(), &farben_selektor),

        gesamt_ausgaben: sum_einzelbuchungen(ausgaben_auf_monat_gefiltert.clone()),
        gesamt_einnahmen: sum_einzelbuchungen(einnahmen_auf_monat_gefiltert.clone()),

        zusammenfassung: berechne_zusammenfassung(
            context.database,
            selektiertes_jahr,
            selektierter_monat,
            &farben_selektor,
        ),

        einnahmen: berechne_buchungen_nach_kategorie(
            einnahmen_auf_monat_gefiltert,
            &farben_selektor,
        ),
        ausgaben: berechne_buchungen_nach_kategorie(ausgaben_auf_monat_gefiltert, &farben_selektor),
    }
}

fn berechne_zusammenfassung(
    database: &Database,
    selektiertes_jahr: i32,
    selektierter_monat: u32,
    farben_selektor: &FarbenSelektor,
) -> Vec<Tag> {
    let tagesweise_aggregation = database
        .einzelbuchungen
        .select()
        .filter(filter_auf_jahr_und_monat(
            selektiertes_jahr,
            selektierter_monat,
        ))
        .group_as_list_by(tagesweise_aggregation);
    let mut tage: Vec<&TagesAggregationsIndex> =
        tagesweise_aggregation.keys().into_iter().collect();
    tage.sort();
    let mut result = vec![];

    for tag in tage {
        let buchungen = tagesweise_aggregation.get(&tag).unwrap();
        let mut items: Vec<Buchung> = Vec::new();
        for buchung in buchungen {
            items.push(Buchung {
                color: farben_selektor.get(&buchung.value.kategorie).clone(),
                name: buchung.value.name.clone(),
                wert: buchung.value.betrag.clone(),
                kategorie: buchung.value.kategorie.clone(),
            });
        }
        let tag_template = Tag {
            name: format!(
                "{:02}.{:02}.{}",
                tag.tag, selektierter_monat, selektiertes_jahr
            ),
            items,
        };
        result.push(tag_template);
    }

    result
}

fn berechne_monats_plus_minus_chart(
    database: &Database,
    selektiertes_jahr: i32,
    selektierter_monat: u32,
) -> PlusMinusChart {
    let buchungen = database
        .einzelbuchungen
        .select()
        .filter(filter_auf_jahr_und_monat(
            selektiertes_jahr,
            selektierter_monat,
        ));
    berechne_plus_minus_chart(buchungen)
}

fn berechne_jahres_plus_minus_chart(database: &Database, selektiertes_jahr: i32) -> PlusMinusChart {
    let buchungen = database
        .einzelbuchungen
        .select()
        .filter(filter_auf_das_jahr(selektiertes_jahr));
    berechne_plus_minus_chart(buchungen)
}

fn berechne_plus_minus_chart(buchungen: Selector<Indiziert<Einzelbuchung>>) -> PlusMinusChart {
    let gruppierte_buchungen =
        buchungen.group_by(einnahmen_ausgaben_aggregation, betrag_summe_gruppierung);

    let zero = Betrag::zero();
    let einnahmen = gruppierte_buchungen
        .get(&Vorzeichen::Positiv)
        .unwrap_or(&zero);
    let ausgaben = gruppierte_buchungen
        .get(&Vorzeichen::Negativ)
        .unwrap_or(&zero);

    if einnahmen.clone() > ausgaben.abs() {
        PlusMinusChart {
            name_uebersicht_gruppe_1: "Gedeckte Ausgaben".to_string(),
            color_uebersicht_gruppe_1: gray(),
            wert_uebersicht_gruppe_1: ausgaben.abs(),

            name_uebersicht_gruppe_2: "Einnahmenüberschuss".to_string(),
            color_uebersicht_gruppe_2: green(),
            wert_uebersicht_gruppe_2: einnahmen.clone() - ausgaben.abs(),
        }
    } else {
        PlusMinusChart {
            name_uebersicht_gruppe_1: "Gedeckte Ausgaben".to_string(),
            color_uebersicht_gruppe_1: gray(),
            wert_uebersicht_gruppe_1: einnahmen.clone(),

            name_uebersicht_gruppe_2: "Ungedeckte Ausgaben".to_string(),
            color_uebersicht_gruppe_2: red(),
            wert_uebersicht_gruppe_2: ausgaben.abs() - einnahmen.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_monat::{
        handle_view, UebersichtMonatContext,
    };
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::farbe::{gray, green, red};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    pub fn view_should_preset_values() {
        let database = generate_database_with_einzelbuchungen(vec![
            Einzelbuchung {
                kategorie: kategorie("Kategorie 1 Einnahme"),
                betrag: Betrag::new(Vorzeichen::Positiv, 20, 0),
                datum: Datum::new(1, 1, 2020),
                name: name("Einzelbuchung 1"),
            },
            Einzelbuchung {
                kategorie: kategorie("Kategorie 1 Ausgabe"),
                betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
                datum: Datum::new(1, 1, 2020),
                name: name("Einzelbuchung 1"),
            },
            Einzelbuchung {
                kategorie: kategorie("Kategorie 1 Ausgabe"),
                betrag: Betrag::new(Vorzeichen::Negativ, 5, 0),
                datum: Datum::new(1, 10, 2020),
                name: name("Einzelbuchung 1"),
            },
        ]);

        let context = UebersichtMonatContext {
            database: &database,
            angefordertes_jahr: Some(2020),
            angeforderter_monat: Some(1),
            konfigurierte_farben: vec![green(), red()],
            today: Datum::new(1, 1, 2020),
        };

        let result = handle_view(context);

        assert_eq!(result.selected_date, "2020-01");
        assert_eq!(result.selected_year, "2020");
        assert_eq!(result.monate, vec!["2020-01", "2020-10"]);

        assert_eq!(
            result.monat_chart.name_uebersicht_gruppe_1,
            "Gedeckte Ausgaben"
        );
        assert_eq!(result.monat_chart.color_uebersicht_gruppe_1, gray());
        assert_eq!(
            result.monat_chart.wert_uebersicht_gruppe_1,
            Betrag::new(Vorzeichen::Positiv, 10, 0)
        );
        assert_eq!(
            result.monat_chart.name_uebersicht_gruppe_2,
            "Einnahmenüberschuss"
        );
        assert_eq!(result.monat_chart.color_uebersicht_gruppe_2, green());
        assert_eq!(
            result.monat_chart.wert_uebersicht_gruppe_2,
            Betrag::new(Vorzeichen::Positiv, 10, 0)
        );

        assert_eq!(
            result.jahr_chart.name_uebersicht_gruppe_1,
            "Gedeckte Ausgaben"
        );
        assert_eq!(result.jahr_chart.color_uebersicht_gruppe_1, gray());
        assert_eq!(
            result.jahr_chart.wert_uebersicht_gruppe_1,
            Betrag::new(Vorzeichen::Positiv, 15, 0)
        );
        assert_eq!(
            result.jahr_chart.name_uebersicht_gruppe_2,
            "Einnahmenüberschuss"
        );
        assert_eq!(result.jahr_chart.color_uebersicht_gruppe_2, green());
        assert_eq!(
            result.jahr_chart.wert_uebersicht_gruppe_2,
            Betrag::new(Vorzeichen::Positiv, 5, 0)
        );

        assert_eq!(result.einnahmen_chart.labels, vec!["Kategorie 1 Einnahme"]);
        assert_eq!(
            result.einnahmen_chart.data,
            vec![Betrag::new(Vorzeichen::Positiv, 20, 0)]
        );
        assert_eq!(result.einnahmen_chart.colors, vec![red()]);

        assert_eq!(result.ausgaben_chart.labels, vec!["Kategorie 1 Ausgabe"]);
        assert_eq!(
            result.ausgaben_chart.data,
            vec![Betrag::new(Vorzeichen::Negativ, 10, 0)]
        );
        assert_eq!(result.ausgaben_chart.colors, vec![green()]);

        assert_eq!(
            result.gesamt_ausgaben,
            Betrag::new(Vorzeichen::Negativ, 10, 0)
        );
        assert_eq!(
            result.gesamt_einnahmen,
            Betrag::new(Vorzeichen::Positiv, 20, 0)
        );

        assert_eq!(result.zusammenfassung.len(), 1);
        assert_eq!(result.zusammenfassung[0].name, "01.01.2020");
        assert_eq!(result.zusammenfassung[0].items.len(), 2);

        assert_eq!(result.zusammenfassung[0].items[1].color, red());
        assert_eq!(
            result.zusammenfassung[0].items[1].name,
            name("Einzelbuchung 1")
        );
        assert_eq!(
            result.zusammenfassung[0].items[1].wert,
            Betrag::new(Vorzeichen::Positiv, 20, 0)
        );
        assert_eq!(
            result.zusammenfassung[0].items[1].kategorie,
            kategorie("Kategorie 1 Einnahme")
        );

        assert_eq!(result.zusammenfassung[0].items[0].color, green());
        assert_eq!(
            result.zusammenfassung[0].items[0].name,
            name("Einzelbuchung 1")
        );
        assert_eq!(
            result.zusammenfassung[0].items[0].wert,
            Betrag::new(Vorzeichen::Negativ, 10, 0)
        );
        assert_eq!(
            result.zusammenfassung[0].items[0].kategorie,
            kategorie("Kategorie 1 Ausgabe")
        );
    }
}

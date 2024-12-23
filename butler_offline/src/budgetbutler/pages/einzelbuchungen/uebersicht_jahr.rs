use crate::budgetbutler::chart::{
    berechne_einnahmen_ausgaben_line_chart, berechne_kategorie_bar_chart,
    berechne_kategorie_line_chart, berechne_pie_chart, make_it_percent, make_it_pro_monat,
};
use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_ausgaben, filter_auf_das_jahr, filter_auf_einnahmen,
};
use crate::budgetbutler::database::select::functions::keyextractors::{
    jahresweise_aggregation, kategorie_aggregation,
};
use crate::budgetbutler::database::select::functions::mapper::map_positive;
use crate::budgetbutler::database::select::functions::sum_by::sum_einzelbuchungen;
use crate::budgetbutler::table::berechne_buchungen_nach_kategorie;
use crate::budgetbutler::view::farbe::{EinnahmenAusgabenFarbenSelektor, FarbenSelektor};
use crate::model::metamodel::chart::{AusgabeAusKategorie, BarChart, LineChart, PieChart};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::persistent_application_state::Database;

pub struct UebersichtJahrViewResult {
    pub jahre: Vec<String>,
    pub selected_jahr: String,

    pub durchschnittlich_monat: BarChart,
    pub einnahmen_ausgaben: LineChart,

    pub einnahmen: LineChart,
    pub ausgaben: LineChart,

    pub zusammenfassung_ausgaben: Vec<AusgabeAusKategorie>,
    pub zusammenfassung_einnahmen: Vec<AusgabeAusKategorie>,

    pub gesamt_ausgaben: Betrag,
    pub gesamt_einnahmen: Betrag,

    pub pie_einnahmen: PieChart,
    pub pie_ausgaben: PieChart,
}

pub struct UebersichtJahrContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub konfigurierte_farben: Vec<Farbe>,
    pub today: Datum,
}

pub fn handle_view(context: UebersichtJahrContext) -> UebersichtJahrViewResult {
    let selektiertes_jahr = context.angefordertes_jahr.unwrap_or(context.today.jahr);
    let mut angefangene_monate: u32 = 12;
    if selektiertes_jahr == context.today.jahr {
        angefangene_monate = context.today.monat;
    }

    let farben_selektor = FarbenSelektor::new(
        context
            .database
            .einzelbuchungen
            .select()
            .extract_unique_values(kategorie_aggregation),
        context.konfigurierte_farben,
    );

    let daten_auf_jahr_gefiltert = context
        .database
        .einzelbuchungen
        .select()
        .filter(filter_auf_das_jahr(selektiertes_jahr));

    let einnahmen_auf_jahr_gefiltert = daten_auf_jahr_gefiltert
        .clone()
        .filter(filter_auf_einnahmen);
    let ausgaben_auf_jahr_gefiltert = daten_auf_jahr_gefiltert
        .clone()
        .filter(filter_auf_ausgaben)
        .map(map_positive);

    let verfuegbare_jahre: Vec<String> = context
        .database
        .einzelbuchungen
        .select()
        .extract_unique_values(jahresweise_aggregation)
        .iter()
        .map(|x| format!("{}", x.jahr))
        .collect();

    let erster_des_jahres = Datum::new(1, 1, selektiertes_jahr);
    let letzter_des_jahres = Datum::new(31, 12, selektiertes_jahr);

    UebersichtJahrViewResult {
        jahre: verfuegbare_jahre.clone(),
        selected_jahr: selektiertes_jahr.to_string(),

        ausgaben: berechne_kategorie_line_chart(
            ausgaben_auf_jahr_gefiltert.clone(),
            &farben_selektor,
            erster_des_jahres.clone(),
            letzter_des_jahres.clone(),
        ),
        einnahmen: berechne_kategorie_line_chart(
            einnahmen_auf_jahr_gefiltert.clone(),
            &farben_selektor,
            erster_des_jahres.clone(),
            letzter_des_jahres.clone(),
        ),
        durchschnittlich_monat: make_it_pro_monat(
            berechne_kategorie_bar_chart(ausgaben_auf_jahr_gefiltert.clone()),
            angefangene_monate,
        ),

        einnahmen_ausgaben: berechne_einnahmen_ausgaben_line_chart(
            daten_auf_jahr_gefiltert.clone(),
            EinnahmenAusgabenFarbenSelektor {},
            erster_des_jahres,
            letzter_des_jahres,
        ),

        pie_einnahmen: make_it_percent(berechne_pie_chart(
            einnahmen_auf_jahr_gefiltert.clone(),
            &farben_selektor,
        )),
        pie_ausgaben: make_it_percent(berechne_pie_chart(
            ausgaben_auf_jahr_gefiltert.clone(),
            &farben_selektor,
        )),

        gesamt_ausgaben: sum_einzelbuchungen(ausgaben_auf_jahr_gefiltert.clone()),
        gesamt_einnahmen: sum_einzelbuchungen(einnahmen_auf_jahr_gefiltert.clone()),

        zusammenfassung_einnahmen: berechne_buchungen_nach_kategorie(
            einnahmen_auf_jahr_gefiltert,
            &farben_selektor,
        ),
        zusammenfassung_ausgaben: berechne_buchungen_nach_kategorie(
            ausgaben_auf_jahr_gefiltert,
            &farben_selektor,
        ),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_jahr::{
        handle_view, UebersichtJahrContext,
    };
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::builder::{minus_zwei, p_zero, vier, zwei};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::farbe::{green, red};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    fn test_handle_view() {
        let database = generate_database_with_einzelbuchungen(vec![
            Einzelbuchung {
                datum: Datum::new(1, 1, 2020),
                betrag: vier(),
                kategorie: kategorie("Einnahme Kategorie"),
                name: demo_name(),
            },
            Einzelbuchung {
                datum: Datum::new(1, 1, 2020),
                betrag: minus_zwei(),
                kategorie: kategorie("Ausgabe Kategorie"),
                name: demo_name(),
            },
            Einzelbuchung {
                datum: Datum::new(1, 1, 2021),
                betrag: minus_zwei(),
                kategorie: kategorie("Ausgabe Kategorie"),
                name: demo_name(),
            },
        ]);
        let context = UebersichtJahrContext {
            database: &database,
            angefordertes_jahr: Some(2020),
            konfigurierte_farben: vec![red(), green()],
            today: Datum::new(1, 1, 2022),
        };

        let result = handle_view(context);

        assert_eq!(result.jahre, vec!["2020", "2021"]);
        assert_eq!(result.selected_jahr, "2020");

        assert_eq!(result.gesamt_ausgaben, zwei());
        assert_eq!(result.gesamt_einnahmen, vier());

        assert_eq!(result.zusammenfassung_ausgaben.len(), 1);
        assert_eq!(result.zusammenfassung_ausgaben[0].wert, zwei());
        assert_eq!(
            result.zusammenfassung_ausgaben[0].kategorie,
            kategorie("Ausgabe Kategorie")
        );

        assert_eq!(result.zusammenfassung_einnahmen.len(), 1);
        assert_eq!(result.zusammenfassung_einnahmen[0].wert, vier());
        assert_eq!(
            result.zusammenfassung_einnahmen[0].kategorie,
            kategorie("Einnahme Kategorie")
        );

        assert_eq!(result.einnahmen.datasets.len(), 1);
        assert_eq!(result.einnahmen.datasets[0].label, "Einnahme Kategorie");
        assert_eq!(
            result.einnahmen.datasets[0].data,
            vec![
                vier(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
            ]
        );

        assert_eq!(result.ausgaben.datasets.len(), 1);
        assert_eq!(result.ausgaben.datasets[0].label, "Ausgabe Kategorie");
        assert_eq!(
            result.ausgaben.datasets[0].data,
            vec![
                zwei(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
                p_zero(),
            ]
        );

        assert_eq!(result.durchschnittlich_monat.datasets.len(), 1);
        assert_eq!(
            result.durchschnittlich_monat.datasets[0],
            Betrag::new(Vorzeichen::Positiv, 0, 16)
        );
    }
}

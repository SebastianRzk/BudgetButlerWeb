use crate::budgetbutler::database::select::functions::datatypes::KategorieAggregation;
use crate::budgetbutler::database::select::functions::filters::filter_auf_zeitraum;
use crate::budgetbutler::database::select::functions::grouper::{
    betrag_summe_gruppierung, einnahmen_ausgaben_gruppierung, kategorie_gruppierung,
};
use crate::budgetbutler::database::select::functions::keyextractors::{
    kategorie_aggregation, monatsweise_aggregation,
};
use crate::budgetbutler::database::select::selector::{generate_monats_indizes, Selector};
use crate::budgetbutler::database::select::selektion::einnahmen_ausgaben::{
    AUSGABEN_SELEKTION_NAME, EINNAHMEN_SELEKTION_NAME,
};
use crate::budgetbutler::view::farbe::{EinnahmenAusgabenFarbenSelektor, FarbenSelektor};
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::metamodel::chart::{BarChart, LineChart, LineChartDataSet, PieChart};
use crate::model::primitives::betrag::{Betrag, Vorzeichen};
use crate::model::primitives::datum::Datum;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use std::collections::{HashMap, HashSet};

pub fn berechne_pie_chart(
    selektion: Selector<Indiziert<Einzelbuchung>>,
    farben_selektor: &FarbenSelektor,
) -> PieChart {
    let buchungen = selektion.group_by(kategorie_aggregation, betrag_summe_gruppierung);
    let mut sortierte_kategorien = buchungen.keys().into_iter().collect::<Vec<&Kategorie>>();
    sortierte_kategorien.sort();

    let mut farben: Vec<Farbe> = Vec::new();
    let mut labels: Vec<String> = Vec::new();
    let mut werte: Vec<Betrag> = Vec::new();

    for kategorie in sortierte_kategorien {
        let zero = Betrag::zero();
        let betrag = buchungen.get(kategorie).unwrap_or(&zero);
        labels.push(kategorie.to_string());
        werte.push(betrag.clone());
        farben.push(farben_selektor.get(kategorie).clone());
    }

    PieChart {
        labels,
        data: werte,
        colors: farben,
    }
}

pub fn berechne_einnahmen_ausgaben_line_chart(
    selektion: Selector<Indiziert<Einzelbuchung>>,
    farben_selektor: EinnahmenAusgabenFarbenSelektor,
    first_date: Datum,
    last_date: Datum,
) -> LineChart {
    let einnahmen_ausgaben = selektion
        .filter(filter_auf_zeitraum(first_date.clone(), last_date.clone()))
        .group_by(monatsweise_aggregation, einnahmen_ausgaben_gruppierung);

    let mut zusammenfassung_monatsliste = vec![];
    let mut zusammenfassung_einnahmenliste = vec![];
    let mut zusammenfassung_ausgabenliste = vec![];

    for monat in generate_monats_indizes(first_date, last_date) {
        zusammenfassung_monatsliste.push(monat.format_descriptive_string().to_name());
        if let Some(einnahmen_ausgaben) = einnahmen_ausgaben.get(&monat) {
            zusammenfassung_einnahmenliste.push(einnahmen_ausgaben.einnahmen.clone());
            zusammenfassung_ausgabenliste.push(einnahmen_ausgaben.ausgaben.abs());
        } else {
            zusammenfassung_einnahmenliste.push(Betrag::zero());
            zusammenfassung_ausgabenliste.push(Betrag::zero());
        }
    }

    LineChart {
        labels: zusammenfassung_monatsliste,
        datasets: vec![
            LineChartDataSet {
                label: EINNAHMEN_SELEKTION_NAME.to_string(),
                data: zusammenfassung_einnahmenliste,
                farbe: farben_selektor.get_einnahmen(),
            },
            LineChartDataSet {
                label: AUSGABEN_SELEKTION_NAME.to_string(),
                data: zusammenfassung_ausgabenliste,
                farbe: farben_selektor.get_ausgaben(),
            },
        ],
    }
}

pub fn berechne_kategorie_line_chart(
    selektion: Selector<Indiziert<Einzelbuchung>>,
    farben_selektor: &FarbenSelektor,
    first_date: Datum,
    last_date: Datum,
) -> LineChart {
    let buchungen_nach_kategorie = selektion
        .clone()
        .group_by(monatsweise_aggregation, kategorie_gruppierung);

    let mut zusammenfassung_monatsliste = vec![];
    let mut kategorie_values_hashmap: HashMap<Kategorie, Vec<Betrag>> = HashMap::new();
    let kategorien = selektion.extract_unique_values(kategorie_aggregation);
    let alle_kategorien_set: HashSet<&Kategorie> = HashSet::from_iter(kategorien.iter());
    let mut alle_kategorien = alle_kategorien_set
        .into_iter()
        .cloned()
        .collect::<Vec<Kategorie>>();
    alle_kategorien.sort();

    for monat in generate_monats_indizes(first_date, last_date) {
        zusammenfassung_monatsliste.push(monat.format_descriptive_string().to_name());
        let default = KategorieAggregation::default();
        let monatsergebnis = buchungen_nach_kategorie.get(&monat).unwrap_or(&default);

        for kategorie in &alle_kategorien {
            let betrag = monatsergebnis
                .content
                .get(&kategorie)
                .unwrap_or(&Betrag::zero())
                .clone();
            let values = kategorie_values_hashmap
                .entry(kategorie.clone())
                .or_insert(vec![]);
            values.push(betrag);
        }
    }

    let mut datasets: Vec<LineChartDataSet> = Vec::new();
    for kategorie in alle_kategorien {
        let values = kategorie_values_hashmap.get(&kategorie).unwrap();
        datasets.push(LineChartDataSet {
            label: kategorie.to_string(),
            data: values.clone(),
            farbe: farben_selektor.get(&kategorie),
        });
    }

    LineChart {
        labels: zusammenfassung_monatsliste,
        datasets,
    }
}

pub fn berechne_kategorie_bar_chart(selektion: Selector<Indiziert<Einzelbuchung>>) -> BarChart {
    let buchungen_nach_kategorie = selektion
        .clone()
        .group_by(kategorie_aggregation, betrag_summe_gruppierung);

    let mut kategorie_liste: Vec<Kategorie> = vec![];
    let mut werte_liste: Vec<Betrag> = vec![];

    let kategorien = selektion.extract_unique_values(kategorie_aggregation);
    let alle_kategorien_set: HashSet<&Kategorie> = HashSet::from_iter(kategorien.iter());
    let mut alle_kategorien = alle_kategorien_set
        .into_iter()
        .cloned()
        .collect::<Vec<Kategorie>>();
    alle_kategorien.sort();

    for kategorie in &alle_kategorien {
        let betrag = buchungen_nach_kategorie
            .get(&kategorie)
            .unwrap_or(&Betrag::zero())
            .clone();
        kategorie_liste.push(kategorie.clone());
        werte_liste.push(betrag);
    }

    BarChart {
        datasets: werte_liste,
        labels: kategorie_liste
            .into_iter()
            .map(|kategorie| Name::new(kategorie.to_string()))
            .collect(),
    }
}

pub fn make_it_pro_monat(bar_chart: BarChart, angefangene_monate: u32) -> BarChart {
    let mut new_data = vec![];
    for data in bar_chart.datasets.iter() {
        let as_cent = data.as_cent();
        let as_cent = as_cent / angefangene_monate as u64;
        let euro = as_cent / 100;
        let cent = as_cent % 100;
        new_data.push(Betrag::new(Vorzeichen::Positiv, euro as u32, cent as u8));
    }
    BarChart {
        datasets: new_data,
        labels: bar_chart.labels,
    }
}

pub fn make_it_percent(bar_chart: PieChart) -> PieChart {
    let gesamt = bar_chart
        .data
        .iter()
        .fold(Betrag::zero(), |acc, x| acc + x.clone());
    let mut new_data = vec![];
    for value in bar_chart.data.iter() {
        if gesamt.as_cent() == 0 {
            new_data.push(Betrag::zero());
            continue;
        }
        let percent = (value.as_cent() * 10000) / gesamt.as_cent();
        let euro = percent / 100;
        let cent = percent % 100;
        new_data.push(Betrag::new(Vorzeichen::Positiv, euro as u32, cent as u8));
    }
    PieChart {
        data: new_data,
        labels: bar_chart.labels,
        colors: bar_chart.colors,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::chart::{
        berechne_kategorie_bar_chart, berechne_kategorie_line_chart, make_it_percent,
        make_it_pro_monat,
    };
    use crate::budgetbutler::view::farbe::FarbenSelektor;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie_und_betrag;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::metamodel::chart::{BarChart, LineChartDataSet, PieChart};
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::{Datum, MonatsName};
    use crate::model::primitives::farbe::builder::farbe;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

    #[test]
    fn test_make_it_percent() {
        let input_pie = PieChart {
            colors: vec![],
            data: vec![
                Betrag::new(Vorzeichen::Positiv, 100, 0),
                Betrag::new(Vorzeichen::Positiv, 200, 0),
                Betrag::new(Vorzeichen::Positiv, 300, 0),
            ],
            labels: vec![],
        };

        let result = make_it_percent(input_pie);

        assert_eq!(result.data[0], Betrag::new(Vorzeichen::Positiv, 16, 66));
        assert_eq!(result.data[1], Betrag::new(Vorzeichen::Positiv, 33, 33));
        assert_eq!(result.data[2], Betrag::new(Vorzeichen::Positiv, 50, 0));
    }

    #[test]
    fn test_berechne_kategorie_bar_chart() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![
                indiziert(einzelbuchung_with_kategorie_und_betrag("K1", zwei())),
                indiziert(einzelbuchung_with_kategorie_und_betrag("K1", zwei())),
                indiziert(einzelbuchung_with_kategorie_und_betrag("K2", zwei())),
            ],
        };

        let result = berechne_kategorie_bar_chart(einzelbuchungen.select());

        assert_eq!(result.labels, vec![name("K1"), name("K2")]);
        assert_eq!(result.datasets, vec![vier(), zwei()]);
    }

    #[test]
    fn test_berechne_kategorie_line_chart() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![
                indiziert(Einzelbuchung {
                    kategorie: kategorie("K1"),
                    name: demo_name(),
                    datum: Datum::new(1, 1, 2020),
                    betrag: zwei(),
                }),
                indiziert(Einzelbuchung {
                    kategorie: kategorie("K2"),
                    name: demo_name(),
                    datum: Datum::new(1, 2, 2020),
                    betrag: vier(),
                }),
            ],
        };
        let farben_selektor = FarbenSelektor::new(
            vec![kategorie("K1"), kategorie("K2")],
            vec![farbe("rot"), farbe("blau")],
        );

        let result = berechne_kategorie_line_chart(
            einzelbuchungen.select(),
            &farben_selektor,
            Datum::new(1, 1, 2020),
            Datum::new(1, 2, 2020),
        );

        assert_eq!(
            result.labels,
            vec![
                MonatsName {
                    monat: "01/2020".to_string(),
                }
                .to_name(),
                MonatsName {
                    monat: "02/2020".to_string(),
                }
                .to_name()
            ]
        );
        assert_eq!(
            result.datasets,
            vec![
                LineChartDataSet {
                    label: "K1".to_string(),
                    data: vec![zwei(), Betrag::zero()],
                    farbe: farbe("rot"),
                },
                LineChartDataSet {
                    label: "K2".to_string(),
                    data: vec![Betrag::zero(), vier()],
                    farbe: farbe("blau"),
                }
            ]
        );
    }

    #[test]
    fn test_make_it_pro_monat() {
        let dataset = BarChart {
            labels: vec![],
            datasets: vec![Betrag::new(Vorzeichen::Positiv, 10, 0)],
        };

        let result = make_it_pro_monat(dataset, 2);

        assert_eq!(result.datasets[0], Betrag::new(Vorzeichen::Positiv, 5, 0));
    }

    #[test]
    fn test_make_it_pro_monat_with_sub_zero_result() {
        let dataset = BarChart {
            labels: vec![],
            datasets: vec![Betrag::new(Vorzeichen::Positiv, 1, 0)],
        };

        let result = make_it_pro_monat(dataset, 4);

        assert_eq!(result.datasets[0], Betrag::new(Vorzeichen::Positiv, 0, 25));
    }
}

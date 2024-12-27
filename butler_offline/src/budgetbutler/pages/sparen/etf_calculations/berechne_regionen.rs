use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    DepotwertMitDaten, Tabelle, TabellenZeile, TabellenZelle,
};
use crate::budgetbutler::shares::countries::get_country_name;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::prozent::Prozent;
use std::collections::HashMap;

pub fn berechne_regionen(
    depotwerte_mit_kontostand: &Vec<DepotwertMitDaten>,
    gesamt_summe: Betrag,
) -> Tabelle {
    let mut regionen_map = HashMap::new();

    for depotwert_mit_kontostand in depotwerte_mit_kontostand {
        let aktuelle_regionen = depotwert_mit_kontostand.data.data.regionen.keys();
        for region in aktuelle_regionen {
            if !regionen_map.contains_key(region) {
                regionen_map.insert(
                    region.clone(),
                    TabellenZeile {
                        gesamt_column: TabellenZelle {
                            prozent: Prozent::zero(),
                            euro: Betrag::zero(),
                        },
                        row_label: region.clone(),
                        other_columns: vec![],
                    },
                );
            }
        }
    }

    let alle_regionen = regionen_map
        .keys()
        .map(|x| x.clone())
        .collect::<Vec<String>>();

    for depotwert_mit_kontostand in depotwerte_mit_kontostand {
        for region in alle_regionen.clone() {
            if !depotwert_mit_kontostand
                .data
                .data
                .regionen
                .contains_key(&region)
            {
                let region_row = regionen_map.get(&region).unwrap();
                let mut neue_werte = region_row.other_columns.clone();
                neue_werte.push(TabellenZelle {
                    euro: Betrag::zero(),
                    prozent: Prozent::zero(),
                });
                regionen_map.insert(
                    region.clone(),
                    TabellenZeile {
                        gesamt_column: region_row.gesamt_column.clone(),
                        row_label: region_row.row_label.clone(),
                        other_columns: neue_werte,
                    },
                );

                continue;
            }

            let betrag_prozent = Prozent::from_float_representation(
                depotwert_mit_kontostand
                    .data
                    .data
                    .regionen
                    .get(&region)
                    .unwrap()
                    .clone(),
            );
            let betrag = depotwert_mit_kontostand
                .aktueller_kontostand
                .anteil(&betrag_prozent);
            let region_row = regionen_map.get(&region).unwrap();
            let neuer_gesamt_wert = region_row.gesamt_column.euro.clone() + betrag.clone();
            let neuer_gesamt_prozent =
                Prozent::from_betrags_differenz(&neuer_gesamt_wert, &gesamt_summe);
            let mut neue_cols = region_row.other_columns.clone();
            neue_cols.push(TabellenZelle {
                euro: betrag.clone(),
                prozent: Prozent::from_betrags_differenz(
                    &betrag,
                    &depotwert_mit_kontostand.aktueller_kontostand.clone(),
                ),
            });
            let neue_region = TabellenZeile {
                gesamt_column: TabellenZelle {
                    prozent: neuer_gesamt_prozent,
                    euro: neuer_gesamt_wert,
                },
                row_label: region_row.row_label.clone(),
                other_columns: neue_cols,
            };

            regionen_map.insert(region.clone(), neue_region);
        }
    }

    let mut regionen_list: Vec<TabellenZeile> = regionen_map.values().map(|x| x.clone()).collect();
    regionen_list.sort_by(|a, b| b.gesamt_column.euro.cmp(&a.gesamt_column.euro));

    let translated_rows = regionen_list
        .iter()
        .map(|x| TabellenZeile {
            row_label: get_country_name(x.row_label.clone()),
            gesamt_column: x.gesamt_column.clone(),
            other_columns: x.other_columns.clone(),
        })
        .collect();
    Tabelle {
        header: depotwerte_mit_kontostand
            .iter()
            .map(|x| x.depotwert.name.name.clone())
            .collect(),
        rows: translated_rows,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::etf_calculations::berechne_regionen::berechne_regionen;
    use crate::budgetbutler::pages::sparen::uebersicht_etfs::DepotwertMitDaten;
    use crate::model::database::depotwert::builder::depotwert_mit_name;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::prozent::Prozent;
    use crate::model::shares::{ShareData, ShareDataContent};
    use std::collections::HashMap;

    #[test]
    fn test_berechne_regionen_ohne_daten() {
        let result = berechne_regionen(&vec![], Betrag::zero());
        assert_eq!(result.header.len(), 0);
        assert_eq!(result.rows.len(), 0);
    }

    #[test]
    fn test_berechne_regionen() {
        let mut depotwert1_regionen = HashMap::new();
        depotwert1_regionen.insert("Region1".to_string(), 50.0);
        depotwert1_regionen.insert("Region2".to_string(), 50.0);

        let mut depotwert2_regionen = HashMap::new();
        depotwert2_regionen.insert("Region2".to_string(), 50.0);
        depotwert2_regionen.insert("Region3".to_string(), 50.0);

        let depotwerte_mit_kontostand = vec![
            DepotwertMitDaten {
                depotwert: depotwert_mit_name("Depotwert1"),
                data: ShareData {
                    date: "any datum".to_string(),
                    source: "any source".to_string(),
                    data: ShareDataContent {
                        sektoren: HashMap::new(),
                        name: "any name".to_string(),
                        index_name: "any index name".to_string(),
                        kosten: 0.0,
                        regionen: depotwert1_regionen,
                    },
                },
                aktueller_kontostand: Betrag::from_cent(Vorzeichen::Positiv, 200 * 100),
            },
            DepotwertMitDaten {
                depotwert: depotwert_mit_name("Depotwert2"),
                data: ShareData {
                    date: "any datum".to_string(),
                    source: "any source".to_string(),
                    data: ShareDataContent {
                        sektoren: HashMap::new(),
                        name: "any name".to_string(),
                        index_name: "any index name".to_string(),
                        kosten: 0.0,
                        regionen: depotwert2_regionen,
                    },
                },
                aktueller_kontostand: Betrag::from_cent(Vorzeichen::Positiv, 100 * 100),
            },
        ];

        let result = berechne_regionen(
            &depotwerte_mit_kontostand,
            Betrag::from_cent(Vorzeichen::Positiv, 300 * 100),
        );
        assert_eq!(result.header, vec!["Depotwert1", "Depotwert2"]);

        assert_eq!(result.rows.len(), 3);
        assert_eq!(result.rows[0].row_label, "Region2");
        assert_eq!(
            result.rows[0].gesamt_column.euro,
            Betrag::from_cent(Vorzeichen::Positiv, 150 * 100)
        );
        assert_eq!(
            result.rows[0].gesamt_column.prozent,
            Prozent::from_float_representation(50.0)
        );
        assert_eq!(result.rows[0].other_columns.len(), 2);
        assert_eq!(
            result.rows[0].other_columns[0].euro,
            Betrag::from_cent(Vorzeichen::Positiv, 100 * 100)
        );
        assert_eq!(
            result.rows[0].other_columns[0].prozent,
            Prozent::from_float_representation(50.0)
        );
        assert_eq!(
            result.rows[0].other_columns[1].euro,
            Betrag::from_cent(Vorzeichen::Positiv, 50 * 100)
        );
        assert_eq!(
            result.rows[0].other_columns[1].prozent,
            Prozent::from_float_representation(50.0)
        );

        assert_eq!(result.rows[1].row_label, "Region1");
        assert_eq!(
            result.rows[1].gesamt_column.euro,
            Betrag::from_cent(Vorzeichen::Positiv, 100 * 100)
        );
        assert_eq!(
            result.rows[1].gesamt_column.prozent,
            Prozent::from_float_representation(33.33)
        );
        assert_eq!(result.rows[1].other_columns.len(), 2);
        assert_eq!(
            result.rows[1].other_columns[0].euro,
            Betrag::from_cent(Vorzeichen::Positiv, 100 * 100)
        );
        assert_eq!(
            result.rows[1].other_columns[0].prozent,
            Prozent::from_float_representation(50.0)
        );
        assert_eq!(result.rows[1].other_columns[1].euro, Betrag::zero());
        assert_eq!(result.rows[1].other_columns[1].prozent, Prozent::zero());

        assert_eq!(result.rows[2].row_label, "Region3");
        assert_eq!(
            result.rows[2].gesamt_column.euro,
            Betrag::from_cent(Vorzeichen::Positiv, 50 * 100)
        );
        assert_eq!(
            result.rows[2].gesamt_column.prozent,
            Prozent::from_float_representation(16.66)
        );
        assert_eq!(result.rows[2].other_columns.len(), 2);
        assert_eq!(result.rows[2].other_columns[0].euro, Betrag::zero());
        assert_eq!(result.rows[2].other_columns[0].prozent, Prozent::zero());
    }

    #[test]
    fn test_berechne_regionen_should_translate_region() {
        let mut depotwert_regionen = HashMap::new();
        depotwert_regionen.insert("DEU".to_string(), 100.0);

        let depotwerte_mit_kontostand = vec![DepotwertMitDaten {
            depotwert: depotwert_mit_name("Depotwert1"),
            data: ShareData {
                date: "any datum".to_string(),
                source: "any source".to_string(),
                data: ShareDataContent {
                    sektoren: HashMap::new(),
                    name: "any name".to_string(),
                    index_name: "any index name".to_string(),
                    kosten: 0.0,
                    regionen: depotwert_regionen,
                },
            },
            aktueller_kontostand: Betrag::from_cent(Vorzeichen::Positiv, 200 * 100),
        }];

        let result = berechne_regionen(
            &depotwerte_mit_kontostand,
            Betrag::from_cent(Vorzeichen::Positiv, 200 * 100),
        );
        assert_eq!(result.header, vec!["Depotwert1"]);

        assert_eq!(result.rows.len(), 1);
        assert_eq!(result.rows[0].row_label, "Deutschland");
    }
}

use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    DepotwertMitDaten, Tabelle, TabellenZeile, TabellenZelle,
};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::prozent::Prozent;
use std::collections::HashMap;

pub fn berechne_sektoren(
    depotwerte_mit_kontostand: &Vec<DepotwertMitDaten>,
    gesamt_summe: Betrag,
) -> Tabelle {
    let mut sektoren_map = HashMap::new();

    for depotwert_mit_kontostand in depotwerte_mit_kontostand {
        let aktuelle_sektoren = depotwert_mit_kontostand.data.data.sektoren.keys();
        for sektor in aktuelle_sektoren {
            if !sektoren_map.contains_key(sektor) {
                sektoren_map.insert(
                    sektor.clone(),
                    TabellenZeile {
                        gesamt_column: TabellenZelle {
                            prozent: Prozent::zero(),
                            euro: Betrag::zero(),
                        },
                        row_label: sektor.clone(),
                        other_columns: vec![],
                    },
                );
            }
        }
    }

    let alle_sektoren = sektoren_map
        .keys()
        .map(|x| x.clone())
        .collect::<Vec<String>>();

    for depotwert_mit_kontostand in depotwerte_mit_kontostand {
        for sektor in alle_sektoren.clone() {
            if !depotwert_mit_kontostand
                .data
                .data
                .sektoren
                .contains_key(&sektor)
            {
                let sektor_row = sektoren_map.get(&sektor).unwrap();
                let mut neue_werte = sektor_row.other_columns.clone();
                neue_werte.push(TabellenZelle {
                    euro: Betrag::zero(),
                    prozent: Prozent::zero(),
                });
                sektoren_map.insert(
                    sektor.clone(),
                    TabellenZeile {
                        gesamt_column: sektor_row.gesamt_column.clone(),
                        row_label: sektor_row.row_label.clone(),
                        other_columns: neue_werte,
                    },
                );

                continue;
            }

            let betrag_prozent = Prozent::from_float_representation(
                depotwert_mit_kontostand
                    .data
                    .data
                    .sektoren
                    .get(&sektor)
                    .unwrap()
                    .clone(),
            );
            let betrag = depotwert_mit_kontostand
                .aktueller_kontostand
                .anteil(&betrag_prozent);
            let sektor_row = sektoren_map.get(&sektor).unwrap();
            let neuer_gesamt_wert = sektor_row.gesamt_column.euro.clone() + betrag.clone();
            let neuer_gesamt_prozent =
                Prozent::from_betrags_differenz(&neuer_gesamt_wert, &gesamt_summe);
            let mut neue_cols = sektor_row.other_columns.clone();
            neue_cols.push(TabellenZelle {
                euro: betrag.clone(),
                prozent: Prozent::from_betrags_differenz(
                    &betrag,
                    &depotwert_mit_kontostand.aktueller_kontostand.clone(),
                ),
            });
            let neuer_sektor = TabellenZeile {
                gesamt_column: TabellenZelle {
                    prozent: neuer_gesamt_prozent,
                    euro: neuer_gesamt_wert,
                },
                row_label: sektor_row.row_label.clone(),
                other_columns: neue_cols,
            };

            sektoren_map.insert(sektor.clone(), neuer_sektor);
        }
    }

    let mut sektoren_list: Vec<TabellenZeile> = sektoren_map.values().map(|x| x.clone()).collect();
    sektoren_list.sort_by(|a, b| b.gesamt_column.euro.cmp(&a.gesamt_column.euro));

    Tabelle {
        header: depotwerte_mit_kontostand
            .iter()
            .map(|x| x.depotwert.name.name.clone())
            .collect(),
        rows: sektoren_list,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::etf_calculations::berechne_sektoren::berechne_sektoren;
    use crate::budgetbutler::pages::sparen::uebersicht_etfs::DepotwertMitDaten;
    use crate::model::database::depotwert::builder::depotwert_mit_name;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::prozent::Prozent;
    use crate::model::shares::{ShareData, ShareDataContent};
    use std::collections::HashMap;

    #[test]
    fn test_berechne_sektoren_ohne_daten() {
        let result = berechne_sektoren(&vec![], Betrag::zero());
        assert_eq!(result.header.len(), 0);
        assert_eq!(result.rows.len(), 0);
    }

    #[test]
    fn test_berechne_sektoren() {
        let mut depotwert1_sektoren = HashMap::new();
        depotwert1_sektoren.insert("Sektor1".to_string(), 50.0);
        depotwert1_sektoren.insert("Sektor2".to_string(), 50.0);

        let mut depotwert2_sektoren = HashMap::new();
        depotwert2_sektoren.insert("Sektor2".to_string(), 50.0);
        depotwert2_sektoren.insert("Sektor3".to_string(), 50.0);

        let depotwerte_mit_kontostand = vec![
            DepotwertMitDaten {
                depotwert: depotwert_mit_name("Depotwert1"),
                data: ShareData {
                    date: "any datum".to_string(),
                    source: "any source".to_string(),
                    data: ShareDataContent {
                        sektoren: depotwert1_sektoren,
                        name: "any name".to_string(),
                        index_name: "any index name".to_string(),
                        kosten: 0.0,
                        regionen: HashMap::new(),
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
                        sektoren: depotwert2_sektoren,
                        name: "any name".to_string(),
                        index_name: "any index name".to_string(),
                        kosten: 0.0,
                        regionen: HashMap::new(),
                    },
                },
                aktueller_kontostand: Betrag::from_cent(Vorzeichen::Positiv, 100 * 100),
            },
        ];

        let result = berechne_sektoren(
            &depotwerte_mit_kontostand,
            Betrag::from_cent(Vorzeichen::Positiv, 300 * 100),
        );
        assert_eq!(result.header, vec!["Depotwert1", "Depotwert2"]);

        assert_eq!(result.rows.len(), 3);
        assert_eq!(result.rows[0].row_label, "Sektor2");
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

        assert_eq!(result.rows[1].row_label, "Sektor1");
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

        assert_eq!(result.rows[2].row_label, "Sektor3");
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
}

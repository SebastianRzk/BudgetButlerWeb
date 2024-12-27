use crate::budgetbutler::pages::sparen::uebersicht_etfs::Tabelle;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::farbe::Farbe;

pub fn make_pie(table: &Tabelle) -> PieChart {
    let mut labels = vec![];
    let mut data = vec![];
    let mut colors = vec![];

    for row in &table.rows {
        labels.push(row.row_label.clone());
        data.push(Betrag::from_iso_string(
            &row.gesamt_column
                .prozent
                .als_halbwegs_gerundeter_iso_string(),
        ));
        colors.push(Farbe {
            as_string: "color(red).alpha(0.5)".to_string(),
        });
    }

    PieChart {
        labels,
        data,
        colors,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
        Tabelle, TabellenZeile, TabellenZelle,
    };
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag::Vorzeichen::Positiv;
    use crate::model::primitives::prozent::Prozent;

    #[test]
    pub fn test_make_pie() {
        let table = Tabelle {
            header: vec!["header".to_string()],
            rows: vec![
                TabellenZeile {
                    row_label: "Wert1".to_string(),
                    gesamt_column: TabellenZelle {
                        euro: Betrag::from_cent(Positiv, 150 * 100),
                        prozent: Prozent::from_int_representation(75),
                    },
                    other_columns: vec![],
                },
                TabellenZeile {
                    row_label: "Wert2".to_string(),
                    gesamt_column: TabellenZelle {
                        euro: Betrag::from_cent(Positiv, 50 * 100),
                        prozent: Prozent::from_int_representation(25),
                    },
                    other_columns: vec![],
                },
            ],
        };

        let result = super::make_pie(&table);

        assert_eq!(result.labels, vec!["Wert1", "Wert2"]);
        assert_eq!(
            result.data,
            vec![
                Betrag::from_cent(Positiv, 75 * 100),
                Betrag::from_cent(Positiv, 25 * 100)
            ]
        );
    }
}

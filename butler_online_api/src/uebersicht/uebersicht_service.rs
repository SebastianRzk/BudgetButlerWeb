use crate::core::datum::monats_name_from_datum;
use crate::uebersicht::model::{BesitztDatumKategorieUndBetrag, MonatsUebersicht, Uebersicht};

pub fn berechne_uebersicht(einzelbuchungen: &Vec<impl BesitztDatumKategorieUndBetrag>) -> Uebersicht {
    let mut monate: Vec<MonatsUebersicht> = vec![];

    for einzelbuchung in einzelbuchungen {
        let mut found = false;
        let datum_als_string = monats_name_from_datum(&einzelbuchung.get_datum());
        for monats_uebersicht in &mut monate {
            if monats_uebersicht.name == datum_als_string {
                found = true;
                monats_uebersicht.werte.insert(
                    einzelbuchung.get_kategorie().clone(),
                    einzelbuchung.get_betrag().clone()
                        + monats_uebersicht
                            .werte
                            .get(einzelbuchung.get_kategorie())
                            .unwrap_or(&0.into()),
                );
            }
        }

        if !found {
            let mut werte = std::collections::HashMap::new();
            werte.insert(einzelbuchung.get_kategorie().clone(), einzelbuchung.get_betrag().clone());
            monate.push(MonatsUebersicht {
                name: datum_als_string,
                werte,
            });
        }
    }
    Uebersicht { monate }
}


#[cfg(test)]
mod tests {
    use crate::einzelbuchungen::model::Einzelbuchung;
    use time::Month;

    #[test]
    fn test_berechne_uebersicht_aus_leerer_liste_sollte_leeres_ergebnis_liefern(){
        let buchungen: Vec<Einzelbuchung> = vec![];
        let result = super::berechne_uebersicht(&buchungen);
        assert_eq!(result.monate.len(), 0);
    }

    #[test]
    fn test_berechne_uebersicht_mit_datum_sollte_monatsuebersicht_anlegen(){
        let result = super::berechne_uebersicht(&vec![
            Einzelbuchung {
                id: "1".to_string(),
                name: "Test".to_string(),
                kategorie: "Kategorie".to_string(),
                wert: 100.into(),
                datum: time::Date::from_calendar_date(2021, Month::January, 1).unwrap(),
                user: "Test".to_string(),
            }
        ]);

        assert_eq!(result.monate.len(), 1);
        assert_eq!(result.monate[0].name, "Januar 2021");
        assert_eq!(result.monate[0].werte.len(), 1);
        assert_eq!(result.monate[0].werte.get("Kategorie").unwrap(), &100.into());
    }

    #[test]
    fn test_berechne_uebersicht_sollte_betraege_gleichen_monats_und_kategorie_addieren(){
        let result = super::berechne_uebersicht(&vec![
            Einzelbuchung {
                id: "1".to_string(),
                name: "Test".to_string(),
                kategorie: "Kategorie".to_string(),
                wert: 100.into(),
                datum: time::Date::from_calendar_date(2021, Month::January, 1).unwrap(),
                user: "Test".to_string(),
            },
            Einzelbuchung {
                id: "1".to_string(),
                name: "Test".to_string(),
                kategorie: "Kategorie".to_string(),
                wert: 50.into(),
                datum: time::Date::from_calendar_date(2021, Month::January, 1).unwrap(),
                user: "Test".to_string(),
            }
        ]);

        assert_eq!(result.monate.len(), 1);
        assert_eq!(result.monate[0].name, "Januar 2021");
        assert_eq!(result.monate[0].werte.len(), 1);
        assert_eq!(result.monate[0].werte.get("Kategorie").unwrap(), &150.into());
    }
}
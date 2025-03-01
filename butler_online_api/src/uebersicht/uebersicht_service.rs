use crate::core::datum::monats_name_from_datum;
use crate::gemeinsame_buchungen::model::GemeinsameBuchung;
use crate::uebersicht::model::{
    BesitztDatumKategorieUndBetrag, GemeinsameMonatsuebersicht, GemeinsameUebersicht,
    MonatsUebersicht, Uebersicht,
};
use bigdecimal::BigDecimal;

pub fn berechne_uebersicht(
    einzelbuchungen: &Vec<impl BesitztDatumKategorieUndBetrag>,
) -> Uebersicht {
    let mut monate: Vec<MonatsUebersicht> = vec![];

    for einzelbuchung in einzelbuchungen {
        let mut found = false;
        let datum_als_string = monats_name_from_datum(einzelbuchung.get_datum());
        for monats_uebersicht in &mut monate {
            if monats_uebersicht.name == datum_als_string {
                found = true;
                monats_uebersicht.gesamt =
                    monats_uebersicht.gesamt.clone() + einzelbuchung.get_betrag().clone();
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
            werte.insert(
                einzelbuchung.get_kategorie().clone(),
                einzelbuchung.get_betrag().clone(),
            );
            monate.push(MonatsUebersicht {
                name: datum_als_string,
                werte,
                gesamt: einzelbuchung.get_betrag().clone(),
            });
        }
    }
    Uebersicht { monate }
}

pub fn berechne_personen_uebersicht(gemeinsame_buchungen: &Vec<GemeinsameBuchung>) -> Uebersicht {
    let als_proxy = gemeinsame_buchungen
        .iter()
        .map(PersonAlsKategorieProxy::from)
        .collect::<Vec<PersonAlsKategorieProxy>>();
    berechne_uebersicht(&als_proxy)
}

struct PersonAlsKategorieProxy {
    pub gemeinsame_buchung: GemeinsameBuchung,
}

impl From<&GemeinsameBuchung> for PersonAlsKategorieProxy {
    fn from(gemeinsame_buchung: &GemeinsameBuchung) -> Self {
        PersonAlsKategorieProxy {
            gemeinsame_buchung: gemeinsame_buchung.clone(),
        }
    }
}

impl BesitztDatumKategorieUndBetrag for PersonAlsKategorieProxy {
    fn get_datum(&self) -> &time::Date {
        &self.gemeinsame_buchung.datum
    }

    fn get_kategorie(&self) -> &String {
        &self.gemeinsame_buchung.zielperson
    }

    fn get_betrag(&self) -> &BigDecimal {
        &self.gemeinsame_buchung.wert
    }
}

pub fn combine_to_gemeinsame_uebersicht(
    uebersicht: Uebersicht,
    personen_uebersicht: Uebersicht,
) -> GemeinsameUebersicht {
    let mut monate: Vec<GemeinsameMonatsuebersicht> = vec![];

    for monats_uebersicht in uebersicht.monate {
        let mut personen = std::collections::HashMap::new();
        for p_monate in &personen_uebersicht.monate {
            if p_monate.name != monats_uebersicht.name {
                continue;
            }
            for (person, betrag) in p_monate.werte.iter() {
                personen.insert(person.clone(), betrag.clone());
            }
        }
        monate.push(GemeinsameMonatsuebersicht {
            name: monats_uebersicht.name,
            werte: monats_uebersicht.werte,
            personen,
            gesamt: monats_uebersicht.gesamt,
        });
    }
    GemeinsameUebersicht { monate }
}

#[cfg(test)]
mod tests {
    use super::{MonatsUebersicht, Uebersicht};
    use crate::einzelbuchungen::model::Einzelbuchung;
    use crate::gemeinsame_buchungen::model::GemeinsameBuchung;
    use crate::uebersicht::model::BesitztDatumKategorieUndBetrag;
    use time::Month;

    #[test]
    fn test_berechne_uebersicht_aus_leerer_liste_sollte_leeres_ergebnis_liefern() {
        let buchungen: Vec<Einzelbuchung> = vec![];
        let result = super::berechne_uebersicht(&buchungen);
        assert_eq!(result.monate.len(), 0);
    }

    #[test]
    fn test_berechne_uebersicht_mit_datum_sollte_monatsuebersicht_anlegen() {
        let result = super::berechne_uebersicht(&vec![Einzelbuchung {
            id: "1".to_string(),
            name: "Test".to_string(),
            kategorie: "Kategorie".to_string(),
            wert: 100.into(),
            datum: time::Date::from_calendar_date(2021, Month::January, 1).unwrap(),
            user: "Test".to_string(),
        }]);

        assert_eq!(result.monate.len(), 1);
        assert_eq!(result.monate[0].name, "Januar 2021");
        assert_eq!(result.monate[0].werte.len(), 1);
        assert_eq!(
            result.monate[0].werte.get("Kategorie").unwrap(),
            &100.into()
        );
        assert_eq!(result.monate[0].gesamt, 100.into());
    }

    #[test]
    fn test_berechne_uebersicht_sollte_betraege_gleichen_monats_und_kategorie_addieren() {
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
            },
        ]);

        assert_eq!(result.monate.len(), 1);
        assert_eq!(result.monate[0].name, "Januar 2021");
        assert_eq!(result.monate[0].werte.len(), 1);
        assert_eq!(
            result.monate[0].werte.get("Kategorie").unwrap(),
            &150.into()
        );
        assert_eq!(result.monate[0].gesamt, 150.into());
    }

    #[test]
    fn test_person_als_kategorie_proxy() {
        let buchung = GemeinsameBuchung {
            id: "1".to_string(),
            name: "Test".to_string(),
            kategorie: "Kategorie".to_string(),
            wert: 100.into(),
            datum: time::Date::from_calendar_date(2021, Month::January, 1).unwrap(),
            user: "Test".to_string(),
            zielperson: "Zielperson".to_string(),
        };

        let proxy = super::PersonAlsKategorieProxy::from(&buchung);

        assert_eq!(
            proxy.get_datum(),
            &time::Date::from_calendar_date(2021, Month::January, 1).unwrap()
        );
        assert_eq!(proxy.get_kategorie(), &"Zielperson".to_string());
        assert_eq!(proxy.get_betrag(), &100.into());
    }

    #[test]
    fn combine_to_gemeinsame_uebersicht_should_combine_uebersicht_and_personen_uebersicht() {
        let mut kategorien_map = std::collections::HashMap::new();
        kategorien_map.insert("asdf".to_string(), 200.into());
        let uebersicht = Uebersicht {
            monate: vec![MonatsUebersicht {
                name: "Januar 2021".to_string(),
                werte: kategorien_map.clone(),
                gesamt: 100.into(),
            }],
        };

        let mut personen_map = std::collections::HashMap::new();
        personen_map.insert("Zielperson".to_string(), 50.into());
        let personen_uebersicht = Uebersicht {
            monate: vec![MonatsUebersicht {
                name: "Januar 2021".to_string(),
                werte: personen_map.clone(),
                gesamt: 50.into(),
            }],
        };

        let result = super::combine_to_gemeinsame_uebersicht(uebersicht, personen_uebersicht);

        assert_eq!(result.monate.len(), 1);
        assert_eq!(result.monate[0].name, "Januar 2021");
        assert_eq!(result.monate[0].werte, kategorien_map);
        assert_eq!(result.monate[0].personen, personen_map);
        assert_eq!(result.monate[0].gesamt, 100.into());
    }
}

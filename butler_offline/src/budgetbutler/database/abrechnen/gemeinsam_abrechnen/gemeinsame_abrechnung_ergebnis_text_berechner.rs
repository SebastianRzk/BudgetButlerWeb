use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::berechner::{
    BerechnungsErgebnisModus, GemeinsamAbrechnenVerhaeltnis,
};
use crate::budgetbutler::pages::gemeinsame_buchungen::gemeinsam_abrechnen::Limit;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;
use crate::model::primitives::prozent::Prozent;

pub fn berechne_ergebnis_text(
    verhaeltnis_original: Prozent,
    verhaeltnis_tatsaechlich: Prozent,
    self_name: Person,
    partner_name: Person,
    min_date: Datum,
    max_date: Datum,
    anzahl: u32,
    gesamt_betrag: Betrag,
    limit: Option<Limit>,
    ergebnis: &GemeinsamAbrechnenVerhaeltnis,
) -> String {
    let mut ergebnis_string: Vec<String> = vec![format!(
        "In dieser Abrechnung wurden {} Buchungen im Zeitraum von {} bis {} betrachtet, welche einen Gesamtbetrag von {}€ umfassen.",
        anzahl, min_date.to_german_string(), max_date.to_german_string(), gesamt_betrag.to_german_string()
    )];
    ergebnis_string.push(format!(
        "Es wurde angenommen, dass diese in einem Verhältnis von {}% ({}) zu {}% ({}) aufgeteilt werden sollen.",
        verhaeltnis_original.als_halbwegs_gerundeter_string(), self_name.person, verhaeltnis_original.invertiere().als_halbwegs_gerundeter_string(), partner_name.person
    ));

    if let Some(limit) = limit {
        ergebnis_string.push(format!(
            "Für die Abrechnung wurde ein Limit von {}€ für {} definiert",
            limit.value.to_german_string(),
            limit.fuer.person
        ));
        if ergebnis.modus == BerechnungsErgebnisModus::LimitNichtErreicht {
            ergebnis_string.push("Das Limit wurde nicht erreicht.".to_string());
        } else {
            ergebnis_string.push(
                "Das Limit wurde überschritten. Das neue Verhältnis ist wie folgt:.".to_string(),
            );
            ergebnis_string.push(format!(
                "{}: {}% ({}€) , {}: {}% ({}€)",
                self_name.person,
                verhaeltnis_tatsaechlich.als_halbwegs_gerundeter_string(),
                ergebnis.eigenes.soll.to_german_string(),
                partner_name.person,
                verhaeltnis_tatsaechlich
                    .invertiere()
                    .als_halbwegs_gerundeter_string(),
                ergebnis.partner.soll.to_german_string()
            ));
        }
    } else {
        ergebnis_string.push("Es wurde kein Limit für die Abrechnung definiert.".to_string());
    }

    if ergebnis.eigenes.diff < Betrag::zero().negativ() {
        ergebnis_string.push(format!(
            "Um die Differenz auszugleichen, sollte {} {}€ an {} überweisen.",
            self_name.person,
            ergebnis.eigenes.diff.abs().to_german_string(),
            partner_name.person
        ));
    } else {
        ergebnis_string.push(format!(
            "Um die Differenz auszugleichen, sollte {} {}€ an {} überweisen.",
            partner_name.person,
            ergebnis.partner.diff.abs().to_german_string(),
            self_name.person
        ));
    }

    ergebnis_string.join("\n")
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::berechner::BerechnungsErgebnisModus::{KeinLimit, LimitErreicht, LimitNichtErreicht};
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::berechner::{GemeinsamAbrechnenVerhaeltnis, PersonenVerhaeltnis};
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_ergebnis_text_berechner::berechne_ergebnis_text;
    use crate::budgetbutler::pages::gemeinsame_buchungen::gemeinsam_abrechnen::Limit;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::person::builder::person;
    use crate::model::primitives::prozent::Prozent;

    #[test]
    fn test_kein_limit_50_50_self_mehr_ausgegeben() {
        let ergebnis = berechne_ergebnis_text(
            Prozent::from_int_representation(50),
            Prozent::from_int_representation(50),
            person("IchName"),
            person("PartnerName"),
            Datum::from_iso_string(&"2020-10-10".to_string()),
            Datum::from_iso_string(&"2020-12-12".to_string()),
            10,
            Betrag::from_user_input(&"-100".to_string()),
            None,
            &GemeinsamAbrechnenVerhaeltnis {
                eigenes: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"60".to_string()),
                    diff: Betrag::from_user_input(&"10".to_string()),
                },
                partner: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"40".to_string()),
                    diff: Betrag::from_user_input(&"-10".to_string()),
                },
                modus: KeinLimit,
            },
        );

        assert_eq!(ergebnis, "In dieser Abrechnung wurden 10 Buchungen im Zeitraum von 10.10.2020 bis 12.12.2020 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.\n\
        Es wurde angenommen, dass diese in einem Verhältnis von 50% (IchName) zu 50% (PartnerName) aufgeteilt werden sollen.\nEs wurde kein Limit für die Abrechnung definiert.\n\
        Um die Differenz auszugleichen, sollte PartnerName 10,00€ an IchName überweisen.");
    }

    #[test]
    fn test_kein_limit_50_50_partner_mehr_ausgegeben() {
        let ergebnis = berechne_ergebnis_text(
            Prozent::from_int_representation(50),
            Prozent::from_int_representation(50),
            person("IchName"),
            person("PartnerName"),
            Datum::from_iso_string(&"2020-10-10".to_string()),
            Datum::from_iso_string(&"2020-12-12".to_string()),
            10,
            Betrag::from_user_input(&"-100".to_string()),
            None,
            &GemeinsamAbrechnenVerhaeltnis {
                eigenes: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"40".to_string()),
                    diff: Betrag::from_user_input(&"-10".to_string()),
                },
                partner: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"60".to_string()),
                    diff: Betrag::from_user_input(&"10".to_string()),
                },
                modus: KeinLimit,
            },
        );

        assert_eq!(ergebnis, "In dieser Abrechnung wurden 10 Buchungen im Zeitraum von 10.10.2020 bis 12.12.2020 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.\n\
        Es wurde angenommen, dass diese in einem Verhältnis von 50% (IchName) zu 50% (PartnerName) aufgeteilt werden sollen.\nEs wurde kein Limit für die Abrechnung definiert.\n\
        Um die Differenz auszugleichen, sollte IchName 10,00€ an PartnerName überweisen.");
    }

    #[test]
    fn test_limit_unterschritten_50_50_partner_mehr_ausgegeben() {
        let ergebnis = berechne_ergebnis_text(
            Prozent::from_int_representation(50),
            Prozent::from_int_representation(50),
            person("IchName"),
            person("PartnerName"),
            Datum::from_iso_string(&"2020-10-10".to_string()),
            Datum::from_iso_string(&"2020-12-12".to_string()),
            10,
            Betrag::from_user_input(&"-100".to_string()),
            Some(Limit {
                fuer: person("PartnerName"),
                value: Betrag::from_user_input(&"200".to_string()),
            }),
            &GemeinsamAbrechnenVerhaeltnis {
                eigenes: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"40".to_string()),
                    diff: Betrag::from_user_input(&"-10".to_string()),
                },
                partner: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"50".to_string()),
                    ist: Betrag::from_user_input(&"60".to_string()),
                    diff: Betrag::from_user_input(&"10".to_string()),
                },
                modus: LimitNichtErreicht,
            },
        );

        assert_eq!(ergebnis, "In dieser Abrechnung wurden 10 Buchungen im Zeitraum von 10.10.2020 bis 12.12.2020 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.\n\
        Es wurde angenommen, dass diese in einem Verhältnis von 50% (IchName) zu 50% (PartnerName) aufgeteilt werden sollen.\n\
        Für die Abrechnung wurde ein Limit von 200,00€ für PartnerName definiert\n\
        Das Limit wurde nicht erreicht.\n\
        Um die Differenz auszugleichen, sollte IchName 10,00€ an PartnerName überweisen.");
    }

    #[test]
    fn test_limit_ueberschritten_50_50_partner_mehr_ausgegeben() {
        let ergebnis = berechne_ergebnis_text(
            Prozent::from_int_representation(50),
            Prozent::from_int_representation(60),
            person("IchName"),
            person("PartnerName"),
            Datum::from_iso_string(&"2020-10-10".to_string()),
            Datum::from_iso_string(&"2020-12-12".to_string()),
            10,
            Betrag::from_user_input(&"-100".to_string()),
            Some(Limit {
                fuer: person("PartnerName"),
                value: Betrag::from_user_input(&"40".to_string()),
            }),
            &GemeinsamAbrechnenVerhaeltnis {
                eigenes: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"60".to_string()),
                    ist: Betrag::from_user_input(&"40".to_string()),
                    diff: Betrag::from_user_input(&"-20".to_string()),
                },
                partner: PersonenVerhaeltnis {
                    soll: Betrag::from_user_input(&"40".to_string()),
                    ist: Betrag::from_user_input(&"60".to_string()),
                    diff: Betrag::from_user_input(&"20".to_string()),
                },
                modus: LimitErreicht,
            },
        );

        assert_eq!(ergebnis, "In dieser Abrechnung wurden 10 Buchungen im Zeitraum von 10.10.2020 bis 12.12.2020 betrachtet, welche einen Gesamtbetrag von -100,00€ umfassen.\n\
        Es wurde angenommen, dass diese in einem Verhältnis von 50% (IchName) zu 50% (PartnerName) aufgeteilt werden sollen.\n\
        Für die Abrechnung wurde ein Limit von 40,00€ für PartnerName definiert\n\
        Das Limit wurde überschritten. Das neue Verhältnis ist wie folgt:.\n\
        IchName: 60% (60,00€) , PartnerName: 40% (40,00€)\n\
        Um die Differenz auszugleichen, sollte IchName 20,00€ an PartnerName überweisen.");
    }
}

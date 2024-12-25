use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{generiere_text, HeaderInsertModus, Metadaten, Ziel};
use crate::budgetbutler::database::abrechnen::abrechnen::einzel_buchungen_text_generator::einzelbuchungen_as_import_text;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_text_generator::generiere_einfuehrungs_text;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::primitives::prozent::Prozent;

pub struct Abrechnung {
    pub lines: Vec<Line>,
}

impl Abrechnung {
    pub fn new(lines: Vec<Line>) -> Abrechnung {
        Abrechnung { lines }
    }
}

#[cfg(test)]
pub mod builder {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
    use crate::io::disk::diskrepresentation::line::Line;

    pub fn abrechnung_from_str(str: &str) -> Abrechnung {
        Abrechnung {
            lines: Line::from_multiline_str(str.to_string()),
        }
    }
}

pub struct AbrechnungsErgebnis {
    pub eigene_abrechnung: Abrechnung,
    pub partner_abrechnung: Abrechnung,
    pub selected_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
}

#[derive(Clone)]
pub struct AusgleichsKonfiguration {
    pub ausgleichs_kategorie: Kategorie,
    pub ausgleichs_name: Name,
}

pub struct AusgleichsGesamtKonfiguration {
    pub selbst: AusgleichsKonfiguration,
    pub partner: AusgleichsKonfiguration,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Titel {
    pub titel: String,
}

#[derive(Clone)]
pub struct AbrechnungsWerte {
    pub sum_buchungen_selbst: Betrag,
    pub sum_buchungen_partner: Betrag,
    pub gesamt_betrag: Betrag,
    pub diff_selbst: Betrag,
    pub prozent: Prozent,
}

impl AbrechnungsWerte {
    pub fn inveritere_fuer_partner(&self) -> AbrechnungsWerte {
        AbrechnungsWerte {
            sum_buchungen_selbst: self.sum_buchungen_partner.clone(),
            sum_buchungen_partner: self.sum_buchungen_selbst.clone(),
            gesamt_betrag: self.gesamt_betrag.clone(),
            diff_selbst: self.diff_selbst.invertiere_vorzeichen(),
            prozent: self.prozent.invertiere(),
        }
    }
}

pub fn rechne_ab(
    gemeinsame_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    eigene_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    partner_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    praeable: String,
    partner: Person,
    selbst: Person,
    today: Datum,
    min_date: Datum,
    max_date: Datum,
    ausgleichs_gesamt_konfiguration: AusgleichsGesamtKonfiguration,
    abrechungs_werte: AbrechnungsWerte,
    titel: Titel,
) -> AbrechnungsErgebnis {
    AbrechnungsErgebnis {
        eigene_abrechnung: rechne_ab_fuer_eine_person(
            gemeinsame_buchungen.clone(),
            eigene_buchungen.clone(),
            partner_buchungen.clone(),
            praeable.clone(),
            partner.clone(),
            selbst.clone(),
            today.clone(),
            min_date.clone(),
            max_date.clone(),
            ausgleichs_gesamt_konfiguration.selbst.clone(),
            abrechungs_werte.clone(),
            titel.clone(),
            Ziel::GemeinsameAbrechnungFuerSelbst,
        ),
        partner_abrechnung: rechne_ab_fuer_eine_person(
            gemeinsame_buchungen.clone(),
            partner_buchungen,
            eigene_buchungen,
            praeable,
            selbst,
            partner,
            today,
            min_date,
            max_date,
            ausgleichs_gesamt_konfiguration.partner,
            abrechungs_werte.inveritere_fuer_partner(),
            titel,
            Ziel::GemeinsameAbrechnungFuerPartner,
        ),
        selected_buchungen: gemeinsame_buchungen,
    }
}

fn rechne_ab_fuer_eine_person(
    gemeinsame_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    eigene_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    partner_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    praeable: String,
    partner: Person,
    selbst: Person,
    today: Datum,
    min_date: Datum,
    max_date: Datum,
    ausgleichs_konfiguration: AusgleichsKonfiguration,
    abrechnungs_werte: AbrechnungsWerte,
    titel: Titel,
    ziel: Ziel,
) -> Abrechnung {
    let buchungen = berechne_neue_einzelbuchungen(
        gemeinsame_buchungen,
        abrechnungs_werte.gesamt_betrag.clone(),
        today.clone(),
        ausgleichs_konfiguration,
        abrechnungs_werte.diff_selbst.clone(),
    );
    let einfuehrungs_text = generiere_einfuehrungs_text(
        eigene_buchungen,
        partner_buchungen,
        praeable,
        partner,
        selbst.clone(),
        today.clone(),
        min_date,
        max_date,
        abrechnungs_werte,
    );
    Abrechnung {
        lines: generiere_text(
            einfuehrungs_text,
            einzelbuchungen_as_import_text(&buchungen),
            Metadaten {
                titel,
                ausfuehrungsdatum: today.clone(),
                abrechnende_person: selbst,
                ziel,
                abrechnungsdatum: today,
            },
            HeaderInsertModus::Insert,
        ),
    }
}

fn berechne_neue_einzelbuchungen(
    gemeinsame_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    erwartete_gesamt_summe: Betrag,
    today: Datum,
    ausgleichs_konfiguration: AusgleichsKonfiguration,
    ausgleichs_betrag: Betrag,
) -> Vec<Einzelbuchung> {
    let mut neue_buchungen: Vec<Einzelbuchung> = vec![];
    let mut berechnete_gesamt_summe = Betrag::zero();

    for gemeinsame_buchung in gemeinsame_buchungen {
        let neuer_betrag = gemeinsame_buchung.value.betrag.anteil(&Prozent::p50_50());
        let neue_buchung = Einzelbuchung {
            datum: gemeinsame_buchung.value.datum.clone(),
            name: gemeinsame_buchung.value.name.clone(),
            kategorie: gemeinsame_buchung.value.kategorie.clone(),
            betrag: neuer_betrag.clone(),
        };
        berechnete_gesamt_summe = berechnete_gesamt_summe + neuer_betrag;
        neue_buchungen.push(neue_buchung);
    }

    let differenz = erwartete_gesamt_summe.anteil(&Prozent::p50_50()) - berechnete_gesamt_summe;
    if differenz.abs().as_cent() > 0 {
        let neue_buchung = Einzelbuchung {
            datum: today.clone(),
            name: Name::new("Korrektur Rundung Abrechnung".to_string()),
            kategorie: Kategorie::new("Sonstiges".to_string()),
            betrag: differenz,
        };
        neue_buchungen.push(neue_buchung);
    }

    if ausgleichs_betrag.abs().as_cent() > 0 {
        let neue_buchung = Einzelbuchung {
            datum: today,
            name: ausgleichs_konfiguration.ausgleichs_name.clone(),
            kategorie: ausgleichs_konfiguration.ausgleichs_kategorie.clone(),
            betrag: ausgleichs_betrag,
        };
        neue_buchungen.push(neue_buchung);
    }

    neue_buchungen
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::{berechne_neue_einzelbuchungen, rechne_ab, AbrechnungsWerte, AusgleichsGesamtKonfiguration, AusgleichsKonfiguration, Titel};
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::{kategorie, Kategorie};
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::{demo_person, person};
    use crate::model::primitives::prozent::Prozent;

    #[test]
    fn test_berechne_neue_einzelbuchungen() {
        let result = berechne_neue_einzelbuchungen(
            vec![indiziert(GemeinsameBuchung {
                person: demo_person(),
                name: name("testname"),
                kategorie: Kategorie::new("testkategorie".to_string()),
                betrag: Betrag::new(Vorzeichen::Negativ, 100, 0),
                datum: Datum::new(1, 1, 2021),
            })],
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            Datum::new(2, 1, 2021),
            AusgleichsKonfiguration {
                ausgleichs_kategorie: kategorie("Ausgleichskategorie"),
                ausgleichs_name: name("Ausgleichsname"),
            },
            Betrag::new(Vorzeichen::Positiv, 20, 0),
        );

        assert_eq!(result.len(), 2);
        assert_eq!(result[0].betrag, Betrag::new(Vorzeichen::Negativ, 50, 0));
        assert_eq!(result[0].datum, Datum::new(1, 1, 2021));
        assert_eq!(result[0].kategorie.get_kategorie(), "testkategorie");
        assert_eq!(result[0].name.get_name(), "testname");

        assert_eq!(result[1].betrag, Betrag::new(Vorzeichen::Positiv, 20, 0));
        assert_eq!(result[1].datum, Datum::new(2, 1, 2021));
        assert_eq!(result[1].kategorie.get_kategorie(), "Ausgleichskategorie");
        assert_eq!(result[1].name.get_name(), "Ausgleichsname");
    }

    fn gemeinssame_buchung_1_cent() -> Indiziert<GemeinsameBuchung> {
        indiziert(GemeinsameBuchung {
            person: demo_person(),
            name: name("testname"),
            kategorie: Kategorie::new("testkategorie".to_string()),
            betrag: Betrag::new(Vorzeichen::Negativ, 0, 1),
            datum: Datum::new(1, 1, 2021),
        })
    }

    #[test]
    fn test_berechne_neue_einzelbuchungen_mit_rundungscent() {
        let result = berechne_neue_einzelbuchungen(
            vec![
                gemeinssame_buchung_1_cent(),
                gemeinssame_buchung_1_cent(),
                gemeinssame_buchung_1_cent(),
                gemeinssame_buchung_1_cent(),
            ],
            Betrag::new(Vorzeichen::Negativ, 0, 4),
            Datum::new(2, 1, 2021),
            AusgleichsKonfiguration {
                ausgleichs_kategorie: kategorie("Ausgleichskategorie"),
                ausgleichs_name: name("Ausgleichsname"),
            },
            Betrag::new(Vorzeichen::Positiv, 20, 0),
        );

        assert_eq!(result.len(), 6);
        assert_eq!(result[0].betrag, Betrag::new(Vorzeichen::Negativ, 0, 0));
        assert_eq!(result[1].betrag, Betrag::new(Vorzeichen::Negativ, 0, 0));
        assert_eq!(result[2].betrag, Betrag::new(Vorzeichen::Negativ, 0, 0));
        assert_eq!(result[3].betrag, Betrag::new(Vorzeichen::Negativ, 0, 0));

        assert_eq!(result[4].betrag, Betrag::new(Vorzeichen::Negativ, 0, 2));
        assert_eq!(result[4].datum, Datum::new(2, 1, 2021));
        assert_eq!(result[4].kategorie.get_kategorie(), "Sonstiges");
        assert_eq!(result[4].name.get_name(), "Korrektur Rundung Abrechnung");
    }

    #[test]
    fn test_rechne_ab() {
        let result = rechne_ab(
            vec![
                indiziert(GemeinsameBuchung {
                    person: demo_person(),
                    name: name("testname"),
                    kategorie: Kategorie::new("testkategorie".to_string()),
                    betrag: Betrag::new(Vorzeichen::Negativ, 70, 0),
                    datum: Datum::new(1, 1, 2021),
                }),
                indiziert(GemeinsameBuchung {
                    person: demo_person(),
                    name: name("testnam2"),
                    kategorie: Kategorie::new("testkategorie2".to_string()),
                    betrag: Betrag::new(Vorzeichen::Negativ, 30, 0),
                    datum: Datum::new(1, 1, 2021),
                }),
            ],
            vec![indiziert(GemeinsameBuchung {
                person: demo_person(),
                name: name("testname"),
                kategorie: Kategorie::new("testkategorie".to_string()),
                betrag: Betrag::new(Vorzeichen::Negativ, 70, 0),
                datum: Datum::new(1, 1, 2021),
            })],
            vec![indiziert(GemeinsameBuchung {
                person: demo_person(),
                name: name("testnam2"),
                kategorie: Kategorie::new("testkategorie2".to_string()),
                betrag: Betrag::new(Vorzeichen::Negativ, 30, 0),
                datum: Datum::new(1, 1, 2021),
            })],
            "mein kleiner Abrechnugnstext".to_string(),
            person("PartnerName"),
            person("IchName"),
            Datum::new(3, 1, 2021),
            Datum::new(1, 1, 2021),
            Datum::new(2, 1, 2021),
            AusgleichsGesamtKonfiguration {
                partner: AusgleichsKonfiguration {
                    ausgleichs_name: name("AusgleichPartnerName"),
                    ausgleichs_kategorie: kategorie("AusgleichPartnerKategorie"),
                },
                selbst: AusgleichsKonfiguration {
                    ausgleichs_name: name("AusgleichSelbstName"),
                    ausgleichs_kategorie: kategorie("AusgleichSelbstKategorie"),
                },
            },
            AbrechnungsWerte {
                sum_buchungen_selbst: Betrag::new(Vorzeichen::Negativ, 70, 0),
                sum_buchungen_partner: Betrag::new(Vorzeichen::Negativ, 30, 0),
                gesamt_betrag: Betrag::new(Vorzeichen::Negativ, 100, 0),
                diff_selbst: Betrag::new(Vorzeichen::Negativ, 20, 0),
                prozent: Prozent::from_int_representation(50),
            },
            Titel {
                titel: "AbrechnungsTitel".to_string(),
            },
        );

        let result_eigene_abrechnung = as_string(&result.eigene_abrechnung.lines);
        assert_eq!(
            result_eigene_abrechnung,
            "AbrechnungsTitel
Abrechnung vom 03.01.2021 (von 01.01.2021 bis einschließlich 02.01.2021
########################################


Ergebnis:
mein kleiner Abrechnugnstext


Erfasste Ausgaben:

IchName          -70,00€
PartnerName      -30,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von IchName
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   testname        testkategorie               -70,00€


########################################
Ausgaben von PartnerName
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   testnam2        testkategorie2              -30,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2021-01-03
Abrechnende Person:IchName
Titel:AbrechnungsTitel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2021-01-03
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2021-01-01,testkategorie,testname,-35.00
2021-01-01,testkategorie2,testnam2,-15.00
2021-01-03,AusgleichSelbstKategorie,AusgleichSelbstName,-20.00
#######MaschinenimportEnd"
        );
    }
}

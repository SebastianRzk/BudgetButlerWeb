use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::EinfuehrungsText;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::AbrechnungsWerte;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;

pub fn generiere_einfuehrungs_text(
    eigene_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    partner_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
    praeamble: String,
    partner: Person,
    selbst: Person,
    today: Datum,
    min_date: Datum,
    max_date: Datum,
    abrechnungs_werte: AbrechnungsWerte,
) -> EinfuehrungsText {
    let mut lines = vec![
        Line::from(generate_title(today.clone(), min_date, max_date)),
        Line::from(spacer()),
        Line::empty_line(),
        Line::empty_line(),
        Line::from(ergebnis()),
    ];

    lines.append(&mut Line::from_multiline_str(praeamble));
    lines.push(Line::empty_line());
    lines.push(Line::empty_line());
    lines.push(Line::from(erfasste_ausgaben()));
    lines.push(Line::empty_line());
    lines.append(&mut Line::from_multiline_str(zusammenfassung(
        &selbst,
        abrechnungs_werte.sum_buchungen_selbst,
        &partner,
        abrechnungs_werte.sum_buchungen_partner,
        abrechnungs_werte.gesamt_betrag,
    )));
    lines.push(Line::empty_line());
    lines.push(Line::empty_line());
    lines.append(&mut Line::from_multiline_str(ausgaben_von_headline(
        &selbst,
    )));
    lines.append(&mut Line::from_multiline_str(ausgaben_von_content(
        &eigene_buchungen,
    )));

    lines.push(Line::empty_line());
    lines.push(Line::empty_line());
    lines.append(&mut Line::from_multiline_str(ausgaben_von_headline(
        &partner,
    )));
    lines.append(&mut Line::from_multiline_str(ausgaben_von_content(
        &partner_buchungen,
    )));
    lines.push(Line::empty_line());
    lines.push(Line::empty_line());
    lines.push(Line::empty_line());

    EinfuehrungsText { lines }
}

fn generate_title(today: Datum, min_date: Datum, max_date: Datum) -> String {
    format!(
        "Abrechnung vom {} (von {} bis einschließlich {}",
        today.to_german_string(),
        min_date.to_german_string(),
        max_date.to_german_string()
    )
}

fn spacer() -> String {
    "########################################".to_string()
}

fn ergebnis() -> String {
    "Ergebnis:".to_string()
}

fn erfasste_ausgaben() -> String {
    "Erfasste Ausgaben:".to_string()
}

fn ausgaben_von_headline(person: &Person) -> String {
    format!("{}\nAusgaben von {}\n{}", spacer(), person.person, spacer())
}

fn ausgaben_von_content(buchungen: &Vec<Indiziert<GemeinsameBuchung>>) -> String {
    let mut result = format!(
        "{: <12} {: <15} {: <25} {: >8}€\n",
        "Datum", "Name", "Kategorie", "Betrag"
    );
    for buchung in buchungen {
        result.push_str(&format!(
            "{: <12} {: <15} {: <25} {: >8}€\n",
            buchung.value.datum.to_german_string(),
            buchung.value.name.get_name(),
            buchung.value.kategorie.get_kategorie(),
            buchung.value.betrag.to_german_string()
        ));
    }
    result
}

fn zusammenfassung(
    person_self: &Person,
    person_self_summe: Betrag,
    partner: &Person,
    partner_summe: Betrag,
    gesamt: Betrag,
) -> String {
    format!(
        "{}\n{}\n{}\n{}",
        zusammenfassung_zeile(&person_self.person, person_self_summe),
        zusammenfassung_zeile(&partner.person, partner_summe),
        format!("{:-<22}", ""),
        zusammenfassung_zeile(&"Gesamt".to_string(), gesamt)
    )
}

fn zusammenfassung_zeile(bezeichnung: &String, summe: Betrag) -> String {
    format!("{: <15} {: >7}€", bezeichnung, summe.to_german_string())
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::AbrechnungsWerte;
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_text_generator::generiere_einfuehrungs_text;
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::person;
    use crate::model::primitives::prozent::builder::any_prozent;

    #[test]
    fn test_rechne_ab() {
        let result = generiere_einfuehrungs_text(
            vec![indiziert(GemeinsameBuchung {
                datum: Datum::new(1, 1, 2021),
                name: name("testname"),
                kategorie: kategorie("testkategorie"),
                betrag: zwei(),
                person: person("IchName"),
            })],
            vec![indiziert(GemeinsameBuchung {
                datum: Datum::new(2, 2, 2022),
                name: name("testname2"),
                kategorie: kategorie("testkategorie2"),
                betrag: zwei(),
                person: person("PartnerName"),
            })],
            "preaeamble\nblablabla".to_string(),
            person("PartnerName"),
            person("IchName"),
            Datum::new(1, 1, 2024),
            Datum::new(1, 1, 1999),
            Datum::new(1, 1, 2050),
            AbrechnungsWerte {
                sum_buchungen_selbst: Betrag::new(Vorzeichen::Negativ, 124, 22),
                sum_buchungen_partner: Betrag::new(Vorzeichen::Negativ, 125, 22),
                gesamt_betrag: Betrag::new(Vorzeichen::Negativ, 123, 22),
                prozent: any_prozent(),
                diff_selbst: Betrag::zero(),
            },
        );

        let result_str: String = as_string(&result.lines);

        assert_eq!(
            result_str,
            "Abrechnung vom 01.01.2024 (von 01.01.1999 bis einschließlich 01.01.2050
########################################


Ergebnis:
preaeamble
blablabla


Erfasste Ausgaben:

IchName         -124,22€
PartnerName     -125,22€
----------------------
Gesamt          -123,22€


########################################
Ausgaben von IchName
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   testname        testkategorie                 2,00€


########################################
Ausgaben von PartnerName
########################################
Datum        Name            Kategorie                   Betrag€
02.02.2022   testname2       testkategorie2                2,00€


"
        )
    }
}

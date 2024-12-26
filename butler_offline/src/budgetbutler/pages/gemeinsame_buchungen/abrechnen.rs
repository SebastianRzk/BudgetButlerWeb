use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::{rechne_ab, AbrechnungsErgebnis, AbrechnungsWerte, AusgleichsGesamtKonfiguration, AusgleichsKonfiguration, Titel};
use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_person, filter_auf_zeitraum,
};
use crate::budgetbutler::database::select::functions::sum_by::sum_gemeinsame_buchungen;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::prozent::Prozent;
use crate::model::state::config::UserConfiguration;
use crate::model::state::persistent_application_state::Database;

pub struct GemeinsameBuchungenAbrechnenSubmitContext<'a> {
    pub database: &'a Database,

    pub user_configuration: UserConfiguration,

    pub set_mindate: Datum,
    pub set_maxdate: Datum,
    pub self_soll: Betrag,
    pub ergebnis: String,
    pub set_titel: String,

    pub verhaeltnis: Prozent,
    pub set_self_kategorie: Kategorie,
    pub set_partner_kategorie: Kategorie,

    pub today: Datum,
}

pub fn submit_rechne_ab(context: GemeinsameBuchungenAbrechnenSubmitContext) -> AbrechnungsErgebnis {
    let selektierter_zeitraum =
        context
            .database
            .gemeinsame_buchungen
            .select()
            .filter(filter_auf_zeitraum(
                context.set_mindate.clone(),
                context.set_maxdate.clone(),
            ));
    let eigene_buchungen = selektierter_zeitraum.clone().filter(filter_auf_person(
        context.user_configuration.self_name.clone(),
    ));
    let partner_buchungen = selektierter_zeitraum.clone().filter(filter_auf_person(
        context.user_configuration.partner_name.clone(),
    ));
    let diff_self = ((sum_gemeinsame_buchungen(eigene_buchungen.clone())
        + sum_gemeinsame_buchungen(partner_buchungen.clone()))
    .anteil(&Prozent::p50_50())
        - context.self_soll.clone())
    .invertiere_vorzeichen();
    let titel = Titel {
        titel: context.set_titel.clone(),
    };

    let abrechnungen = rechne_ab(
        selektierter_zeitraum.clone().collect(),
        eigene_buchungen.clone().collect(),
        partner_buchungen.clone().collect(),
        context.ergebnis,
        context.user_configuration.partner_name.clone(),
        context.user_configuration.self_name.clone(),
        context.today,
        context.set_mindate,
        context.set_maxdate,
        AusgleichsGesamtKonfiguration {
            selbst: AusgleichsKonfiguration {
                ausgleichs_kategorie: context.set_self_kategorie,
                ausgleichs_name: Name::new(context.set_titel.clone()),
            },
            partner: AusgleichsKonfiguration {
                ausgleichs_kategorie: context.set_partner_kategorie,
                ausgleichs_name: Name::new(context.set_titel.clone()),
            },
        },
        AbrechnungsWerte {
            sum_buchungen_partner: sum_gemeinsame_buchungen(partner_buchungen),
            sum_buchungen_selbst: sum_gemeinsame_buchungen(eigene_buchungen),
            gesamt_betrag: sum_gemeinsame_buchungen(selektierter_zeitraum.clone()),
            prozent: context.verhaeltnis,
            diff_selbst: diff_self,
        },
        titel,
    );
    abrechnungen
}
#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::gemeinsame_buchungen::abrechnen::GemeinsameBuchungenAbrechnenSubmitContext;
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::model::database::gemeinsame_buchung::builder::gemeinsame_buchung;
    use crate::model::primitives::betrag::builder::minus_fuenfzig;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::person::builder::{demo_partner, demo_self};
    use crate::model::primitives::prozent::Prozent;
    use crate::model::state::config::builder::demo_user_configuration;
    use crate::model::state::persistent_application_state::builder::generate_database_with_gemeinsamen_buchungen;

    #[test]
    fn test_rechne_ab_einfaches_szenario() {
        let datum_innerhalb_zeitraum = datum("2021-01-01");
        let database = generate_database_with_gemeinsamen_buchungen(vec![
            gemeinsame_buchung(
                datum_innerhalb_zeitraum.clone(),
                demo_self(),
                minus_fuenfzig(),
            ),
            gemeinsame_buchung(
                datum_innerhalb_zeitraum.clone(),
                demo_partner(),
                minus_fuenfzig(),
            ),
        ]);

        let context = GemeinsameBuchungenAbrechnenSubmitContext {
            database: &database,
            user_configuration: demo_user_configuration(),
            set_mindate: datum_innerhalb_zeitraum,
            set_maxdate: datum("2022-02-02"),
            self_soll: minus_fuenfzig(),
            ergebnis: "Mein Ergebnis".to_string(),
            set_titel: "Mein Titel".to_string(),
            verhaeltnis: Prozent::p50_50(),
            set_self_kategorie: kategorie("Meine Kategorie"),
            set_partner_kategorie: kategorie("Partner Kategorie"),
            today: datum("2024-01-01"),
        };

        let result = super::submit_rechne_ab(context);

        assert_eq!(
            as_string(&result.eigene_abrechnung.lines),
            EINFACH_EIGENE_ABRECHNUNG
        );
        assert_eq!(
            as_string(&result.partner_abrechnung.lines),
            EINFACH_PARTNER_ABRECHNUNG
        );
    }

    #[test]
    fn test_rechne_ab_komplexes_szenario() {
        let datum_innerhalb_zeitraum = datum("2021-01-01");
        let database = generate_database_with_gemeinsamen_buchungen(vec![
            gemeinsame_buchung(
                datum_innerhalb_zeitraum.clone(),
                demo_self(),
                minus_fuenfzig(),
            ),
            gemeinsame_buchung(
                datum_innerhalb_zeitraum.clone(),
                demo_partner(),
                minus_fuenfzig(),
            ),
        ]);

        let context = GemeinsameBuchungenAbrechnenSubmitContext {
            database: &database,
            user_configuration: demo_user_configuration(),
            set_mindate: datum_innerhalb_zeitraum,
            set_maxdate: datum("2022-02-02"),
            self_soll: Betrag::from_user_input(&"-70".to_string()),
            ergebnis: "Mein Ergebnis".to_string(),
            set_titel: "Mein Titel".to_string(),
            verhaeltnis: Prozent::from_int_representation(70),
            set_self_kategorie: kategorie("Meine Kategorie"),
            set_partner_kategorie: kategorie("Partner Kategorie"),
            today: datum("2024-01-01"),
        };

        let result = super::submit_rechne_ab(context);

        assert_eq!(
            as_string(&result.eigene_abrechnung.lines),
            KOMPLEX_EIGENE_ABRECHNUNG
        );
        assert_eq!(
            as_string(&result.partner_abrechnung.lines),
            KOMPLEX_PARTNER_ABRECHNUNG
        );
    }

    const EINFACH_EIGENE_ABRECHNUNG: &str = "Mein Titel
Abrechnung vom 01.01.2024 (von 01.01.2021 bis einschließlich 02.02.2022
########################################


Ergebnis:
Mein Ergebnis


Erfasste Ausgaben:

Self             -50,00€
Partner          -50,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von Self
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€


########################################
Ausgaben von Partner
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-01-01
Abrechnende Person:Self
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2024-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2021-01-01,Test,Test,-25.00
2021-01-01,Test,Test,-25.00
#######MaschinenimportEnd";

    const EINFACH_PARTNER_ABRECHNUNG: &str = "Mein Titel
Abrechnung vom 01.01.2024 (von 01.01.2021 bis einschließlich 02.02.2022
########################################


Ergebnis:
Mein Ergebnis


Erfasste Ausgaben:

Partner          -50,00€
Self             -50,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von Partner
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€


########################################
Ausgaben von Self
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-01-01
Abrechnende Person:Partner
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2024-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2021-01-01,Test,Test,-25.00
2021-01-01,Test,Test,-25.00
#######MaschinenimportEnd";

    const KOMPLEX_EIGENE_ABRECHNUNG: &str = "Mein Titel
Abrechnung vom 01.01.2024 (von 01.01.2021 bis einschließlich 02.02.2022
########################################


Ergebnis:
Mein Ergebnis


Erfasste Ausgaben:

Self             -50,00€
Partner          -50,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von Self
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€


########################################
Ausgaben von Partner
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-01-01
Abrechnende Person:Self
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2024-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2021-01-01,Test,Test,-25.00
2021-01-01,Test,Test,-25.00
2024-01-01,Meine Kategorie,Mein Titel,-20.00
#######MaschinenimportEnd";

    const KOMPLEX_PARTNER_ABRECHNUNG: &str = "Mein Titel
Abrechnung vom 01.01.2024 (von 01.01.2021 bis einschließlich 02.02.2022
########################################


Ergebnis:
Mein Ergebnis


Erfasste Ausgaben:

Partner          -50,00€
Self             -50,00€
----------------------
Gesamt          -100,00€


########################################
Ausgaben von Partner
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€


########################################
Ausgaben von Self
########################################
Datum        Name            Kategorie                   Betrag€
01.01.2021   Test            Test                        -50,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-01-01
Abrechnende Person:Partner
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2024-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2021-01-01,Test,Test,-25.00
2021-01-01,Test,Test,-25.00
2024-01-01,Partner Kategorie,Mein Titel,20.00
#######MaschinenimportEnd";
}

use crate::budgetbutler::database::abrechnen::abrechnen::importer::{import_abrechnung, update_abrechnung_for_import};
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::Database;

pub struct ImportAbrechnungContext<'a> {
    pub database: &'a Database,
    pub abrechnung: Abrechnung,
    pub heute: Datum,
}

pub struct ImportAbrechnungViewResult {
    pub database: Database,
    pub diff_einzelbuchungen: usize,
    pub diff_gemeinsame_buchungen: usize,
    pub aktualisierte_abrechnung: Vec<Line>,
}

pub fn handle_import_abrechnung(context: ImportAbrechnungContext) -> ImportAbrechnungViewResult {
    let einzelbuchungen_count_before = context.database.einzelbuchungen.select().count();
    let gemeinsame_buchungen_count_before = context.database.gemeinsame_buchungen.select().count();
    let neue_datenbank = import_abrechnung(&context.database, &context.abrechnung);
    let einzelbuchungen_count_after = neue_datenbank.einzelbuchungen.select().count();
    let gemeinsame_buchungen_count_after = neue_datenbank.gemeinsame_buchungen.select().count();

    ImportAbrechnungViewResult {
        database: neue_datenbank,
        diff_einzelbuchungen: einzelbuchungen_count_after - einzelbuchungen_count_before,
        diff_gemeinsame_buchungen: gemeinsame_buchungen_count_after
            - gemeinsame_buchungen_count_before,
        aktualisierte_abrechnung: update_abrechnung_for_import(context.abrechnung, context.heute)
            .lines,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::builder::abrechnung_from_str;
    use crate::budgetbutler::pages::shared::import::{
        handle_import_abrechnung, ImportAbrechnungContext,
    };
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    const DEMO_ABRECHNUNG_INPUT: &str = "\
MeinTitel
Abrechnung vom 29.11.2024 (von 01.11.2024 bis einschließlich 21.11.2024
########################################


Ergebnis:
21.11.2024   asd             NeueKategorie             -1234,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:kein_Partnername_gesetzt
Titel:MeinTitel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2024-11-29
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2024-11-21,NeueKategorie,asd,-617.00
#######MaschinenimportEnd
";

    const DEMO_ABRECHNUNG_OUTPUT: &str = "\
MeinTitel
Abrechnung vom 29.11.2024 (von 01.11.2024 bis einschließlich 21.11.2024
########################################


Ergebnis:
21.11.2024   asd             NeueKategorie             -1234,00€



#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:kein_Partnername_gesetzt
Titel:MeinTitel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2025-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2024-11-21,NeueKategorie,asd,-617.00
#######MaschinenimportEnd";

    #[test]
    fn test_handle_import_abrechnung() {
        let result = handle_import_abrechnung(ImportAbrechnungContext {
            database: &generate_empty_database(),
            abrechnung: abrechnung_from_str(DEMO_ABRECHNUNG_INPUT),
            heute: Datum::new(1, 1, 2025),
        });

        assert_eq!(result.diff_einzelbuchungen, 1);
        assert_eq!(result.diff_gemeinsame_buchungen, 0);
        assert_eq!(
            as_string(&result.aktualisierte_abrechnung),
            DEMO_ABRECHNUNG_OUTPUT
        );
        assert_eq!(result.database.einzelbuchungen.select().count(), 1);
        assert_eq!(result.database.gemeinsame_buchungen.select().count(), 0);
        assert_eq!(
            result.database.einzelbuchungen.get(0).value,
            Einzelbuchung {
                datum: Datum::new(21, 11, 2024),
                kategorie: kategorie("NeueKategorie"),
                name: name("asd"),
                betrag: Betrag::from_user_input(&"-617,00".to_string()),
            }
        )
    }
}

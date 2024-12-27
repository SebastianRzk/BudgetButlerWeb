use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::database::sparkonto::Kontotyp;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::type_description::TypeDescription;
use crate::model::state::non_persistent_application_state::DepotauszugChange;
use crate::model::state::persistent_application_state::Database;

pub struct AddDepotauszugContext<'a> {
    pub database: &'a Database,
    pub depotwerte_changes: &'a Vec<DepotauszugChange>,
    pub edit_buchung: Option<EditDepotauszug>,
    pub heute: Datum,
}

pub struct EditDepotauszug {
    pub datum: Datum,
    pub konto_referenz: KontoReferenz,
}

pub struct AddDepotauszugViewResult {
    pub database_version: String,
    pub bearbeitung: bool,
    pub kontos: Vec<KontoBeschreibung>,
    pub letzte_erfassung: Vec<LetzteErfassung>,
    pub element_titel: String,
    pub approve_titel: String,
}

pub struct KontoBeschreibung {
    pub kontoname: String,
    pub datum: Datum,
    pub filled_items: Vec<KontoItem>,
    pub empty_items: Vec<KontoItem>,
}

pub struct KontoItem {
    pub beschreibung: TypeDescription<String>,
    pub wert: Betrag,
}

pub struct LetzteErfassung {
    pub fa: String,
    pub datum: String,
    pub value: String,
    pub konto: String,
}

pub fn handle_view(context: AddDepotauszugContext) -> AddDepotauszugViewResult {
    let element_titel: String;
    let approve_titel: String;
    let kontos: Vec<KontoBeschreibung>;
    if let Some(edit) = &context.edit_buchung {
        kontos = calc_konto_laden(edit, &context);
        element_titel = "Depotauszug bearbeiten".to_string();
        approve_titel = "Depotauszug bearbeiten".to_string();
    } else {
        kontos = calc_all_kontos(&context);
        element_titel = "Depotauszug erfassen".to_string();
        approve_titel = "Depotauszug erfassen".to_string();
    }

    AddDepotauszugViewResult {
        database_version: context.database.db_version.as_string(),
        kontos,
        bearbeitung: context.edit_buchung.is_some(),
        letzte_erfassung: context
            .depotwerte_changes
            .iter()
            .map(|change| LetzteErfassung {
                fa: change.icon.as_fa.to_string(),
                datum: change.datum.to_german_string(),
                value: change
                    .changes
                    .iter()
                    .map(|x| {
                        format!(
                            "{}: {}",
                            x.depotwert_beschreibung,
                            x.wert.to_german_string()
                        )
                    })
                    .reduce(|x, y| format!("{}\n{}", x, y))
                    .unwrap_or("".to_string()),
                konto: change.konto.konto_name.name.clone(),
            })
            .collect(),
        element_titel,
        approve_titel,
    }
}

fn calc_konto_laden(
    edit: &EditDepotauszug,
    context: &AddDepotauszugContext,
) -> Vec<KontoBeschreibung> {
    let mut kontos = vec![];
    for konto in context
        .database
        .sparkontos
        .select()
        .filter(|k| k.value.name == edit.konto_referenz.konto_name)
        .collect()
    {
        let mut filled_items = vec![];
        let empty_items = vec![];
        for depotwert in context.database.depotwerte.select().collect() {
            let letzter_kontostand = context.database.depotauszuege.select().lade_kontostand(
                depotwert.value.as_referenz(),
                konto.value.as_reference(),
                edit.datum.clone(),
            );
            if letzter_kontostand != Betrag::zero() {
                filled_items.push(KontoItem {
                    beschreibung: calc_depotwert_beschreibung(
                        &depotwert.value.isin,
                        &context.database,
                    ),
                    wert: letzter_kontostand.clone(),
                });
            }
        }
        let konto_template = KontoBeschreibung {
            kontoname: konto.value.name.name,
            datum: edit.datum.clone(),
            filled_items,
            empty_items,
        };
        kontos.push(konto_template);
    }
    kontos
}

fn calc_all_kontos(context: &AddDepotauszugContext) -> Vec<KontoBeschreibung> {
    let mut kontos = vec![];
    for konto in context
        .database
        .sparkontos
        .select()
        .filter(|k| k.value.kontotyp == Kontotyp::Depot)
        .collect()
    {
        let mut filled_items = vec![];
        let mut empty_items = vec![];
        for depotwert in context.database.depotwerte.select().collect() {
            let letzter_kontostand = context
                .database
                .depotauszuege
                .select()
                .get_letzter_kontostand(depotwert.value.as_referenz(), konto.value.as_reference());
            if letzter_kontostand == Betrag::zero() {
                empty_items.push(KontoItem {
                    beschreibung: calc_depotwert_beschreibung(
                        &depotwert.value.isin,
                        &context.database,
                    ),
                    wert: Betrag::zero(),
                });
            } else {
                filled_items.push(KontoItem {
                    beschreibung: calc_depotwert_beschreibung(
                        &depotwert.value.isin,
                        &context.database,
                    ),
                    wert: letzter_kontostand.clone(),
                });
            }
        }
        let konto_template = KontoBeschreibung {
            kontoname: konto.value.name.name,
            datum: context.heute.clone(),
            filled_items,
            empty_items,
        };
        kontos.push(konto_template);
    }
    kontos
}

#[cfg(test)]
mod tests {
    //TODO: Add tests
}

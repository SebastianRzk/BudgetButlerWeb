use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::berechner::{
    berechne_abrechnungs_summen, BerechnungsErgebnisModus,
};
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_ergebnis_text_berechner::berechne_ergebnis_text;
use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_person, filter_auf_zeitraum,
};
use crate::budgetbutler::database::select::functions::sum_by::sum_gemeinsame_buchungen;
use crate::budgetbutler::database::util::calc_kategorien;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::primitives::prozent::Prozent;
use crate::model::state::config::UserConfiguration;
use crate::model::state::persistent_application_state::{Database, DatabaseVersion};

pub struct GemeinsamAbrechnenViewResult {
    pub database_version: DatabaseVersion,

    pub set_self_kategorie: Kategorie,
    pub kategorien: Vec<Kategorie>,

    pub set_other_kategorie: Kategorie,

    pub limit: Option<Limit>,

    pub gesamt_count: u32,
    pub set_count: u32,

    pub mindate: Datum,
    pub maxdate: Datum,
    pub set_mindate: Datum,
    pub set_maxdate: Datum,

    pub myname: Person,
    pub partnername: Person,

    pub ausgabe_partner: Betrag,
    pub ausgabe_partner_prozent: Prozent,
    pub partner_soll: Betrag,
    pub partner_diff: Betrag,

    pub ausgabe_self: Betrag,
    pub ausgabe_self_prozent: Prozent,
    pub self_soll: Betrag,
    pub self_diff: Betrag,

    pub ausgabe_gesamt: Betrag,

    pub ergebnis: String,

    pub set_verhaeltnis_real: Prozent,
    pub set_verhaeltnis: Prozent,

    pub set_titel: String,
}

pub struct GemeinsameBuchungenAbrechnenContext<'a> {
    pub database: &'a Database,

    pub user_configuration: UserConfiguration,

    pub set_mindate: Option<Datum>,
    pub set_maxdate: Option<Datum>,
    pub set_verhaeltnis: Option<u32>,

    pub today: Datum,
    pub extra_kategorie: &'a Option<Kategorie>,

    pub set_self_kategorie: Kategorie,
    pub set_other_kategorie: Kategorie,
    pub set_titel: Option<String>,

    //Optionale Felder
    pub set_limit: Option<Limit>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Limit {
    pub fuer: Person,
    pub value: Betrag,
}

pub fn handle_view(context: GemeinsameBuchungenAbrechnenContext) -> GemeinsamAbrechnenViewResult {
    let datum_list = context
        .database
        .gemeinsame_buchungen
        .select()
        .map(|x| x.value.datum.clone())
        .collect();
    let gesamt_min_datum = datum_list.iter().min().unwrap_or(&context.today);
    let gesamt_max_datum = datum_list.iter().max().unwrap_or(&context.today);

    let set_mindate = context.set_mindate.unwrap_or(gesamt_min_datum.clone());
    let set_maxdate = context.set_maxdate.unwrap_or(gesamt_max_datum.clone());

    let set_verhaeltnis = context.set_verhaeltnis.unwrap_or(50);

    let filtered_zeitraum =
        context
            .database
            .gemeinsame_buchungen
            .select()
            .filter(filter_auf_zeitraum(
                set_mindate.clone(),
                set_maxdate.clone(),
            ));

    let buchungen_von_self = filtered_zeitraum.clone().filter(filter_auf_person(
        context.user_configuration.self_name.clone(),
    ));
    let buchungen_von_partner = filtered_zeitraum.clone().filter(filter_auf_person(
        context.user_configuration.partner_name.clone(),
    ));

    let eigene_summe = sum_gemeinsame_buchungen(buchungen_von_self);
    let partner_summe = sum_gemeinsame_buchungen(buchungen_von_partner);
    let gesamt_summe = eigene_summe.clone() + partner_summe.clone();

    let eigene_summe_prozent = Prozent::from_betrags_differenz(&eigene_summe, &gesamt_summe);
    let partner_summe_prozent = Prozent::from_betrags_differenz(&partner_summe, &gesamt_summe);

    let berechnungs_ergebnis = berechne_abrechnungs_summen(
        set_verhaeltnis.clone(),
        context.set_limit.clone(),
        context.user_configuration.self_name.clone(),
        eigene_summe,
        partner_summe,
        &gesamt_summe,
    );

    let reales_verhaeltnis;
    if berechnungs_ergebnis.modus == BerechnungsErgebnisModus::LimitErreicht {
        reales_verhaeltnis =
            Prozent::from_betrags_differenz(&berechnungs_ergebnis.eigenes.soll, &gesamt_summe);
    } else {
        reales_verhaeltnis = Prozent::from_int_representation(set_verhaeltnis);
    }

    let ergebnis_text = berechne_ergebnis_text(
        Prozent::from_int_representation(set_verhaeltnis),
        reales_verhaeltnis.clone(),
        context.user_configuration.self_name.clone(),
        context.user_configuration.partner_name.clone(),
        set_mindate.clone(),
        set_maxdate.clone(),
        filtered_zeitraum.count() as u32,
        gesamt_summe.clone(),
        context.set_limit.clone(),
        &berechnungs_ergebnis,
    );

    let result = GemeinsamAbrechnenViewResult {
        database_version: context.database.db_version.clone(),
        ergebnis: ergebnis_text,
        set_titel: context.set_titel.clone().unwrap_or("".to_string()),
        set_verhaeltnis_real: reales_verhaeltnis,
        set_verhaeltnis: Prozent::from_int_representation(set_verhaeltnis.clone()),
        gesamt_count: context.database.gemeinsame_buchungen.select().count() as u32,
        set_count: filtered_zeitraum.count() as u32,
        myname: context.user_configuration.self_name,
        partnername: context.user_configuration.partner_name,
        set_self_kategorie: context.set_self_kategorie,
        kategorien: calc_kategorien(&context.database.einzelbuchungen, &context.extra_kategorie),
        set_other_kategorie: context.set_other_kategorie,
        limit: context.set_limit,
        mindate: gesamt_min_datum.clone(),
        maxdate: gesamt_max_datum.clone(),
        set_mindate,
        set_maxdate,
        ausgabe_partner: berechnungs_ergebnis.partner.ist,
        partner_soll: berechnungs_ergebnis.partner.soll,
        partner_diff: berechnungs_ergebnis.partner.diff,
        ausgabe_self: berechnungs_ergebnis.eigenes.ist,
        ausgabe_self_prozent: eigene_summe_prozent,
        ausgabe_partner_prozent: partner_summe_prozent,
        self_soll: berechnungs_ergebnis.eigenes.soll,
        self_diff: berechnungs_ergebnis.eigenes.diff,
        ausgabe_gesamt: gesamt_summe,
    };
    result
}

#[cfg(test)]
mod tests {}

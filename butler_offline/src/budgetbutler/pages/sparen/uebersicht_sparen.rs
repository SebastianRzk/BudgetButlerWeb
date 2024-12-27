use crate::budgetbutler::database::select::functions::keyextractors::{start_ende_aggregation, StartEndeAggregation};
use crate::budgetbutler::database::sparen::berechne_depot_metainfo::{berechne_depot_meta_infos, DepotMetaInfo};
use crate::budgetbutler::pages::sparen::uebersicht_calculations::berechne_anlagetypen::{berechne_anlagetypen, Anlagetyp};
use crate::budgetbutler::pages::sparen::uebersicht_calculations::berechne_delta_entwicklung::make_delta_entwicklung_from_gesamt_entwicklung;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::berechne_delta_entwicklung_pro_jahr::make_delta_entwicklung_pro_jahr_from_delta_entwicklung;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::einnahmen_ausgaben_sparen::{berechne_einnahmen_ausgaben_sparen, EinnahmenAusgabenSparen};
use crate::budgetbutler::pages::sparen::uebersicht_calculations::gesamt_entwicklung::berechne_gesamt_entwicklung;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_ablagetypen_pie::make_uebersicht_anlagetrypen_pie;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_aktuelle_dauerauftraege_pie::make_aktuelle_dauerauftraege_pie;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_dauerauftraege_abzug::make_dauerauftraege_abzuge;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_kontouebersicht_abzug::make_kontouebersicht_abzug;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_ordertypen_pie::make_ordertypen_pie;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::make_uebersicht_kontos_pie::make_uebersicht_kontos_pie;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::order_typen::{berechne_order_typen, OrderTypen};
use crate::budgetbutler::pages::sparen::uebersicht_kontos::{handle_uebersicht_kontos, UebersichtKontosContext};
use crate::model::database::sparkonto::Sparkonto;
use crate::model::indiziert::Indiziert;
use crate::model::metamodel::chart::{BarChart, LineChart, PieChart};
use crate::model::metamodel::jahr_range::JahrRange;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::state::persistent_application_state::Database;

pub struct UebersichtSparenContext<'a> {
    pub database: &'a Database,
    pub aktuelles_jahr: i32,
    pub design_farben: Vec<Farbe>,
    pub heute: Datum,
}

pub struct UebersichtSparenViewResult {
    pub einnahmen_ausgaben_sparen: Vec<EinnahmenAusgabenSparen>,
    pub gesamt_entwicklung: LineChart,
    pub gesamt_entwicklung_delta: LineChart,
    pub gesamt_entwicklung_delta_jahr: BarChart,
    pub depot_metainfos: Vec<DepotMetaInfo>,
    pub uebersicht_kontos: UebersichtKontos,
    pub uebersicht_kontos_pie: PieChart,
    pub anlagetypen: Vec<Anlagetyp>,
    pub anlagetypen_pie: PieChart,
    pub order_typen: OrderTypen,
    pub order_typen_pie: PieChart,
    pub aktuelle_dauerauftraege: Vec<DauerauftragAbzug>,
    pub aktuelle_dauerauftrege_pie: PieChart,
}

pub struct UebersichtKontos {
    pub konten: Vec<KontoMitKontostandUndFarbe>,
    pub gesamt: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
}

pub struct KontoMitKontostandUndFarbe {
    pub konto: Indiziert<Sparkonto>,
    pub kontostand: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
    pub farbe: Farbe,
}

pub struct DauerauftragAbzug {
    pub name: Name,
    pub depotwert_beschreibung: String,
    pub wert: OrderBetrag,
    pub farbe: Farbe,
}

pub fn handle_uebersicht_sparen(context: UebersichtSparenContext) -> UebersichtSparenViewResult {
    let range = JahrRange {
        ende_jahr: context.aktuelles_jahr,
        start_jahr: context
            .database
            .einzelbuchungen
            .select()
            .find_first()
            .map(|x| x.value.datum.jahr)
            .unwrap_or(context.heute.jahr),
    };

    let einnahmen_ausgaben_sparen = berechne_einnahmen_ausgaben_sparen(&range, context.database);
    let konto_uebersicht = handle_uebersicht_kontos(UebersichtKontosContext {
        database: context.database,
    });
    let anlagetypen = berechne_anlagetypen(context.database, context.design_farben.clone());
    let order_typen = berechne_order_typen(context.database);
    let aktuelle_dauerauftraege = context
        .database
        .order_dauerauftraege
        .select()
        .group_as_list_by(start_ende_aggregation(context.heute.clone()))
        .get(&StartEndeAggregation::Aktuelle)
        .unwrap_or(&vec![])
        .clone();

    let gesamt_entwicklung =
        berechne_gesamt_entwicklung(&einnahmen_ausgaben_sparen, context.database);
    let gesamt_entwicklung_delta =
        make_delta_entwicklung_from_gesamt_entwicklung(&gesamt_entwicklung);
    let gesamt_entwicklung_delta_jahr =
        make_delta_entwicklung_pro_jahr_from_delta_entwicklung(&gesamt_entwicklung_delta);
    UebersichtSparenViewResult {
        einnahmen_ausgaben_sparen: einnahmen_ausgaben_sparen.clone(),
        gesamt_entwicklung_delta,
        gesamt_entwicklung_delta_jahr,
        gesamt_entwicklung,
        depot_metainfos: berechne_depot_meta_infos(context.database),
        uebersicht_kontos_pie: make_uebersicht_kontos_pie(
            &konto_uebersicht,
            context.design_farben.clone(),
        ),
        uebersicht_kontos: make_kontouebersicht_abzug(
            konto_uebersicht,
            context.design_farben.clone(),
        ),
        anlagetypen_pie: make_uebersicht_anlagetrypen_pie(
            &anlagetypen,
            context.design_farben.clone(),
        ),
        anlagetypen,
        order_typen_pie: make_ordertypen_pie(&order_typen, context.design_farben.clone()),
        order_typen,
        aktuelle_dauerauftrege_pie: make_aktuelle_dauerauftraege_pie(
            &aktuelle_dauerauftraege,
            context.database,
            context.design_farben.clone(),
        ),
        aktuelle_dauerauftraege: make_dauerauftraege_abzuge(
            aktuelle_dauerauftraege,
            context.design_farben.clone(),
            context.database,
        ),
    }
}

#[cfg(test)]
mod tests {
    //TODO
}

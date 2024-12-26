use crate::budgetbutler::pages::gemeinsame_buchungen::gemeinsam_abrechnen::GemeinsamAbrechnenViewResult;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "gemeinsame_buchungen/gemeinsamabrechnen.html")]
pub struct GemeinsamAbrechnenTemplate {
    pub database_id: String,

    pub set_self_kategorie_value: String,
    pub kategorien: Select<String>,

    pub set_other_kategorie_value: String,

    pub set_limit: bool,
    pub set_limit_value: String,
    pub set_limit_fuer: String,

    pub set_titel: String,

    pub gesamt_count: u32,
    pub set_count: u32,

    pub mindate: String,
    pub maxdate: String,
    pub set_mindate: String,
    pub set_mindate_rfc: String,
    pub set_maxdate: String,
    pub set_maxdate_rfc: String,

    pub myname: String,
    pub partnername: String,

    pub ausgabe_partner: String,
    pub ausgabe_partner_prozent: String,
    pub partner_soll: String,
    pub partner_diff: String,

    pub ausgabe_self: String,
    pub ausgabe_self_prozent: String,
    pub self_soll: String,
    pub self_soll_rfc: String,
    pub self_diff: String,

    pub ausgabe_gesamt: String,

    pub ergebnis: String,

    pub set_verhaeltnis_real: String,
    pub set_verhaeltnis: String,
}

pub fn render_gemeinsame_buchungen_abrechnen(template: GemeinsamAbrechnenViewResult) -> String {
    let as_template: GemeinsamAbrechnenTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_to_template(view_result: GemeinsamAbrechnenViewResult) -> GemeinsamAbrechnenTemplate {
    GemeinsamAbrechnenTemplate {
        database_id: view_result.database_version.as_string(),
        ergebnis: view_result.ergebnis,
        gesamt_count: view_result.gesamt_count,
        myname: view_result.myname.person,
        set_titel: view_result.set_titel,
        kategorien: Select::new(
            view_result
                .kategorien
                .iter()
                .map(|x| x.kategorie.clone())
                .collect(),
            Some(view_result.set_self_kategorie.clone().kategorie),
        ),
        partnername: view_result.partnername.person,
        set_count: view_result.set_count,
        set_limit: view_result.limit.is_some(),
        set_limit_fuer: view_result
            .limit
            .clone()
            .map(|x| x.fuer.person)
            .unwrap_or("".to_string()),
        set_limit_value: view_result
            .limit
            .map(|x| x.value.abs().to_string())
            .unwrap_or("50".to_string()),
        set_mindate: view_result.set_mindate.to_german_string(),
        set_mindate_rfc: view_result.set_mindate.to_iso_string(),
        set_maxdate: view_result.set_maxdate.to_german_string(),
        set_maxdate_rfc: view_result.set_maxdate.to_iso_string(),
        set_other_kategorie_value: view_result.set_other_kategorie.kategorie,
        set_self_kategorie_value: view_result.set_self_kategorie.kategorie,
        ausgabe_gesamt: view_result.ausgabe_gesamt.to_german_string(),
        ausgabe_partner: view_result.ausgabe_partner.to_german_string(),
        ausgabe_self: view_result.ausgabe_self.to_german_string(),
        partner_diff: view_result.partner_diff.to_german_string(),
        partner_soll: view_result.partner_soll.to_german_string(),
        ausgabe_partner_prozent: view_result
            .ausgabe_partner_prozent
            .als_halbwegs_gerundeter_iso_string(),
        ausgabe_self_prozent: view_result
            .ausgabe_self_prozent
            .als_halbwegs_gerundeter_iso_string(),
        self_diff: view_result.self_diff.to_german_string(),
        self_soll: view_result.self_soll.to_german_string(),
        set_verhaeltnis: view_result.set_verhaeltnis.as_string(),
        set_verhaeltnis_real: view_result.set_verhaeltnis_real.as_string(),
        maxdate: view_result.maxdate.to_german_string(),
        mindate: view_result.mindate.to_german_string(),
        self_soll_rfc: view_result.self_soll.to_iso_string(),
    }
}

#[cfg(test)]
mod tests {}

use crate::budgetbutler::database::util::calc_kategorien;
use crate::budgetbutler::view::farbe::FarbenSelektor;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::state::config::Configuration;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct ConfigurationViewResult {
    pub database_id: DatabaseVersion,
    pub database_name: String,

    pub kategorien: Vec<Kategorie>,
    pub partner: Person,

    pub themecolor: Farbe,

    pub ausgeschlossene_kategorien: Vec<Kategorie>,

    pub palette: Vec<FarbenZuordnung>,
}

pub struct FarbenZuordnung {
    pub farbe: Farbe,
    pub kategorie: Kategorie,
}

pub struct ConfigurationContext<'a> {
    pub database: &'a Database,
    pub extra_kategorie: Option<Kategorie>,
    pub config: &'a Configuration,
}

pub fn handle_view(context: ConfigurationContext) -> ConfigurationViewResult {
    ConfigurationViewResult {
        partner: context.config.user_configuration.partner_name.clone(),
        database_id: context.database.db_version.clone(),
        kategorien: calc_kategorien(
            &context.database.einzelbuchungen,
            &context.extra_kategorie,
            &context
                .config
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
        ),
        database_name: context.config.database_configuration.name.clone(),
        themecolor: context.config.design_configuration.design_farbe.clone(),
        palette: berechne_farben_zurordnung(
            context.database.einzelbuchungen.get_kategorien(),
            context
                .config
                .design_configuration
                .configurierte_farben
                .clone(),
        ),
        ausgeschlossene_kategorien: context
            .config
            .erfassungs_configuration
            .ausgeschlossene_kategorien
            .clone(),
    }
}

fn berechne_farben_zurordnung(
    kategorien: Vec<Kategorie>,
    farben: Vec<Farbe>,
) -> Vec<FarbenZuordnung> {
    let selektor = FarbenSelektor::new(kategorien.clone(), farben.clone());
    let mut result = vec![];
    let mut index = 0;

    for kategorie in kategorien {
        let farbe = selektor.get(&kategorie);
        result.push(FarbenZuordnung { farbe, kategorie });
        index += 1;
    }

    while index < farben.len() as u32 {
        result.push(FarbenZuordnung {
            farbe: farben[index as usize].clone(),
            kategorie: Kategorie::new("keine Kategorie gesetzt".to_string()),
        });
        index += 1;
    }

    result
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::farbe::builder::farbe;
    use crate::model::primitives::kategorie::kategorie;

    #[test]
    pub fn test_berechne_farben_zurordnung() {
        let kategorien = vec![kategorie("Kategorie 1"), kategorie("Kategorie 2")];

        let farben = vec![farbe("farbe1"), farbe("farbe2"), farbe("farbe3")];

        let result = super::berechne_farben_zurordnung(kategorien, farben);

        assert_eq!(result.len(), 3);
        assert_eq!(result[0].kategorie.kategorie, "Kategorie 1");
        assert_eq!(result[1].kategorie.kategorie, "Kategorie 2");
        assert_eq!(result[2].kategorie.kategorie, "keine Kategorie gesetzt");

        assert_eq!(result[0].farbe.as_string, "farbe1");
        assert_eq!(result[1].farbe.as_string, "farbe2");
        assert_eq!(result[2].farbe.as_string, "farbe3");
    }
}

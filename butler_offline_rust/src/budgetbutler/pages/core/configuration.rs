use crate::budgetbutler::database::util::calc_kategorien;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::state::config::Config;
use crate::model::state::persistent_application_state::{Database, DatabaseVersion};

pub struct ConfigurationViewResult {
    pub database_id: DatabaseVersion,
    pub database_name: String,

    pub kategorien: Vec<Kategorie>,
    pub partner: Person,

    pub themecolor: Farbe,

    pub ausgeschlossene_kategorien: Vec<Kategorie>,

    pub palette: Vec<FarbenZuordnung>
}


pub struct FarbenZuordnung{
    pub checked: bool,
    pub nummer: u32,
    pub farbe: Farbe,
    pub kategorie: Kategorie,
}


pub struct ConfigurationContext<'a> {
    pub database: &'a Database,
    pub extra_kategorie: Option<Kategorie>,
    pub config: &'a Config,
}


pub fn handle_view(context: ConfigurationContext) -> ConfigurationViewResult {
    ConfigurationViewResult {
        partner: context.config.user_configuration.partner_name.clone(),
        database_id: context.database.db_version.clone(),
        kategorien: calc_kategorien(&context.database.einzelbuchungen, &context.extra_kategorie),
        database_name: context.config.database_configuration.name.clone(),
        themecolor: context.config.design_configuration.design_farbe.clone(),
        //TODO:
        palette: vec![],
        //TODO:
        ausgeschlossene_kategorien: vec![]
    }
}

#[cfg(test)]
mod tests {
    #[test]
    pub  fn test(){
        todo!()
    }
}
use crate::budgetbutler::pages::core::change_config::ChangeConfigViewResult;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::config::{Configuration, ErfassungsConfiguration};

pub struct ChangeAusgeschlosseneKategorienContext<'a> {
    pub neue_ausgeschlossene_kategorien: Vec<Kategorie>,
    pub config: &'a Configuration,
}

pub fn action_change_ausgeschlossene_kategorien(
    context: ChangeAusgeschlosseneKategorienContext,
) -> ChangeConfigViewResult {
    ChangeConfigViewResult {
        new_config: Configuration {
            database_configuration: context.config.database_configuration.clone(),
            erfassungs_configuration: ErfassungsConfiguration {
                ausgeschlossene_kategorien: context.neue_ausgeschlossene_kategorien.clone(),
            },
            user_configuration: context.config.user_configuration.clone(),
            abrechnungs_configuration: context.config.abrechnungs_configuration.clone(),
            backup_configuration: context.config.backup_configuration.clone(),
            design_configuration: context.config.design_configuration.clone(),
            server_configuration: context.config.server_configuration.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::action_change_ausgeschlossene_kategorien::{
        action_change_ausgeschlossene_kategorien, ChangeAusgeschlosseneKategorienContext,
    };
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::config::builder::{
        leere_abrechnungs_configuration, leere_backup_configuration, leere_database_configuration,
        leere_design_configuration, leere_erfassungs_configuration, leere_server_configuration,
        leere_user_configuration,
    };
    use crate::model::state::config::Configuration;

    #[test]
    fn test_action_change_ausgeschlossene_kategorien() {
        let configuration = Configuration {
            database_configuration: leere_database_configuration(),
            server_configuration: leere_server_configuration(),
            erfassungs_configuration: leere_erfassungs_configuration(),
            user_configuration: leere_user_configuration(),
            design_configuration: leere_design_configuration(),
            abrechnungs_configuration: leere_abrechnungs_configuration(),
            backup_configuration: leere_backup_configuration(),
        };

        let context = ChangeAusgeschlosseneKategorienContext {
            neue_ausgeschlossene_kategorien: vec![kategorie("asdf")],
            config: &configuration,
        };

        let result = action_change_ausgeschlossene_kategorien(context);

        assert_eq!(
            result
                .new_config
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
            vec![kategorie("asdf")]
        );
    }
}

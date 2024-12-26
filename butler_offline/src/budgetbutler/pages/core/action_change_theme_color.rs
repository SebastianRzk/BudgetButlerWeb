use crate::budgetbutler::pages::core::change_config::ChangeConfigViewResult;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::config::{Configuration, DesignConfiguration};

pub struct ChangeThemeColorContext<'a> {
    pub neue_farbe: Farbe,
    pub config: &'a Configuration,
}

pub fn action_change_theme_color(context: ChangeThemeColorContext) -> ChangeConfigViewResult {
    ChangeConfigViewResult {
        new_config: Configuration {
            database_configuration: context.config.database_configuration.clone(),
            erfassungs_configuration: context.config.erfassungs_configuration.clone(),
            user_configuration: context.config.user_configuration.clone(),
            abrechnungs_configuration: context.config.abrechnungs_configuration.clone(),
            backup_configuration: context.config.backup_configuration.clone(),
            design_configuration: DesignConfiguration {
                configurierte_farben: context
                    .config
                    .design_configuration
                    .configurierte_farben
                    .clone(),
                design_farbe: context.neue_farbe.clone(),
            },
            server_configuration: context.config.server_configuration.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::action_change_theme_color::{
        action_change_theme_color, ChangeThemeColorContext,
    };
    use crate::model::primitives::farbe::builder::farbe;
    use crate::model::state::config::builder::{
        leere_abrechnungs_configuration, leere_backup_configuration, leere_database_configuration,
        leere_design_configuration, leere_erfassungs_configuration, leere_server_configuration,
        leere_user_configuration,
    };
    use crate::model::state::config::Configuration;

    #[test]
    fn test_action_change_theme_color() {
        let configuration = Configuration {
            database_configuration: leere_database_configuration(),
            server_configuration: leere_server_configuration(),
            erfassungs_configuration: leere_erfassungs_configuration(),
            user_configuration: leere_user_configuration(),
            design_configuration: leere_design_configuration(),
            abrechnungs_configuration: leere_abrechnungs_configuration(),
            backup_configuration: leere_backup_configuration(),
        };

        let context = ChangeThemeColorContext {
            neue_farbe: farbe("neue Farbe"),
            config: &configuration,
        };

        let result = action_change_theme_color(context);

        assert_eq!(
            result.new_config.design_configuration.design_farbe,
            farbe("neue Farbe")
        );
    }
}

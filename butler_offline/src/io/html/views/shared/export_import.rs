use crate::model::remote::server::ServerConfiguration;
use crate::model::state::persistent_state::database_version::DatabaseVersion;
pub use askama::Template;

#[derive(Template)]
#[template(path = "shared/import.html")]
pub struct ExportImportTemplate {
    pub database_id: String,
    pub online_default_server: String,
}

#[derive(Clone)]
pub struct ExportImportViewResult {
    pub database_version: DatabaseVersion,
    pub online_default_server: ServerConfiguration,
}

pub fn render_import_template(template: ExportImportViewResult) -> String {
    let as_template: ExportImportTemplate = map_to_template(template);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: ExportImportViewResult) -> ExportImportTemplate {
    ExportImportTemplate {
        database_id: view_result.database_version.as_string(),
        online_default_server: view_result.online_default_server.server_url.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::io::html::views::shared::export_import::ExportImportViewResult;
    use crate::model::remote::server::ServerConfiguration;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    fn test_map_to_template() {
        let result = ExportImportViewResult {
            database_version: DatabaseVersion {
                name: "test".to_string(),
                version: 2,
                session_random: 2,
            },
            online_default_server: ServerConfiguration::new("test".to_string()),
        };

        let template = super::map_to_template(result);

        assert_eq!(template.database_id, "test-2-2");
        assert_eq!(template.online_default_server, "test");
    }
}

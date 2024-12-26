use crate::budgetbutler::database::abrechnen::abrechnen::importer::KategorieMitBeispiel;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::io::disk::diskrepresentation::line::as_string;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_state::database_version::DatabaseVersion;
pub use askama::Template;
use crate::io::html::input::select::Select;

pub const ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT: &str = "Als neue Kategorie importieren";

#[derive(Template)]
#[template(path = "shared/import_mapping.html")]
pub struct ImportMappingTemplate {
    pub database_id: String,
    pub abrechnung: String,
    pub alle_kategorie_optionen: Select<String>,
    pub unpassende_kategorien: Vec<KategorieMitBeispielTemplate>,
}

pub struct ImportMappingViewResult {
    pub database_version: DatabaseVersion,
    pub abrechnung: Abrechnung,
    pub alle_kategorien: Vec<Kategorie>,
    pub unpassende_kategorien: Vec<KategorieMitBeispiel>,
}

#[derive(Debug, Clone)]
pub struct KategorieMitBeispielTemplate {
    pub name: String,
    pub beispiel: String,
}

pub fn render_import_mapping_template(template: ImportMappingViewResult) -> String {
    let as_template: ImportMappingTemplate = map_to_template(template);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: ImportMappingViewResult) -> ImportMappingTemplate {
    let mut kategorie_moeglichkeiten: Vec<String> = view_result
        .alle_kategorien
        .iter()
        .map(|x| x.kategorie.clone())
        .collect();
    kategorie_moeglichkeiten.push(ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT.to_string());

    ImportMappingTemplate {
        database_id: view_result.database_version.as_string(),
        alle_kategorie_optionen: Select::new(
            kategorie_moeglichkeiten,
            Some(ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT.to_string()),
        ),
        unpassende_kategorien: view_result
            .unpassende_kategorien
            .iter()
            .map(|x| KategorieMitBeispielTemplate {
                name: x.kategorie.kategorie.clone(),
                beispiel: x.beispiel.join("\n"),
            })
            .collect(),
        abrechnung: as_string(&view_result.abrechnung.lines),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::io::html::views::shared::import_mapping::ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    fn test_map_to_template() {
        let view_result = super::ImportMappingViewResult {
            database_version: demo_database_version(),
            abrechnung: Abrechnung {
                lines: vec![line("abrechnung")],
            },
            alle_kategorien: vec![kategorie("kategorie")],
            unpassende_kategorien: vec![super::KategorieMitBeispiel {
                kategorie: kategorie("unpassende kategorie"),
                beispiel: vec!["beispiel".to_string()],
            }],
        };
        let template = super::map_to_template(view_result);
        assert_eq!(template.database_id, "empty-0-0");
        assert_eq!(template.abrechnung, "abrechnung");
        assert_eq!(template.alle_kategorie_optionen.items.len(), 2);
        assert_eq!(template.alle_kategorie_optionen.items[0].value, "kategorie");
        assert_eq!(template.alle_kategorie_optionen.items[0].selected, false);
        assert_eq!(
            template.alle_kategorie_optionen.items[1].value,
            ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT
        );
        assert_eq!(template.alle_kategorie_optionen.items[1].selected, true);
        assert_eq!(template.unpassende_kategorien.len(), 1);
        assert_eq!(
            template.unpassende_kategorien[0].name,
            "unpassende kategorie"
        );
        assert_eq!(template.unpassende_kategorien[0].beispiel, "beispiel");
    }
}

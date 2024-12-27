use crate::budgetbutler::view::icons::{Icon, COGS, DASHBOARD, LINE_CHART, LIST, PLUS, RELOAD};
use crate::budgetbutler::view::routes::{
    CORE_CONFIGURATION, CORE_IMPORT, CORE_RELOAD_DATABASE, EINZELBUCHUNGEN_AUSGABE_ADD,
    EINZELBUCHUNGEN_DAUERAUFTRAG_ADD, EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT,
    EINZELBUCHUNGEN_EINNAHME_ADD, EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT,
    EINZELBUCHUNGEN_JAHRESUEBERSICHT, EINZELBUCHUNGEN_MONATSUEBERSICHT,
    GEMEINSAME_BUCHUNGEN_ABRECHNEN, GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN, GEMEINSAME_BUCHUNGEN_ADD,
    GEMEINSAME_BUCHUNGEN_UEBERSICHT, SPAREN_DEPOTAUSZUEGE_UEBERSICHT, SPAREN_DEPOTAUSZUG_ADD,
    SPAREN_DEPOTWERTE_UEBERSICHT, SPAREN_DEPOTWERT_ADD, SPAREN_ORDERDAUERAUFTRAG_ADD,
    SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT, SPAREN_ORDER_ADD, SPAREN_ORDER_UEBERSICHT,
    SPAREN_SPARBUCHUNGEN_UEBERSICHT, SPAREN_SPARBUCHUNG_ADD, SPAREN_SPARKONTO_ADD,
    SPAREN_SPARKONTO_UEBERSICHT, SPAREN_UEBERSICHT, SPAREN_UEBERSICHT_ETFS,
};
use std::string::ToString;

pub const PERSOENLICHE_FINANZEN: &str = "Persönliche Finanzen";
pub const GEMEINSAME_FINANZEN: &str = "Gemeinsame Finanzen";
pub const SPAREN: &str = "Sparen";
pub const EINSTELLUNGEN: &str = "Einstellungen";

pub fn einzelbuchungen_menu() -> RootMenu {
    RootMenu {
        icon: DASHBOARD,
        name: PERSOENLICHE_FINANZEN.to_string(),
        sub_menu: vec![
            MenuEntry {
                url: EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT.to_string(),
                name: "Übersicht Einzelbuchungen".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT.to_string(),
                name: "Übersicht Daueraufträge".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_AUSGABE_ADD.to_string(),
                name: "Neue Ausgabe".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_EINNAHME_ADD.to_string(),
                name: "Neue Einnahme".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_DAUERAUFTRAG_ADD.to_string(),
                name: "Neuer Dauerauftrag".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_MONATSUEBERSICHT.to_string(),
                name: "Monatsübersicht".to_string(),
                icon: LINE_CHART,
            },
            MenuEntry {
                url: EINZELBUCHUNGEN_JAHRESUEBERSICHT.to_string(),
                name: "Jahresübersicht".to_string(),
                icon: LINE_CHART,
            },
            MenuEntry {
                url: CORE_IMPORT.to_string(),
                name: "Export / Import".to_string(),
                icon: COGS,
            },
        ],
    }
}

pub fn gemeinsame_buchungen_menu() -> RootMenu {
    RootMenu {
        icon: DASHBOARD,
        name: GEMEINSAME_FINANZEN.to_string(),
        sub_menu: vec![
            MenuEntry {
                url: GEMEINSAME_BUCHUNGEN_UEBERSICHT.to_string(),
                name: "Übersicht Buchungen".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: GEMEINSAME_BUCHUNGEN_ADD.to_string(),
                name: "Neue gemeinsame Ausgabe".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: GEMEINSAME_BUCHUNGEN_ABRECHNEN.to_string(),
                name: "Gemeinsam abrechnen".to_string(),
                icon: COGS,
            },
            MenuEntry {
                url: CORE_IMPORT.to_string(),
                name: "Export / Import".to_string(),
                icon: COGS,
            },
            MenuEntry {
                url: GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN.to_string(),
                name: "Übersicht Abrechnungen".to_string(),
                icon: LIST,
            },
        ],
    }
}

pub fn einstellungen_menu() -> RootMenu {
    RootMenu {
        icon: COGS,
        name: EINSTELLUNGEN.to_string(),
        sub_menu: vec![
            MenuEntry {
                url: CORE_CONFIGURATION.to_string(),
                name: "Allgemeine Einstellungen".to_string(),
                icon: COGS,
            },
            MenuEntry {
                url: CORE_RELOAD_DATABASE.to_string(),
                name: "Datenbank neu laden".to_string(),
                icon: RELOAD,
            },
        ],
    }
}

pub fn sparen_menu() -> RootMenu {
    RootMenu {
        icon: DASHBOARD,
        name: SPAREN.to_string(),
        sub_menu: vec![
            MenuEntry {
                url: SPAREN_UEBERSICHT.to_string(),
                name: "Sparen Übersicht".to_string(),
                icon: LINE_CHART,
            },
            MenuEntry {
                url: SPAREN_UEBERSICHT_ETFS.to_string(),
                name: "ETF Übersicht".to_string(),
                icon: LINE_CHART,
            },
            MenuEntry {
                url: SPAREN_SPARBUCHUNG_ADD.to_string(),
                name: "Neue Sparbuchung".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_SPARKONTO_ADD.to_string(),
                name: "Neues Sparkonto".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_DEPOTWERT_ADD.to_string(),
                name: "Neuer Depotwert".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_ORDER_ADD.to_string(),
                name: "Neuer Order".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_ORDERDAUERAUFTRAG_ADD.to_string(),
                name: "Neuer Order-Dauerauftrag".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_DEPOTAUSZUG_ADD.to_string(),
                name: "Neuer Depotauszug".to_string(),
                icon: PLUS,
            },
            MenuEntry {
                url: SPAREN_SPARBUCHUNGEN_UEBERSICHT.to_string(),
                name: "Übersicht Sparbuchungen".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: SPAREN_SPARKONTO_UEBERSICHT.to_string(),
                name: "Übersicht Sparkonten".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: SPAREN_DEPOTWERTE_UEBERSICHT.to_string(),
                name: "Übersicht Depotwerte".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: SPAREN_ORDER_UEBERSICHT.to_string(),
                name: "Übersicht Orders".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT.to_string(),
                name: "Übersicht Order-Daueraufträge".to_string(),
                icon: LIST,
            },
            MenuEntry {
                url: SPAREN_DEPOTAUSZUEGE_UEBERSICHT.to_string(),
                name: "Übersicht Depotauszüge".to_string(),
                icon: LIST,
            },
        ],
    }
}

pub struct RootMenu {
    pub name: String,
    pub icon: Icon,
    pub sub_menu: Vec<MenuEntry>,
}

pub struct MenuEntry {
    pub url: String,
    pub name: String,
    pub icon: Icon,
}

pub fn resolve_active_group_from_url(url: &str) -> String {
    let mut found: Option<String> = None;
    for entry in sparen_menu().sub_menu {
        if entry.url == url {
            found = Some(SPAREN.to_string());
        }
    }

    for entry in gemeinsame_buchungen_menu().sub_menu {
        if entry.url == url {
            found = Some(GEMEINSAME_FINANZEN.to_string());
        }
    }

    for entry in einstellungen_menu().sub_menu {
        if entry.url == url {
            found = Some(EINSTELLUNGEN.to_string());
        }
    }

    found.unwrap_or(PERSOENLICHE_FINANZEN.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_resolve_active_group_from_url() {
        assert_eq!(
            resolve_active_group_from_url(EINZELBUCHUNGEN_JAHRESUEBERSICHT),
            PERSOENLICHE_FINANZEN
        );
        assert_eq!(resolve_active_group_from_url(SPAREN_UEBERSICHT), SPAREN);
        assert_eq!(
            resolve_active_group_from_url(GEMEINSAME_BUCHUNGEN_UEBERSICHT),
            GEMEINSAME_FINANZEN
        );
        assert_eq!(
            resolve_active_group_from_url(CORE_CONFIGURATION),
            EINSTELLUNGEN
        );

        assert_eq!(
            resolve_active_group_from_url("asdfg"),
            PERSOENLICHE_FINANZEN
        );
    }
}

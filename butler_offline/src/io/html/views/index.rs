use crate::budgetbutler::view::menu::{
    einstellungen_menu, einzelbuchungen_menu, gemeinsame_buchungen_menu, sparen_menu, RootMenu,
};
use crate::budgetbutler::view::request_handler::SuccessMessage;
use askama::Template;

#[derive(Template)]
#[template(path = "index.html")]
pub struct IndexTemplate {
    pub nutzername: String,
    pub active_page_url: String,
    pub active: String,
    pub element_titel: String,
    pub menu: Vec<RootMenuTemplate>,
    pub content: String,
    pub message: Option<MessageTemplate>,
    pub info_messages: Vec<InfoMessageTemplate>,
}

pub struct RootMenuTemplate {
    pub name: String,
    pub icon: String,
    pub sub_menu: Vec<MenuEntryTemplate>,
}

pub struct MenuEntryTemplate {
    pub url: String,
    pub name: String,
    pub icon: String,
}

pub struct MessageTemplate {
    pub content: String,
    pub message_type: String,
}

pub struct InfoMessageTemplate {
    pub content: String,
    pub vorgeschlagene_problembehebungen: Vec<VorgeschlageneProblembehebung>,
}

pub struct VorgeschlageneProblembehebung {
    pub link: String,
    pub link_beschreibung: String,
}

pub fn map_to_template(
    active_menu_group: String,
    active_page_url: String,
    element_titel: String,
    content: String,
    menu: Vec<RootMenu>,
    success_message: Option<SuccessMessage>,
    name: String,
) -> IndexTemplate {
    IndexTemplate {
        nutzername: name,
        active_page_url,
        active: active_menu_group,
        element_titel,
        content,
        menu: map_menu_to_template(menu),
        info_messages: vec![],
        message: success_message.map(|message| MessageTemplate {
            content: message.message.clone(),
            message_type: "success".to_string(),
        }),
    }
}

fn map_menu_to_template(menu: Vec<RootMenu>) -> Vec<RootMenuTemplate> {
    menu.iter()
        .map(|root_menu| RootMenuTemplate {
            icon: root_menu.icon.as_fa.to_string(),
            name: root_menu.name.clone(),
            sub_menu: root_menu
                .sub_menu
                .iter()
                .map(|menu_entry| MenuEntryTemplate {
                    url: menu_entry.url.clone(),
                    name: menu_entry.name.clone(),
                    icon: menu_entry.icon.as_fa.to_string(),
                })
                .collect(),
        })
        .collect()
}

pub fn render_index_template(
    active_menu_group: String,
    active_page_url: String,
    page_title: String,
    content: String,
    success_message: Option<SuccessMessage>,
    name: String,
) -> String {
    let as_template: IndexTemplate = map_to_template(
        active_menu_group,
        active_page_url,
        page_title,
        content,
        vec![
            einzelbuchungen_menu(),
            gemeinsame_buchungen_menu(),
            sparen_menu(),
            einstellungen_menu(),
        ],
        success_message,
        name,
    );
    as_template.render().unwrap()
}

use crate::budgetbutler::view::request_handler::Redirect;
use crate::io::http::redirect::http_redirect;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::non_persistent_application_state::AdditionalKategorie;
use actix_web::web::{Data, Form};
use actix_web::{post, Responder};
use serde::Deserialize;

#[post("addkategorie/")]
pub async fn add_kategorie(
    data: Data<AdditionalKategorie>,
    form: Form<AddKategorieForm>,
) -> impl Responder {
    let mut data = data.kategorie.lock().unwrap();
    *data = Some(Kategorie::new(form.neue_kategorie.clone()));
    drop(data);
    http_redirect(Redirect {
        target: form.redirect.clone(),
    })
}

#[derive(Deserialize)]
pub struct AddKategorieForm {
    pub neue_kategorie: String,
    pub redirect: String,
}

pub use askama::Template;

#[derive(Template)]
#[template(path = "success_zurueck_zu.html")]
pub struct SuccessZurueckZuTemplate {
    link: String,
    text: String,
}

pub struct SuccessZurueckZuViewResult {
    pub link: String,
    pub text: String,
}

pub fn render_success_message_template(context: SuccessZurueckZuViewResult) -> String {
    SuccessZurueckZuTemplate {
        text: context.text,
        link: context.link,
    }
    .render()
    .unwrap()
}

use serde::Serialize;

#[derive(Serialize)]
pub struct ResultDto {
    result: String,
    message: String,
}

pub fn result_success(message: &str) -> ResultDto {
    ResultDto {
        result: "OK".to_string(),
        message: message.to_string(),
    }
}

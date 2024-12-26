use crate::model::remote::login::LoginCredentials;
use reqwest::Client;
use std::fmt::Debug;

pub async fn get_request(
    route: String,
    login_credentials: LoginCredentials,
) -> Result<String, ErrorOnRequest> {
    println!("GET request for {}", route);
    let formatted_cookie = format!(
        "{}={}",
        login_credentials.session_cookie.name, login_credentials.session_cookie.value
    );
    let builder1 = Client::builder()
        .build()
        .unwrap()
        .get(route)
        .header("Cookie", formatted_cookie)
        .header("Accept", "application/json");
    let r_raw = builder1.send().await.map_err(|_| ErrorOnRequest {})?;
    println!("HTTP Status{:?}", r_raw.status());
    let test = r_raw.text().await.map_err(|_| ErrorOnRequest {})?;
    println!("Result text {:?}", test);
    Ok(test)
}

pub async fn post_request(
    route: String,
    login_credentials: LoginCredentials,
    body: String,
) -> Result<(), ErrorOnRequest> {
    println!("POST request for {}", route);
    let formatted_cookie = format!(
        "{}={}",
        login_credentials.session_cookie.name, login_credentials.session_cookie.value
    );
    let builder1 = Client::builder()
        .build()
        .unwrap()
        .post(route)
        .header("Cookie", formatted_cookie)
        .header("Accept", "application/json")
        .header("Content-Type", "application/json")
        .body(body);
    let r_raw = builder1.send().await.map_err(|_| ErrorOnRequest {})?;
    let status = r_raw.status();
    println!("HTTP Status{:?}", status);
    let test = r_raw.text().await.map_err(|_| ErrorOnRequest {})?;
    println!("Result text {:?}", test);
    if status.is_success() {
        Ok(())
    } else {
        Err(ErrorOnRequest {})
    }
}

pub async fn delete_request(
    route: String,
    login_credentials: LoginCredentials,
) -> Result<(), ErrorOnRequest> {
    println!("DELETE request for {}", route);
    let formatted_cookie = format!(
        "{}={}",
        login_credentials.session_cookie.name, login_credentials.session_cookie.value
    );
    let builder1 = Client::builder()
        .build()
        .unwrap()
        .delete(route)
        .header("Cookie", formatted_cookie)
        .header("Accept", "application/json");
    let r_raw = builder1.send().await.map_err(|_| ErrorOnRequest {})?;
    let status = r_raw.status();
    println!("HTTP Status{:?}", status);
    let test = r_raw.text().await.map_err(|_| ErrorOnRequest {})?;
    println!("Result text {:?}", test);
    if status.is_success() {
        Ok(())
    } else {
        Err(ErrorOnRequest {})
    }
}

#[derive(Debug)]
pub struct ErrorOnRequest {}

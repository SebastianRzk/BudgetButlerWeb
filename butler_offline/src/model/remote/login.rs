#[derive(Debug, Clone)]
pub struct LoginCredentials {
    pub username: String,
    pub session_cookie: Cookie,
}

#[derive(Debug, Clone)]
pub struct Cookie {
    pub name: String,
    pub value: String,
}

impl Cookie {
    pub fn from_session_str(session: String) -> Cookie {
        let splitted_session = session.split('=').collect::<Vec<&str>>();
        println!("{:?}", splitted_session);
        Cookie {
            name: splitted_session[0].to_string(),
            value: splitted_session[1].to_string(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::remote::login::Cookie;

    #[test]
    fn should_create_cookie_from_session_string() {
        let session = "key=value".to_string();

        let cookie = Cookie::from_session_str(session);

        assert_eq!(cookie.name, "key");
        assert_eq!(cookie.value, "value");
    }
}

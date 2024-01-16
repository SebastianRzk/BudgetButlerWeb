// @generated automatically by Diesel CLI.

diesel::table! {
    einzelbuchungen (id) {
        #[max_length = 36]
        id -> Varchar,
        #[max_length = 60]
        name -> Varchar,
        #[max_length = 60]
        kategorie -> Varchar,
        wert -> Decimal,
        datum -> Date,
        #[max_length = 60]
        user -> Varchar,
    }
}

diesel::table! {
    gemeinsame_buchungen (id) {
        #[max_length = 36]
        id -> Varchar,
        #[max_length = 60]
        name -> Varchar,
        #[max_length = 60]
        kategorie -> Varchar,
        wert -> Decimal,
        datum -> Date,
        #[max_length = 60]
        user -> Varchar,
        #[max_length = 60]
        zielperson -> Varchar,
    }
}

diesel::table! {
    kategorien (id) {
        #[max_length = 36]
        id -> Varchar,
        #[max_length = 60]
        name -> Varchar,
        #[max_length = 60]
        user -> Varchar,
    }
}

diesel::table! {
    partner (user) {
        #[max_length = 60]
        zielperson -> Varchar,
        #[max_length = 60]
        user -> Varchar,
    }
}

diesel::allow_tables_to_appear_in_same_query!(
    einzelbuchungen,
    gemeinsame_buchungen,
    kategorien,
    partner,
);

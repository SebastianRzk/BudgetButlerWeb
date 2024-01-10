pub struct NeuerPartnerStatus {
    pub name: String,
    pub user: String,
}

#[derive(Clone)]
pub struct PartnerStatus {
    pub zielperson: String,
    pub user: String,
    pub bestaetigt: bool,
}

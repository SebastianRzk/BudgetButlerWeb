use crate::database::DbError;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};

use crate::partner::model::{NeuerPartnerStatus, PartnerStatus};
use crate::schema::partner;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = partner)]
pub struct PartnerStatusEntity {
    pub zielperson: String,
    pub user: String,
}

impl NeuerPartnerStatus {
    pub fn to_entity(&self) -> PartnerStatusEntity {
        PartnerStatusEntity {
            zielperson: self.name.clone(),
            user: self.user.clone(),
        }
    }
}

impl PartnerStatusEntity {
    pub fn to_domain(&self, bestaetigt: bool) -> PartnerStatus {
        PartnerStatus {
            zielperson: self.zielperson.clone(),
            user: self.user.clone(),
            bestaetigt: bestaetigt.clone(),
        }
    }
}

pub fn calculate_partnerstatus(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<PartnerStatus, DbError> {
    use crate::schema::partner::dsl::*;

    let partnerstatus = load_partnerstatus(conn, &user_name)?;

    if partnerstatus.clone().is_some() {
        let mut bestaetigt = false;
        let status_des_partners: Option<PartnerStatusEntity> = partner
            .filter(user.eq(partnerstatus.clone().unwrap().zielperson))
            .filter(zielperson.eq(user_name.clone()))
            .first::<PartnerStatusEntity>(conn)
            .optional()?;
        if status_des_partners.clone().is_some() {
            bestaetigt = true
        }
        return Ok(partnerstatus.unwrap().to_domain(bestaetigt));
    };

    Ok(PartnerStatus {
        bestaetigt: false,
        zielperson: String::from(""),
        user: user_name.clone(),
    })
}

fn load_partnerstatus(
    conn: &mut MysqlConnection,
    user_name: &String,
) -> Result<Option<PartnerStatusEntity>, DbError> {
    use crate::schema::partner::dsl::*;
    let partnerstatus: Option<PartnerStatusEntity> = partner
        .filter(user.eq(user_name.clone()))
        .first::<PartnerStatusEntity>(conn)
        .optional()?;
    Ok(partnerstatus)
}

pub fn update_partnerstatus(
    conn: &mut MysqlConnection,
    neuer_partnerstatus: NeuerPartnerStatus,
) -> Result<PartnerStatus, DbError> {
    let username = &neuer_partnerstatus.user;
    let aktueller_partnerstatus = load_partnerstatus(conn, &username);
    if aktueller_partnerstatus.is_ok() && aktueller_partnerstatus.unwrap().is_some() {
        delete_partnerstatus(conn, username.clone()).unwrap();
    };

    let partner_status_entity = neuer_partnerstatus.to_entity();

    use crate::schema::partner::dsl::*;
    diesel::insert_into(partner)
        .values(&partner_status_entity)
        .execute(conn)?;

    calculate_partnerstatus(conn, username.to_string())
}

pub struct DeleteResult {}

pub fn delete_partnerstatus(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<DeleteResult, DbError> {
    use crate::schema::partner::dsl::*;

    diesel::delete(partner)
        .filter(user.eq(user_name))
        .execute(conn)?;

    Ok(DeleteResult {})
}

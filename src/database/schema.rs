use serde::{Deserialize, Serialize};
use surrealdb::sql::Thing;

#[derive(Debug, Serialize)]
pub struct Item {
    pub name: String,
}

#[derive(Debug, Serialize)]
pub struct ItemSet {
    pub items: Vec<Item>,
}

#[derive(Debug, Serialize)]
pub struct User {
    pub name: String,
    pub email: String,
    pub pw_hash: String,
}

#[derive(Debug, Serialize)]
pub struct Group {
    pub users: Vec<User>,
}

#[derive(Debug, Serialize)]
pub struct Basket {
    pub items: ItemSet,
    pub owner: User,
    pub contributors: Group,
}

#[derive(Debug, Deserialize)]
pub struct Record {
    #[allow(dead_code)]
    pub id: Thing,
}

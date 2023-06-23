use serde::{Deserialize, Serialize};
use surrealdb::sql::Thing;


#[derive(Debug, Serialize, Deserialize)]
pub struct ListItem {
    pub name: String,
    pub quantity: usize,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ItemSet {
    pub items: Vec<ListItem>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub name: String,
    pub email: String,
    pub pw_hash: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Group {
    pub users: Vec<User>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Basket {
    pub name: String,
    pub items: ItemSet,
    pub owner: User,
    pub contributors: Group,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Record {
    #[allow(dead_code)]
    pub id: Thing,
}

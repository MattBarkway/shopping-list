use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct CreateShoppingList {
    pub name: String,
    pub user: String,
}

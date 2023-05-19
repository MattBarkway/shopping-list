use crate::config;
use crate::database::schema;
use actix_web::{get, put, post, web, Responder};
use crate::config::DB;
use crate::database::schema::{Basket, Group, ItemSet, Record, User};
use crate::endpoints::payloads;

#[get("/shopping/{id}")]
pub async fn get_shopping_list(
    id: web::Path<usize>,
    data: web::Data<config::Config>,
) -> impl Responder {
    let app_name = &data.app_name;
    format!("Hello from {app_name}! Here is shopping list {id}!")
}

#[put("/shopping/{id}")]
pub async fn add_shopping_list_item(
    id: web::Path<usize>,
    item: web::Json<schema::ListItem>,
) -> impl Responder {
    format!(
        "You have added {} of item: {} to list: {id}!",
        item.quantity, item.name
    )
}

#[post("/shopping/{id}")]
pub async fn create_shopping_list(
    id: web::Path<usize>,
    to_create: web::Json<payloads::CreateShoppingList>,
)  -> impl Responder {
    let created: Record = DB
        .create("shopping-list")
        .content(Basket {
            items: ItemSet { items: vec![] },
            owner: User {
                name: "".to_string(),
                email: "".to_string(),
                pw_hash: "".to_string(),
            },
            contributors: Group { users: vec![] },
        })
    .await?;
}

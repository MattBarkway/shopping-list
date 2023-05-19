use actix_web::{get, put, web, Responder};
use serde::Deserialize;


#[get("/shopping/{id}")]
pub async fn get_shopping_list(id: web::Path<usize>) -> impl Responder {
    format!("Here is shopping list {id}!")
}


#[derive(Deserialize)]
pub struct ShoppingItem {
    name: String,
    quantity: usize,
}

#[put("/shopping/{id}")]
pub async fn add_shopping_list_item(id: web::Path<usize>, item: web::Json<ShoppingItem>) -> impl Responder {
    format!("You have added {} of item: {} to list: {id}!", item.quantity, item.name)
}

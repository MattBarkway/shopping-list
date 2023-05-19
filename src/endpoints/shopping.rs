use actix_web::{get, put, web, Responder};
use serde::Deserialize;

struct AppState {
    app_name: String,
}


#[get("/shopping/{id}")]
async fn get_shopping_list(id: web::Path<usize>, data: web::Data<AppState>) -> impl Responder {
    let app_name = &data.app_name; // <- get app_name
    format!("Hello {app_name}! Here is shopping list {id}!") // <- response with app_name

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

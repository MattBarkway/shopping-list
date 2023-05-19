use actix_web::{get, put, Responder, web};
use crate::config;
use crate::database::schema;


#[get("/shopping/{id}")]
pub async fn get_shopping_list(id: web::Path<usize>, data: web::Data<config::Config>) -> impl Responder {
    let app_name = &data.app_name;
    format!("Hello from {app_name}! Here is shopping list {id}!")
}

#[put("/shopping/{id}")]
pub async fn add_shopping_list_item(id: web::Path<usize>, item: web::Json<schema::ListItem>) -> impl Responder {
    format!("You have added {} of item: {} to list: {id}!", item.quantity, item.name)
}

use actix_web::{get, web, Responder};


#[get("/shopping/{id}")]
pub async fn get_shopping_list(id: web::Path<usize>) -> impl Responder {
    format!("Here is shopping list {id}!")
}
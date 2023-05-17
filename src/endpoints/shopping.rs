use actix_web::{get, web, Responder};

struct AppState {
    app_name: String,
}


#[get("/shopping/{id}")]
async fn get_shopping_list(id: web::Path<usize>, data: web::Data<AppState>) -> impl Responder {
    let app_name = &data.app_name; // <- get app_name
    format!("Hello {app_name}! Here is shopping list {id}!") // <- response with app_name

}

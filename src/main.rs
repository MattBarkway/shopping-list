use actix_web::{App, HttpServer};
use tokio;
mod endpoints;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new().service(endpoints::shopping::get_shopping_list)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
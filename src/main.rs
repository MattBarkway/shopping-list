mod database;
mod endpoints;

use crate::database::interface::{ConnectionManager, ShoppingListManager};
use crate::database::surreal::{AsyncConnector, SurrealConnector};
use actix_web::{App, HttpServer};
use std::error::Error;
use tokio;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // HttpServer::new(|| {
    //     App::new().service(endpoints::shopping::get_shopping_list)
    // })
    // .bind(("127.0.0.1", 8080))?
    // .run()
    // .await
    let connector = SurrealConnector::new(
        "shopping",
        "shopping-list",
        "***",
        "***",
        "http://127.0.0.1:8000",
    );

    let mut manager = ShoppingListManager::new(Box::new(connector));

    manager.begin().await?;

    Ok(())
}

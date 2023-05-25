mod config;
mod database;
mod endpoints;

use crate::database::interface::{ConnectionManager, ShoppingListManager};
use crate::database::surreal::SurrealConnector;
use surrealdb::engine::remote::ws::Ws;

use crate::config::{Config, DB};
use actix_web::{App, HttpServer};
use std::error::Error;
use tokio;

fn load_config() -> Config {
    Config {
        app_name: "".to_string(),
        env: "".to_string(),
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let config = load_config();
    DB.connect::<Ws>("cloud.surrealdb.com").await?;
    DB.use_ns("shopping").use_db(config.env).await?;

    HttpServer::new(|| App::new().service(endpoints::shopping::get_shopping_list))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await?;
    let connector = SurrealConnector::new(
        "shopping-list",
        "shopping-list",
        "***",
        "***",
        "http://127.0.0.1:8000",
    );

    let mut manager = ShoppingListManager::new(Box::new(connector));

    manager.begin().await?;

    Ok(())
}

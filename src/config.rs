use surrealdb::engine::remote::ws::Client;
use surrealdb::Surreal;

pub struct Config {
    pub app_name: String,
    pub env: String,
}

pub static DB: Surreal<Client> = Surreal::init();

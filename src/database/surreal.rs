use async_trait::async_trait;
use std::error::Error;
use surrealdb::engine::any::Any;
use surrealdb::engine::remote::ws::{Client, Ws};
use surrealdb::opt::auth::Root;
use surrealdb::Surreal;

#[async_trait]
pub trait AsyncConnector {
    async fn connect(&mut self) -> Result<(), Box<dyn Error>> {
        Ok(())
    }
}

pub struct SurrealConnector {
    connection: Option<Surreal<Client>>,
    namespace: String,
    database: String,
    username: String,
    password: String,
    address: String,
}

impl SurrealConnector {
    pub fn new(
        namespace: &str,
        database: &str,
        username: &str,
        password: &str,
        address: &str,
    ) -> Self {
        SurrealConnector {
            connection: None,
            namespace: namespace.to_string(),
            database: database.to_string(),
            username: username.to_string(),
            password: password.to_string(),
            address: address.to_string(),
        }
    }
}

#[async_trait]
impl AsyncConnector for SurrealConnector {
    async fn connect(&mut self) -> Result<(), Box<dyn Error>> {
        let db = Surreal::new::<Ws>(self.address.clone()).await?;

        db.signin(Root {
            username: &self.username,
            password: &self.password,
        })
        .await?;

        db.use_ns("shopping").use_db("shopping-list").await?;

        self.connection = Some(db);

        Ok(())
    }
}

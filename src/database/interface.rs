use crate::database::surreal::AsyncConnector;
use async_trait::async_trait;
use std::error::Error;

#[async_trait]
pub trait ConnectionManager {
    async fn begin(&mut self) -> Result<(), Box<dyn Error>> {
        Ok(())
    }
}

pub struct ShoppingListManager {
    connector: Box<dyn AsyncConnector + Send>,
}

impl ShoppingListManager {
    pub fn new(connector: Box<dyn AsyncConnector + Send>) -> Self {
        ShoppingListManager { connector }
    }

    pub async fn create_shopping_list(_owner: usize) {}

    pub async fn delete_shopping_list(_owner: usize) {}

    pub async fn create_user(_name: &str, _email: &str, _pw_hash: &str) {}
    pub async fn delete_user(_name: &str, _email: &str, _pw_hash: &str) {}

    pub async fn create_group(_basket: usize) {}
    pub async fn delete_group(_basket: usize) {}

    pub async fn add_list_item(_basket: usize) {}
    pub async fn remove_list_item(_basket: usize) {}
    pub async fn update_list_item(_basket: usize) {}

    pub async fn add_group_user(_group: usize, _user: usize) {}
    pub async fn remove_group_user(_group: usize, _user: usize) {}
}

#[async_trait]
impl ConnectionManager for ShoppingListManager {
    async fn begin(&mut self) -> Result<(), Box<dyn Error>> {
        self.connector.connect().await?;
        Ok(())
    }
}

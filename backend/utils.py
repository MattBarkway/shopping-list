def assemble_mysql_connection(
    dialect: str,
    driver: str,
    username: str,
    password: str,
    address: str,
    port: int,
    database: str,
) -> str:
    """
    Create mysql shopping-list connection path.

    Args:
        dialect: SQL dialect.
        driver: SQL driver.
        username: Username for the shopping-list.
        password: Password for the shopping-list.
        address: Database address.
        port: Port number for shopping-list.
        database: Database name.

    Returns:
        Database connection path.
    """
    return f"{dialect}+{driver}://{username}:{password}@{address}:{port}/{database}"

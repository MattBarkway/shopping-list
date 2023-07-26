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
    Create mysql database connection path.

    Args:
        dialect: SQL dialect.
        driver: SQL driver.
        username: Username for the database.
        password: Password for the database.
        address: Database address.
        port: Port number for database.
        database: Database name.

    Returns:
        Database connection path.
    """
    return f"{dialect}+{driver}://{username}:{password}@{address}:{port}/{database}"

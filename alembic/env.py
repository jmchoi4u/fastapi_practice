# alembic/env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# NEW: import SQLModel metadata from our app
from sqlmodel import SQLModel
from app.database import DATABASE_URL, engine  # or wherever you store the URL/engine
from app.models import *  # or import Post, User, etc. 
# We need to ensure that all models are imported so that
# SQLModel.metadata has them.

# this is the Alembic Config object
config = context.config

# set the sqlalchemy.url (if not set in alembic.ini)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata  # This is key!

def run_migrations_offline():
    """
    For 'offline' migrations: read from the config and create DB scripts
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    For 'online' migrations: create engine and run.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

def run_migrations():
    """
    Decide offline/online based on config
    """
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()

# Then at the bottom:
run_migrations()
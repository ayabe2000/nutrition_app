"""
Alembic migration environment configuration.

This module provides configuration for Alembic migrations.
"""
import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context as alembic_context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = alembic_context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    """
    データベースエンジンを取得する関数
    Returns:
    Engine: データベースエンジンのインスタンス
    """
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """
    データベースエンジンのURLを取得する関数

    Returns:
        str: データベースエンジンのURL
    """
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    """
    データベースメタデータを取得する関数

    Returns:
        sqlalchemy.MetaData: データベースメタデータのインスタンス
    """
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    alembic_context.config(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with alembic_context.config.begin_transaction():
        alembic_context.config.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        alembic_context.config.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with alembic_context.config.begin_transaction():
            alembic_context.config.run_migrations()


if alembic_context.config.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

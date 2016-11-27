from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
from zope.sqlalchemy import register

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .Project import Project,Comment# noqa
from .User import User# noqa
from .Equipment import Equipment# noqa
from .Obligation import Obligation# noqa
from .Member import Member_table# noqa
from  .Proposal import (Proposal,
                        Objective,
                        Cost,
                        Previouse_result,
                        Owner_for_proposal,
                        Member_for_proposal,
                        Delicate_budget,
                        Schedule,
                        )# noqa
from .Summary import Summary

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()

def get_session(maker,transaction_manager):
    register(maker,transaction_manager=transaction_manager)
    session = maker()
    return session

def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('ProjectExcercise.models')``.

    """
    settings = config.get_settings()

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    engine = engine_from_config(settings,prefix='sqlalchemy.')
    maker = sessionmaker()
    register(maker)
    maker.configure(bind = engine)

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        lambda r: get_session(maker,r.tm),
        'db_session',
        reify=True
    )
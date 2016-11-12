import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from ..models.meta import Base
from ..models import (
    get_session
    )
from ..models import (Project,
                      User,
                      Equipment,
                      Obligation,
                      Member_table,
                      Member,
                      )

import datetime

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings,prefix='sqlalchemy.')
    Base.metadata.create_all(engine)

    maker = sessionmaker()
    maker.configure(bind=engine)

    with transaction.manager:
        session = get_session(maker, transaction.manager)

        dummy_User = User(First_name = 'GOD', Last_name = 'DAMN', role ='GOD',student_id = 00000,Email = 'GOD@FIBO.com',user_id = 'GODdamn',year=0)
        dummy_User.hash_password('dummy')

        dummy_project = Project(title = 'GOD PROJECT',description ='It a god very duty no such a normal human will understand.',status ='Neary done',type ='GOD duty',start_date=datetime.date(datetime.MINYEAR,1,1),finish_date = datetime.date(datetime.MAXYEAR,12,31))
        dummy_project.leader = dummy_User
        dummy_project.advisor=dummy_User
        dummy_project.project_member.append(dummy_User)

        dummy_equipment = Equipment(name = 'Legendary item',cost = 1000000000000000, buy_date = datetime.date(datetime.MINYEAR,1,1), contract = 'Only God will know', status='Wait for TRUE HERO to be found',)
        dummy_equipment.asso_to = dummy_project
        dummy_equipment.owner = dummy_User

        dummy_obligation = Obligation(type = 'Duty from GOD', description = 'wait for the TRUE HERO', duty = 'Find Legendary item', status='Not found yet')
        dummy_obligation.asso_to = dummy_project
        dummy_obligation.equipment = dummy_equipment

        session.add(dummy_project)
        session.add(dummy_User)
        session.add(dummy_equipment)
        session.add(dummy_obligation)

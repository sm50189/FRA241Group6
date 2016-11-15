import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from sqlalchemy import (engine_from_config,
                        Column,
                        String,
                        Index,
                        Integer,
                        Text,
                        VARCHAR,
                        Date,
                        ForeignKey,)
from sqlalchemy.orm import sessionmaker

from ..models.meta import Base
from ..models import (
    get_session
    )
from ..models import (Proposal,
                        Objective,
                        Cost,
                        Previouse_result,
                        Owner_for_proposal,
                        Member_for_proposal,
                        Delicate_budget,
                        Schedule,
                        )# noqa




def add_column(engine, table_name, column,name):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, name, column_type))
    print 'added'

def checkArgv(option):
    try:
        # print globals()
        if "table" not in option or "column" not in option:
            print "wrong parse"
            sys.exit(1)
        if option["table"] not in globals():
            print 'no table name '+option["table"]
            sys.exit(1)
        a = globals()[option["table"]]
        if hasattr(a,option["column"]) == False:
            print 'no attrbute'+option["column"]
            sys.exit(1)
    except TypeError:
        print 'something wrong'
        sys.exit(1)

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
    checkArgv(options)
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings,prefix='sqlalchemy.')
    column = getattr(globals()[options["table"]],options["column"])
    add_column(engine, options["table"], column,options["column"])

    sys.exit(0)
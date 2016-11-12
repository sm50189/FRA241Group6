#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import transaction
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import RGBColor

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

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


def Get_data(session, project_id):
    return session.query(Project).filter_by(id=project_id).one()


def Gen_Doc(doc_name='Doc.docx'
            , project_name_th=''
            , project_name_en=''
            , date_cap=u''
            , where=''
            , rational=''):
    document = Document('FRA241PROJECT/static/Archetype_gendoc.docx')

    ######################################################################
    '''Create Style'''
    ######################################################################

    obj_styles = document.styles

    obj_charstyle = obj_styles.add_style('header', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(16)
    obj_font.name = 'TH Sarabun New'
    obj_font.bold = True
    obj_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    obj_charstyle = obj_styles.add_style('content', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(16)
    obj_font.name = 'TH Sarabun New'
    obj_font.bold = False
    obj_font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    ######################################################################

    document.add_picture('FRA241PROJECT/static/kmutt.png', width=Inches(0.99), height=Inches(0.99))
    logo = document.paragraphs[-1]
    logo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    proj_name = document.add_heading('', 0)
    proj_name.add_run(u'ข้อเสนอโครงการเข้าร่วม\n', style='header')
    proj_name.add_run(project_name_th + '\n', style='header') if len(project_name_th) != 0 else 0
    proj_name.add_run(project_name_en + '\n', style='header') if len(project_name_en) != 0 else 0
    proj_name.add_run(u'สถาบันวิทยาการหุ่นยนต์ภาคสนาม (ฟีโบ้) มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี\n', style='header')
    proj_name.add_run(u'ระหว่างวันที่ ' + date_cap + '\n', style='header')
    proj_name.add_run(u'ณ ' + where, style='header')
    proj_name.alignment = WD_ALIGN_PARAGRAPH.CENTER

    rationale_head = document.add_paragraph('\n')
    rationale_head.add_run(u'หลักการและเหตุผล', style='header')

    rationale = document.add_paragraph('\t')
    rationale.add_run(rational + '\n', style='content')
    rationale.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY

    purpose_head = document.add_paragraph()
    purpose_head.add_run(u'วัตถุประสงค์', style='header').alignment = WD_ALIGN_PARAGRAPH.LEFT

    purpose = document.add_paragraph()
    purpose.add_run(style='content')

    document.add_page_break()
    document.save(doc_name)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, prefix='sqlalchemy.')
    Base.metadata.create_all(engine)

    maker = sessionmaker()
    maker.configure(bind=engine)

    session = get_session(maker, transaction.manager)

    all_data = Get_data(session=session, project_id=4)
    Gen_Doc(doc_name='FRA241PROJECT/static/Gened_DOC/'+str(all_data.id)+'.docx',
            project_name_th=all_data.title,
            date_cap=u'17 มกราคม – 21 มีนาคม 2559',
            where=all_data.proposal[0].activity_location,
            rational=all_data.proposal[0].Reason)

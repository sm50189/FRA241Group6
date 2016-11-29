# from .models.Project import Project
# from .models.User import User
# from  .models.Proposal import (Proposal,
#                                 )
# from sqlalchemy.orm.exc import NoResultFound
# from pyramid.httpexceptions import (
#     HTTPNotFound,
#     HTTPFound,
# )
# from pyramid.security import (
#     Allow,
#     Everyone,
# )
from views.view_factory import *
# import datetime
# import transaction
# import time

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('profile','/profile')
    config.add_route('enroll_project','/profile/{project_id}')
    config.add_route('bar', '/bar')
    config.add_route('test','/test')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.add_route('plusButton','/plusButton')
    config.add_route('recommend','/recommend/{project_id}')
    config.add_route('download','/download/{project_id}')
    config.add_route('checkStatus','/checkStatus/{project_id}',factory = check_status_factory)
    config.add_route('addProject','/add_project')
    config.add_route('select_project_edit','/select_project')
    config.add_route('proposal','/add_proposal/{project_id}/{type_project}',factory=proposal_factory)
    config.add_route('teacherProject','/teacherProject',factory = teacher_project_factory)
    config.add_route('adminProject','/adminProject',factory=admin_project_factory)
    config.add_route('inspectProject','/teacherProject/{project_id}',factory = inspect_foctory)
    config.add_route('select_project_summarize','/summarize')
    config.add_route('summarize','/summarize/{project_id}',factory = summarize_factory)
    config.add_route('select_cost', '/projectCost')
    config.add_route('cost', '/projectCost/{project_id}', factory=cost_factory)
    # config.add_route('myProject','/myProject')


from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models.User import User
from ..models.Project import Project
from  ..models.Summary import Summary


@view_config(route_name = 'select_project_summarize',renderer = '../templates/summary.pt')
def select_projct(request):
    if request.user.role == "Admin":
        project_list = request.db_session.query(Project)
    else:
        project_list = request.user.own_project+request.user.advisee_project
    return dict(project_list = project_list)

@view_config(route_name = 'summarize', renderer = '../templates/summary.pt')
def summary_project(request):
    if request.user.role == "Admin":
        project_list = request.db_session.query(Project)
    else:
        project_list = request.user.own_project+request.user.advisee_project
    project = request.context.project
    summary = project.summary
    count_owner = 1
    project_owner= ''
    while True:
        print "\n\nfucking loop\n\n"
        name_inParam = "SF1_" + str(count_owner)
        if name_inParam in request.params:
            project_owner += request.params[name_inParam] + unichr(171)
        else:
            break
        count_owner += 1
    count_member = 1
    project_member = ''
    while True:
        name_inParam = "SF2"+str(count_member)
        print name_inParam
        if name_inParam in request.params:
            project_member += request.params[name_inParam]+unichr(171)
        else:
            break
        count_member+=1
    reason = request.params.get("SF3","")
    count_obj = 1
    project_obj = ''
    while True:
        name_inParam = "SF4"+str(count_obj)
        print name_inParam
        if name_inParam in request.params:
            project_obj += request.params[name_inParam]+unichr(171)
        else:
            break
        print name_inParam
        count_obj+=1
    count_target = 1
    project_target = ''
    while True:
        name_tar1_inParam = "SF51_" + str(count_target)
        name_tar2_inParam = "SF52_" + str(count_target)
        name_tar3_inParam = "SF53_" + str(count_target)
        if name_tar1_inParam in request.params and name_tar2_inParam in request.params and name_tar3_inParam in request.params:
            project_target += request.params[name_tar1_inParam] + unichr(172) + request.params[
                name_tar2_inParam] + unichr(172) + request.params[name_tar3_inParam] + unichr(171)
        else:
            break
        print name_tar1_inParam
        count_target += 1
    count_bene = 1
    project_bene = ''
    while True:
        name_inParam = "SF6" + str(count_bene)
        if name_inParam in request.params:
            project_bene += request.params[name_inParam] + unichr(171)
        else:
            break
        print name_inParam
        count_bene += 1
    count_DB = 1
    project_DB = ''
    while True:
        name_DB1_inParam = "SF71_" + str(count_DB)
        name_DB2_inParam = "SF72_" + str(count_DB)
        name_DB3_inParam = "SF73_" + str(count_DB)
        if name_DB1_inParam in request.params and name_DB2_inParam in request.params and name_DB3_inParam in request.params:
            project_DB += request.params[name_DB1_inParam] + unichr(172) + request.params[
                name_DB2_inParam] + unichr(172) + request.params[name_DB3_inParam] + unichr(171)
        else:
            break
        print name_DB1_inParam
        count_DB += 1
    project_location = request.params.get("SF8","")
    project_problem = request.params.get("SF9","")
    project_suggest = request.params.get("SF10","")
    project_criteria = request.params.get("SF11","")

    if "save" in request.params:
        summary.owner_for_proposal = project_owner
        summary.member_for_proposal = project_member
        summary.Reason = reason
        summary.objective = project_obj
        summary.target_group = project_target
        summary.profit = project_bene
        summary.delicate_budget = project_DB
        summary.location = project_location
        summary.problem = project_problem
        summary.suggest = project_suggest
        summary.criteria = project_criteria
    return dict(project = project,
                summary = summary,
                project_list = project_list,
                )
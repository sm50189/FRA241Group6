from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models.User import User
from ..models.Project import (Project,
                             Comment,)
import transaction

@view_config(route_name = "teacherProject", renderer = "../templates/pageTeacher1.pt",permission = "access")
def teacherProject(request):
    project_list = request.context.project_list
    uncheck_project = []
    checked_project = []
    for i in project_list:
        if i.status.split(unichr(171))[0] == "F":
            uncheck_project.append(i)
        elif i.status.split(unichr(171))[0] == "T":
            checked_project.append(i)
    return dict(uncheck_project = uncheck_project,
                checked_project = checked_project,
                user = request.user,
                )

@view_config(route_name = "adminProject", renderer = "../templates/Adminpage1.pt",permission = "access")
def adminProject(request):
    project_list = request.context.project_list
    uncheck_project = []
    checked_project = []
    for i in project_list:
        status = i.status.split(unichr(171))
        print "\n\n\n\n\n\n\n\n\n\n",status,"\n\n\n\n\n\n\n\n\n\n"
        if status[1] == "F":
            uncheck_project.append(i)
        elif status[1] == "T":
            checked_project.append(i)
    if "x" in request.params:
        id_recommend_list = []
        for i in checked_project:
            if str(i.id) in request.params:
                id_recommend_list.append(str(i.id))
        print "\n\n\n\n\n\n\n\n\nid recommend",id_recommend_list,"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        for i in id_recommend_list:
            with transaction.manager:
                pass
        return HTTPFound(location=request.route_url('home'))
    return dict(uncheck_project = uncheck_project,
                checked_project = checked_project,
                user = request.user,
                )

@view_config(route_name = "inspectProject" , renderer = "../templates/pageTeacher2.pt",permission = "access")
def inspectProject(request):
    project = request.context.project
    comment = request.context.comment
    commentID = comment.id
    if "save" in request.params or "send-comment" in request.params:
        comment.text = request.params.get("message","")
    print "\n\n\n\n\n\n\n\n\n\n","send-comment" in request.params,"\n\n\n\n\n\n\n\n"
    if "send-comment" in request.params:
        status = [i for i in project.status.split(unichr(171))]
        if request.user.role == "Admin":
            status[1] = 'T'
        else:
            status[0] = 'T'
        project.status = unichr(171).join(status)
        print "\n\n\n\n\n\n\n\n\n\nfuck yeah\n\n\n\n\n\n\n\n"
        if request.user.role == "Teacher":
            return HTTPFound(location=request.route_url("teacherProject"))
        else:
            return HTTPFound(location=request.route_url("adminProject"))
    comment = request.db_session.query(Comment).filter_by(id = commentID).first()
    return dict(project = project,
                comment = comment,
                )


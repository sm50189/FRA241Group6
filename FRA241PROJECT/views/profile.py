from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from ..models import User,Project
import transaction

@view_config(route_name = "profile",renderer = '../templates/Profile.pt')
def profile(request):
    project_list = request.user.enroll_project
    userID = request.user.id
    if "save_profile" in request.params:
        with transaction.manager:
            user = request.db_session.query(User).filter_by(id = userID).first()
            user.student_id = request.params.get("id","")
            user.First_name = request.params.get("firstname","")
            print "\n\n\n\n\n\n\n",request.params.get("firstname",""),"\n\n\n\n\n\n\n\n"
            user.Last_name = request.params.get("lastname","")
            user.year = request.params.get("year","")
            user.Email = request.params.get("mail","")
        return HTTPFound(location=request.route_url('profile'))
    return dict(project_list = project_list,
                )

@view_config(route_name = "enroll_project",renderer = '../templates/InterestProject.pt')
def enroll_project(request):
    projectID = request.matchdict["project_id"]
    project = request.db_session.query(Project).filter_by(id = projectID).first()
    return dict(project = project,
                alert = "",
                )
from pyramid.security import (
    Allow,
    Everyone,
)
from ..models.Project import Project,Comment
from ..models.User import User
from ..models.Summary import Summary
from  ..models.Proposal import (Proposal,
                                )
from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
import datetime
import transaction
import time
import copy

def proposal_factory(request):
    try:
        project = request.db_session.query(Project).filter_by(id = request.matchdict["project_id"]).one()
    except NoResultFound:
        return HTTPFound(location=request.route_url("addProject"))
    projectId = project.id
    if project.proposal is None:
        with transaction.manager:
            proposal = Proposal( Reason = '',
                                objective='',
                                owner_for_proposal = '',
                                member_for_proposal = '',
                                advisor_for_proposal = '',
                                evaluation_index = '',
                                profit = '',
                                type_of_activity = '',
                                cost = '',
                                delicate_budget = '',
                                schedule = '',
                                previouse_result = '',
                                activity_comparition = '',
                                )
            proposal.parent_id = projectId
            request.db_session.add(proposal)
    project.proposal = request.db_session.query(Proposal).filter_by(parent_id = projectId).first()
    return AddProposal(project)
class AddProposal(object):
    def __init__(self,project):
        self.project = project
        print "\n\n\n\n\n\n\nin class",self.project.owner_id,"\n\n\n\n\n\n\n\n"

    def __acl__(self):
        a = [
            (Allow,Everyone,'nor_access'),
            (Allow,'role:Student','not_access'),
            (Allow,'role:Teach','not_access'),
            (Allow,'role:GOD','not_access'),
            (Allow,str(self.project.owner_id),'edit'),
        ]
        print "\n\n\n\n\n\n\n\nacl",a,"\n\n\n\n\n\n\n"
        return a

def teacher_project_factory(request):
    id = request.user.id
    with transaction.manager:
        with request.db_session.query(User).filter_by(id = id).first() as user:
            project_list = user.advisee_project
            for i in project_list:
                if i.status is None or len(i.status.split(unichr(171))) < 3:
                    i.status = 'F'+unichr(171)+'F'+unichr(171)+'F'+unichr(171)+'F'+unichr(171)
    projectList = request.db_session.query(User).filter_by(id = id).first().advisee_project

    return TeacherProject(projectList,id)
class TeacherProject(object):
    def __init__(self,project_list,id):
        self.project_list = project_list
        self.id = id

    def __acl__(self):
        return [
            (Allow,Everyone,'deny'),
            (Allow,'role:Teacher','access'),
            (Allow,'role:GOD','access'),
        ]

def admin_project_factory(request):
    with transaction.manager:
        project_list = request.db_session.query(Project)
        for i in project_list:
            if i.status is None or len(i.status.split(unichr(171))) <3:
                i.status = 'F' + unichr(171) + 'F' + unichr(171) + 'F' + unichr(171) + 'F' + unichr(171)
    project_list = request.db_session.query(Project)
    return AdminProject(project_list)
class AdminProject(object):
    def __init__(self,project_list):
        self.project_list = project_list

    def __acl__(self):
        return [(Allow,'role:Admin',"access"),
                ]


def inspect_foctory(request):
    project_id = request.matchdict['project_id']
    project = request.db_session.query(Project).filter_by(id = project_id).first()
    projectID = project.id
    userID = request.user.id
    comment = request.db_session.query(Comment).filter_by(parent_id = projectID).filter_by(writer_id = userID).first()
    if comment is None:
        with transaction.manager:
            cmt = Comment(parent_id = projectID,
                              writer_id=userID,
                              )
            request.db_session.add(cmt)
        comment = request.db_session.query(Comment).filter_by(parent_id = projectID).filter_by(writer_id = userID).first()
    return inspectProject(project,comment)
class inspectProject(object):
    def __init__(self,project,comment):
        self.project = project
        self.comment = comment
        self.advisor_list = self.project.advisor

    def __acl__(self):
        a = [
            (Allow,Everyone,"deny"),
            (Allow,'role:GOD',"access"),
            (Allow,'role:Admin',"access")
        ]
        for i in self.advisor_list:
            a.append((Allow,str(i.id),"access"))
        return a

def summarize_factory(request):
    try:
        project = request.db_session.query(Project).filter_by(id=request.matchdict["project_id"]).one()
    except NoResultFound:
        return HTTPFound(location=request.route_url("addProject"))
    proposal = project.proposal
    projectID = project.id
    if project.summary is None:
        with transaction.manager:
            summary = Summary()
            summary.parent_id = projectID
            summary.owner_for_proposal = proposal.owner_for_proposal
            summary.member_for_proposal = proposal.member_for_proposal
            summary.delicate_budget = proposal.delicate_budget
            summary.profit = proposal.profit
            summary.Reason = proposal.Reason
            summary.objective = proposal.objective
            summary.target_group = ''
            summary.location = ''
            summary.problem = ''
            summary.suggest = ''
            summary.criteria = ''
            request.db_session.add(summary)
    project = request.db_session.query(Project).filter_by(id=request.matchdict["project_id"]).one()
    return summarizeProject(project)
class summarizeProject(object):
    def __init__(self,project):
        self.project = project

    def __acl__(self):
        return [(Allow,Everyone,"deny"),
                (Allow,str(self.project.owner_id),"access"),
                ]

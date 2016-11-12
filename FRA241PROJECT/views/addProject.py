from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
    view_defaults,
)

from ..models.Project import Project
from ..models.User import User
from  ..models.Proposal import (Proposal,
                                Objective,
                                Cost,
                                Previouse_result,
                                Owner_for_proposal,
                                Member_for_proposal,
                                Delicate_budget,
                                Schedule,
                                )
import datetime
import transaction

@view_defaults(route_name='proposal')
class Project_view():

    def __init__(self,request):
        self.request = request

    @view_config(route_name = 'addProject',renderer = "../templates/index.pt")
    def add_project(self):
        # user = self.request.user
        thisUser = self.request.user.id
        if self.request.params.get("project_title",'') == '':
            return dict(alert='No project title',current_title = '',flag= False)
        elif "volunteer-button" in self.request.params:
            print "\n\n\n\n\n\n\n\nvolun\n\n\n\n\n\n\n\n\n\n"
            return dict(flag = 'volunteer',current_title = self.request.params["project_title"],alert = False)
        elif "competitive-button" in self.request.params:
            print "\n\n\n\n\n\n\n\ncompet\n\n\n\n\n\n\n\n\n\n"
            return dict(flag = 'competitive',current_title = self.request.params["project_title"],alert = False)
        elif "camp-button" in self.request.params:
            print "\n\n\n\n\n\n\n\ncamp\n\n\n\n\n\n\n\n\n\n"
            return dict(flag = 'camp',current_title = self.request.params["project_title"],alert = False)

        if "volunteer" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title=self.request.params["project_title"], type="volunteer")
                project.owner_id = thisUser
                session.add(project)
            print "\n\n\n\n\n\nadd complete\n\n\n\n"
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id)
            return HTTPFound(location = self.request.route_url('proposal',project_id = project.id,type_project=project.type),headers=headers )
        elif "competitive" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title = self.request.params["project_title"],type = "competitive")
                thisUser = self.request.user.id
                project.owner_id = thisUser
                session.add(project)
            print "\n\n\n\n\n\nadd complete\n\n\n\n"
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id)
            return HTTPFound(location=self.request.route_url('proposal',project_id = project.id,type_project=project.type), headers=headers )
        elif "camp" in self.request.params:
            with transaction.manager:
                session = self.request.db_session
                project = Project(title = self.request.params["project_title"],type = "camp")
                thisUser = self.request.user.id
                project.owner_id = thisUser
                session.add(project)
            print "\n\n\n\n\n\nadd complete\n\n\n\n"
            user = self.request.user
            project_list = self.request.db_session.query(Project).filter_by(title=self.request.params["project_title"]).filter_by(owner_id=user.id).order_by(Project.id)
            project = project_list[-1]
            headers = remember(self.request, user.id)
            return HTTPFound(location=self.request.route_url('proposal',project_id = project.id,type_project=project.type),headers=headers )

        return dict( current_title='',flag = False,alert = False)

    @view_config(route_name = 'proposal',match_param="type_project=camp",renderer = "../templates/formCamp.pt")
    def form_champ(self):
        try:
            with self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).one() as proposal:
                project_year=proposal.year
                project_activity_location=proposal.activity_location
                project_reason= proposal.Reason
                project_Calibration = proposal.activity_comparition
                project_duration=proposal.durtion
                project_evaluation = proposal.evaluation_index
                project_profit=proposal.profit
                list_OJ = [ i.text for i in proposal.objective]
                count_OJ = len(list_OJ)
                list_PR = [i.text for i in proposal.owner_for_proposal]
                count_P_R = len(list_PR)
                list_PM = [i.text for i in proposal.member_for_proposal]
                count_P_M = len(list_PM)
                list_BGT = [i.text for i in proposal.cost]
                count_BGT = len(list_BGT)
                list_DB = [[i.order,i.descrip,i.value] for i in proposal.delicate_budget]
                count_DB = len(list_DB)
                list_schedule = [[i.time,i.descrip] for i in proposal.schedule]
                count_schedule = len(list_schedule)
        except NoResultFound:
            is_exist = False
            project_year = ''
            project_activity_location = ''
            project_reason = ''
            project_Calibration = ''
            project_duration = ''
            project_evaluation = ''
            project_profit = ''
            list_OJ = []
            count_OJ = len(list_OJ)
            list_PR = []
            count_P_R = len(list_PR)
            list_PM = []
            count_P_M = len(list_PM)
            list_BGT = []
            count_BGT = len(list_BGT)
            list_DB = []
            count_DB = len(list_DB)
            list_schedule = []
            count_schedule = len(list_schedule)

        try:
            with self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first() as project:
                # start_date = str(project.start_date.day) + "/" + str(project.start_date.month) + "/" + str(project.start_date.year)
                # finish_date = str(project.finish_date.day) + "/" + str(project.finish_date.month) + "/" + str(project.finish_date.year)
                project_title = project.title
                if project.start_date is not None:
                    start_date = str(project.start_date.day)+"/"+str(project.start_date.month)+"/"+str(project.start_date.year)
                elif project.start_date is None:
                    start_date = ''
                if project.finish_date is not None:
                    finish_date = str(project.finish_date.day)+"/"+str(project.finish_date.month)+"/"+str(project.finish_date.year)
                else:
                    finish_date = ''
        except NoResultFound:
            print "\n\n\n\n\n\n\nwhy the fuck there is no result\n\n\n\n\n\n\n"
            return HTTPFound(location=self.request.route_url("addProject"))

        if "P_N" in self.request.params:
            project_title = self.request.params["P_N"]

        if "Year" in self.request.params:
            project_year = self.request.params["Year"]

        if "Date-start" in self.request.params:
            raw_date_start = self.request.params["Date-start"]
            if "/" not in raw_date_start:
                raw_date_start = 'Invalid format'
            split_date = raw_date_start.split("/")
            if len(split_date) != 3:
                raw_date_start = 'Invalid format'
            for i in split_date:
                if i.isdigit() == False:
                    raw_date_start = 'Invalid format'
                    break

            if raw_date_start != 'Invalid format':
                start_date = datetime.date(int(split_date[2]),int(split_date[1]),int(split_date[0]))

            else:
                start_date = ''

        if "Date-finish" in self.request.params:
            raw_date_finish = self.request.params["Date-finish"]
            if "/" not in raw_date_finish:
                raw_date_finish = 'Invalid format'
            split_finish_date = raw_date_finish.split("/")
            if len(split_finish_date) != 3:
                raw_date_finish = 'Invalid format'
            for i in split_finish_date:
                if i.isdigit() == False:
                    raw_date_finish = 'Invalid format'
                    break

            if raw_date_finish != 'Invalid format':
                finish_date = datetime.date(int(split_finish_date[2]), int(split_finish_date[1]), int(split_finish_date[0]))

            else:
                finish_date = ''

        if "P_P" in self.request.params:
            project_activity_location = self.request.params["P_P"]

        if "Reason_Project" in self.request.params:
            project_reason = self.request.params["Reason_Project"]

        count_OJ = 1
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "OJ"+str(count_OJ)
            if name_inParam in self.request.params:
                if self.request.params[name_inParam] in list_OJ:
                    pass
                else:
                    list_OJ.append(self.request.params[name_inParam])
            else:
                break
            count_OJ+=1

        if "Calibration" in self.request.params:
            project_Calibration = self.request.params["Calibration"]

        count_P_R = 1
        while True:
            name_PR_inParam = "P_R"+str(count_P_R)
            if name_PR_inParam in self.request.params:
                if self.request.params[name_PR_inParam] in list_PR:
                    pass
                else:
                    list_PR.append(self.request.params[name_PR_inParam])
            else:
                break
            count_P_R+=1

        if "Duration" in self.request.params:
            project_duration = self.request.params["Duration"]

        count_P_M = 1
        while True:
            name_PM_inParam = "P_M"+str(count_P_M)
            if name_PM_inParam in self.request.params:
                if self.request.params[name_PM_inParam] in list_PM:
                    pass
                else:
                    list_PM.append(self.request.params[name_PM_inParam])
            else:
                break
            count_P_M+=1

        if "evaluation" in self.request.params:
            project_evaluation = self.request.params["evaluation"]

        if "Benefits" in self.request.params:
            project_profit = self.request.params["Benefits"]

        count_BGT = 1
        while True:
            name_BGT_inParam = "BGT"+str(count_BGT)
            if name_BGT_inParam in self.request.params:
                if self.request.params[name_BGT_inParam] in list_BGT:
                    pass
                else:
                    list_BGT.append(self.request.params[name_BGT_inParam])
            else:
                break
            count_BGT+=1

        count_DB = 1
        list_DB = []
        while True:
            name_DB1_inParam = "D_B1_"+str(count_DB)
            name_DB2_inParam = "D_B2_"+str(count_DB)
            name_DB3_inParam = "D_B3_"+str(count_DB)
            if name_DB1_inParam in self.request.params and name_DB2_inParam in self.request.params and name_DB3_inParam in self.request.params:
                list_DB.append([self.request.params[name_DB1_inParam],self.request.params[name_DB2_inParam],self.request.params[name_DB3_inParam]])
            else:
                break
            count_DB+=1

        count_schedule = 1
        list_schedule = []
        while True:
            name_schedule1_inParam = "schedule1_"+str(count_schedule)
            name_schedule2_inParam = "schedule2_" + str(count_schedule)
            if name_schedule1_inParam in self.request.params and name_schedule1_inParam in self.request.params:
                list_schedule.append([self.request.params[name_schedule1_inParam],self.request.params[name_schedule2_inParam]])
            else:
                break
            count_schedule+=1

        if "save_proposal" in self.request.params:
            if is_exist == False:
                with transaction.manager:

                    proposal = Proposal(year = project_year,
                                        activity_location=project_activity_location,
                                        Reason = project_reason,
                                        activity_comparition = project_Calibration,
                                        duration = project_duration,
                                        evaluation_index = project_evaluation,
                                        profit = project_profit,
                                        )
                    if type(start_date) != str:
                        project.start_date = start_date
                    if type(finish_date) != str:
                        project.finish_date = finish_date
                    proposal.parent_project = project
                    for i in list_OJ:
                        obj = Objective(text = i)
                        proposal.objective.append(obj)
                    for i in list_PR:
                        PR = Owner_for_proposal(text = i)
                        proposal.owner_for_proposal.append(PR)
                    for i in list_PM:
                        PM = Member_for_proposal(text = i)
                        proposal.member_for_proposal.append(PM)
                    for i in list_BGT:
                        BGT = Cost(text = i)
                        proposal.cost.append(BGT)
                    for i in list_DB:
                        DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                        proposal.delicate_budget.append(DB)
                    for i in list_schedule:
                        sch = Schedule(time=i[0],descrip = i[1])
                        proposal.schedule.append(sch)

                    self.request.db_session.add(proposal)

            else:
                with transaction.manager:
                    proposal = self.request.db_session.query(Proposal).filter_by(parent_id=self.request.headers["project_id"]).first()
                    project = self.request.db_session.query(Project).filter_by(id=self.request.headers["project_id"]).first()
                    proposal.year = project_year
                    proposal.activity_location = project_activity_location
                    proposal.Reason = project_reason
                    proposal.activity_comparition = project_Calibration
                    proposal.durtion = project_duration
                    proposal.evaluation_index = project_evaluation
                    proposal.profit = project_profit
                    if type(start_date)!= str:
                        project.start_date = start_date
                    if type(finish_date) != str:
                        project.finish_date = finish_date
                    for i in list_OJ:
                        obj = Objective(text=i)
                        proposal.objective.append(obj)
                    for i in list_PR:
                        PR = Owner_for_proposal(text=i)
                        proposal.owner_for_proposal.append(PR)
                    for i in list_PM:
                        PM = Member_for_proposal(text=i)
                        proposal.member_for_proposal.append(PM)
                    for i in list_BGT:
                        BGT = Cost(text=i)
                        proposal.cost.append(BGT)
                    for i in list_DB:
                        DB = Delicate_budget(order=i[0], descrip=i[1], value=i[2])
                        proposal.delicate_budget.append(DB)
                    for i in list_schedule:
                        sch = Schedule(time=i[0], descrip=i[1])
                        proposal.schedule.append(sch)
        if "Date-start" in self.request.params:
            start_date_fot_return = self.request.params["Date-start"]
        else:
            start_date_fot_return = ''
        if "Date-finish" in self.request.params:
            finish_date_fot_return = self.request.params["Date-finish"]
        else:
            finish_date_fot_return = ''
        return dict(project_title = project_title,
                    project_year = project_year,
                    project_activity_location = project_activity_location,
                    project_reason = project_reason,
                    project_Calibration = project_Calibration,
                    project_duration = project_duration,
                    project_evaluation = project_evaluation,
                    project_profit = project_profit,
                    start_date = start_date_fot_return,
                    finish_date = finish_date_fot_return,
                    OJ_ = list_OJ,
                    PR_ = list_PR,
                    PM_ = list_PM,
                    BGT_ = list_BGT,
                    DB_ = list_DB,
                    Sch_ = list_schedule,
                   )








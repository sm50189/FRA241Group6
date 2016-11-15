# -- coding: utf-8 --
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
                project_duration=proposal.duration
                project_evaluation = proposal.evaluation_index
                project_profit=proposal.profit
                list_OJ = proposal.objective
                # list_OJ = [ i.text for i in proposal.objective]
                # count_OJ = len(list_OJ)
                list_PR = proposal.owner_for_proposal
                # list_PR = [i.text for i in proposal.owner_for_proposal]
                # count_P_R = len(list_PR)
                list_PM = proposal.member_for_proposal
                # list_PM = [i.text for i in proposal.member_for_proposal]
                # count_P_M = len(list_PM)
                list_BGT = proposal.cost
                # list_BGT = [i.text for i in proposal.cost]
                # count_BGT = len(list_BGT)
                list_DB = proposal.delicate_budget
                # list_DB = [[i.order,i.descrip,i.value] for i in proposal.delicate_budget]
                # count_DB = len(list_DB)
                list_schedule = proposal.schedule
                # list_schedule = [[i.time,i.descrip] for i in proposal.schedule]
                # count_schedule = len(list_schedule)
            is_exist = True
        except NoResultFound:
            is_exist = False
            project_year = ''
            project_activity_location = ''
            project_reason = ''
            project_Calibration = ''
            project_duration = ''
            project_evaluation = ''
            project_profit = ''
            list_OJ = ''
            count_OJ = len(list_OJ)
            list_PR = ''
            count_P_R = len(list_PR)
            list_PM = ''
            count_P_M = len(list_PM)
            list_BGT = ''
            count_BGT = len(list_BGT)
            list_DB = ''
            count_DB = len(list_DB)
            list_schedule = ''
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

        if self.request.params.get("OJ","0") == "0":list_OJ = ''
        if self.request.params.get("P_R","0") == "0":list_PR = ''
        if self.request.params.get("P_M","0") == "0":list_PM = ''
        if self.request.params.get("BGT","0") == "0":list_BGT = ''
        if self.request.params.get("D_B","0") == "0":list_DB = ''
        if self.request.params.get("schedule","0") == "0":list_schedule = ''

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
        if "OJ1" in self.request.params:
            list_OJ = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "OJ"+str(count_OJ)
            if name_inParam in self.request.params:
                list_OJ += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_OJ+=1

        # if "Calibration" in self.request.params:
        #     project_Calibration = self.request.params["Calibration"]
        if "myradio" in self.request.params:
            print "\n\n\n\nHave myradio\n\n\n\n\n\n"
            if self.request.params["myradio"] == "2":
                project_Calibration = u"กิจกรรมที่ไม่นับหน่วยชั่วโมง,"
            elif self.request.params["myradio"] == "1":
                project_Calibration = u"กิจกรรมเลือกเข้าร่วม,"
                if self.request.params.get("checkbox1","") != "":
                    project_Calibration += u"ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ:"+self.request.params.get("CB1",'')+","
                if self.request.params.get("checkbox2","") != "":
                    project_Calibration += u"ด้านกีฬาและการส่งเสริมสุขภาพ:"+self.request.params.get("CB2",'')+","
                if self.request.params.get("checkbox3","") != "":
                    project_Calibration += u"ด้านบำเพ็ญประโยชน์และรักษาสิ่งแวดล้อม:"+self.request.params.get("CB3","")+","
                if self.request.params.get("checkbox4","") != "":
                    project_Calibration += u"ด้านทำนุบำรุงศิลปะและวัฒนธรรม:"+self.request.params.get("CB4","")+","
                if self.request.params.get("checkbox5","") != "":
                    project_Calibration += u"ด้านนันทนาการและการพัฒนาบุคลิกภาพ:"+self.request.params.get("CB5","")+","
                if self.request.params.get("checkbox6","") != "" :
                    project_Calibration += u"ด้านความภูมิใจ ความรัก ความผูกพันธ์มหาวิทยาลัย:"+self.request.params.get("CB6","")+","
        dict_type = {u"ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ":1,u"ด้านกีฬาและการส่งเสริมสุขภาพ":2,u"ด้านบำเพ็ญประโยชน์และรักษาสิ่งแวดล้อม":3,u"ด้านทำนุบำรุงศิลปะและวัฒนธรรม":4,u"ด้านนันทนาการและการพัฒนาบุคลิกภาพ":5,u"ด้านความภูมิใจ ความรัก ความผูกพันธ์มหาวิทยาลัย":6}
        count_P_R = 1
        if "P_R1" in self.request.params:
            list_PR = ''
        while True:
            name_PR_inParam = "P_R"+str(count_P_R)
            if name_PR_inParam in self.request.params:
                list_PR += self.request.params[name_PR_inParam]+unichr(171)
            else:
                break
            count_P_R+=1

        if "Duration" in self.request.params:
            project_duration = self.request.params["Duration"]

        count_P_M = 1
        if "P_M1" in self.request.params:
            list_PM = ''
        while True:
            name_PM_inParam = "P_M"+str(count_P_M)
            if name_PM_inParam in self.request.params:
               list_PM += self.request.params[name_PM_inParam]+unichr(171)
            else:
                break
            count_P_M+=1

        if "evaluation" in self.request.params:
            project_evaluation = self.request.params["evaluation"]

        if "Benefits" in self.request.params:
            project_profit = self.request.params["Benefits"]

        count_BGT = 1
        if "BGT1" in self.request.params:
            list_BGT = ''
        while True:
            name_BGT_inParam = "BGT"+str(count_BGT)
            if name_BGT_inParam in self.request.params:
                list_BGT += self.request.params[name_BGT_inParam]+unichr(171)
            else:
                break
            count_BGT+=1

        count_DB = 1
        if "D_B1_1" in self.request.params:
            list_DB = ''
        while True:
            name_DB1_inParam = "D_B1_"+str(count_DB)
            name_DB2_inParam = "D_B2_"+str(count_DB)
            name_DB3_inParam = "D_B3_"+str(count_DB)
            if name_DB1_inParam in self.request.params and name_DB2_inParam in self.request.params and name_DB3_inParam in self.request.params:
                list_DB += self.request.params[name_DB1_inParam]+unichr(172)+self.request.params[name_DB2_inParam]+unichr(172)+self.request.params[name_DB3_inParam]+unichr(171)
            else:
                break
            count_DB+=1

        count_schedule = 1
        if "schedule1_1" in self.request.params:
            print "\n\n\n\n\nin this fucking condition\n\n\n\n\n"
            list_schedule = ''
        while True:
            name_schedule1_inParam = "schedule1_"+str(count_schedule)
            name_schedule2_inParam = "schedule2_" + str(count_schedule)
            if name_schedule1_inParam in self.request.params and name_schedule1_inParam in self.request.params:
                list_schedule+=self.request.params[name_schedule1_inParam]+unichr(172)+self.request.params[name_schedule2_inParam]+unichr(171)
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
                                        objective = list_OJ,
                                        owner_for_proposal = list_PR,
                                        member_for_proposal = list_PM,
                                        cost = list_BGT,
                                        delicate_budget = list_DB,
                                        schedule = list_schedule,
                                        )
                    if type(start_date) != str:
                        project.start_date = start_date
                    if type(finish_date) != str:
                        project.finish_date = finish_date
                    proposal.parent_project = project
                    # for i in list_OJ:
                    #     obj = Objective(text = i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text = i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text = i)
                    #     proposal.member_for_proposal.append(PM)
                    # for i in list_BGT:
                    #     BGT = Cost(text = i)
                    #     proposal.cost.append(BGT)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                    #     proposal.delicate_budget.append(DB)
                    # for i in list_schedule:
                    #     sch = Schedule(time=i[0],descrip = i[1])
                    #     proposal.schedule.append(sch)

                    self.request.db_session.add(proposal)

            else:
                with transaction.manager:
                    proposal = self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).first()
                    project = self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first()
                    proposal.year = project_year
                    proposal.activity_location = project_activity_location
                    proposal.Reason = project_reason
                    proposal.activity_comparition = project_Calibration
                    proposal.durtion = project_duration
                    proposal.evaluation_index = project_evaluation
                    proposal.profit = project_profit
                    proposal.objective = list_OJ
                    proposal.owner_for_proposal = list_PR
                    proposal.member_for_proposal = list_PM
                    proposal.cost = list_BGT
                    proposal.delicate_budget = list_DB
                    proposal.schedule = list_schedule
                    if type(start_date)!= str:
                        project.start_date = start_date
                    if type(finish_date) != str:
                        project.finish_date = finish_date
                    # for i in list_OJ:
                    #     obj = Objective(text=i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text=i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text=i)
                    #     proposal.member_for_proposal.append(PM)
                    # for i in list_BGT:
                    #     BGT = Cost(text=i)
                    #     proposal.cost.append(BGT)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order=i[0], descrip=i[1], value=i[2])
                    #     proposal.delicate_budget.append(DB)
                    # for i in list_schedule:
                    #     sch = Schedule(time=i[0], descrip=i[1])
                    #     proposal.schedule.append(sch)

        if "Date-start" in self.request.params:
            start_date_fot_return = self.request.params["Date-start"]
        else:
            start_date_fot_return = ''
        if "Date-finish" in self.request.params:
            finish_date_fot_return = self.request.params["Date-finish"]
        else:
            finish_date_fot_return = ''
        dict2return =  dict(project_title=project_title,
                    project_year=project_year,
                    project_activity_location=project_activity_location,
                    project_reason=project_reason,
                    project_duration=project_duration,
                    project_evaluation=project_evaluation,
                    project_profit=project_profit,
                    start_date=start_date_fot_return,
                    finish_date=finish_date_fot_return,
                    OJ_=[i for i in list_OJ.split(unichr(171)) if i != ''],
                    PR_=[i for i in list_PR.split(unichr(171)) if i != ''],
                    PM_=[i for i in list_PM.split(unichr(171)) if i != ''],
                    BGT_=[i for i in list_BGT.split(unichr(171)) if i != ''],
                    DB_=[i.split(unichr(172)) for i in list_DB.split(unichr(171)) if len(i.split(unichr(172)))==3 and '' not in i.split(unichr(172))],
                    Sch_=[i.split(unichr(172))for i in list_schedule.split(unichr(171)) if len(i.split(unichr(172)))==2 and '' not in i.split(unichr(172))],
                    )
        split_calibration = project_Calibration.split(",")
        print "\n\n\n\n this is fucking split text",split_calibration,"\n\n\n\n\n"
        if split_calibration == u"กิจกรรมที่ไม่นับหน่วยชั่วโมง":
            dict2return.update(dict(myradio2="checked"))

        else:
            dict2return.update(dict(myradio1="checked"))
            for i in range(1,len(split_calibration)-1):
                if split_calibration[i].split(":")[0] in dict_type:
                    if dict_type[split_calibration[i].split(":")[0]]==1:
                        dict2return.update(dict(Checkbox1=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 2:
                        dict2return.update(dict(Checkbox2=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 3:
                        dict2return.update(dict(Checkbox3=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 4:
                        dict2return.update(dict(Checkbox4=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 5:
                        dict2return.update(dict(Checkbox5=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 6:
                        dict2return.update(dict(Checkbox6=split_calibration[i].split(":")[1]))
        print "\n\n\n\n this is fucking fucking return-dick",dict2return,"\n\n\n\n\n\n\n"
        return dict2return

    @view_config(route_name = 'proposal',match_param="type_project=competitive",renderer = "../templates/formCompetition.pt")
    def form_competitive(self):
        try:
            with self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).one() as proposal:
                project_year=proposal.year
                project_place=proposal.location
                project_activity_location = proposal.activity_location
                project_reason= proposal.Reason
                project_Bene=proposal.profit
                project_advisor = proposal.advisor_for_proposal
                project_activity_type = proposal.type_of_activity
                project_criteria = proposal.success_criteria
                list_OJ = proposal.objective
                # list_OJ = [ i.text for i in proposal.objective]
                # count_OJ = len(list_OJ)
                list_PR = proposal.owner_for_proposal
                # list_PR = [i.text for i in proposal.owner_for_proposal]
                # count_P_R = len(list_PR)
                list_PM = proposal.member_for_proposal
                # list_PM = [i.text for i in proposal.member_for_proposal]
                # count_P_M = len
                list_DB = proposal.delicate_budget
                # list_DB = [[i.order,i.descrip,i.value] for i in proposal.delicate_budget]
                # count_DB = len(list_DB)
            is_exist = True
        except NoResultFound:
            project_year = ''
            project_activity_location = ''
            project_place = ''
            project_reason = ''
            project_activity_type = ''
            project_criteria = ''
            project_Bene = ''
            project_advisor = ''
            list_OJ = ''
            count_OJ = len(list_OJ)
            list_PR = ''
            count_P_R = len(list_PR)
            list_PM = ''
            count_P_M = len(list_PM)
            list_DB = ''
            count_DB = len(list_DB)
            is_exist = False


        try:
            with self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first() as project:
                # start_date = str(project.start_date.day) + "/" + str(project.start_date.month) + "/" + str(project.start_date.year)
                # finish_date = str(project.finish_date.day) + "/" + str(project.finish_date.month) + "/" + str(project.finish_date.year)
                project_title = project.title
                if project.start_date is not None:
                    start_date = str(project.start_date.day)+"/"+str(project.start_date.month)+"/"+str(project.start_date.year)
                elif project.start_date is None:
                    start_date = ''
                # if project.finish_date is not None:
                #     finish_date = str(project.finish_date.day)+"/"+str(project.finish_date.month)+"/"+str(project.finish_date.year)
                # else:
                #     finish_date = ''
        except NoResultFound:
            print "\n\n\n\n\n\n\nwhy the fuck there is no result\n\n\n\n\n\n\n"
            return HTTPFound(location=self.request.route_url("addProject"))

        if self.request.params.get("OJ","0") == "0":list_OJ = ''
        if self.request.params.get("P_R","0") == "0":list_PR = ''
        if self.request.params.get("P_M","0") == "0":list_PM = ''
        if self.request.params.get("S_P","0") == "0":project_criteria = ''
        if self.request.params.get("Benefits","0") == "0":project_Bene = ''
        if self.request.params.get("D_B","0") == "0":list_DB = ''

        if "Year" in self.request.params:
            project_year = self.request.params.get("Year",'')

        if "Place" in self.request.params:
            project_place = self.request.params.get("Place",'')

        if "Date" in self.request.params:
            raw_date_start = self.request.params["Date"]
            if "/" not in raw_date_start:
                raw_date_start = 'Invalid format'
            split_start_date = raw_date_start.split("/")
            if len(split_start_date) != 3:
                raw_date_start = 'Invalid format'
            for i in split_start_date:
                if i.isdigit() == False:
                    raw_date_start = 'Invalid format'
                    break

            if raw_date_start != 'Invalid format':
                start_date = datetime.date(int(split_start_date[2]), int(split_start_date[1]), int(split_start_date[0]))

            else:
                start_date = ''

        if "Reason_Project" in self.request.params:
            project_reason = self.request.params.get('Reason_Project',"")

        count_OJ = 1
        if "OJ1" in self.request.params:
            list_OJ = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "OJ"+str(count_OJ)
            if name_inParam in self.request.params:
                list_OJ += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_OJ+=1

        count_Bene = 1
        if "Benefits1_1" in self.request.params:
            project_Bene = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "Benefits1_"+str(count_Bene)
            if name_inParam in self.request.params:
                project_Bene += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_Bene+=1

        count_P_R = 1
        if "P_R1" in self.request.params:
            list_PR = ''
        while True:
            name_PR_inParam = "P_R"+str(count_P_R)
            if name_PR_inParam in self.request.params:
                list_PR += self.request.params[name_PR_inParam]+unichr(171)
            else:
                break
            count_P_R+=1

        if "Advisor" in self.request.params:
            project_advisor = self.request.params.get("Advisor",'')

        count_P_M = 1
        if "P_M1" in self.request.params:
            list_PM = ''
        while True:
            name_PM_inParam = "P_M"+str(count_P_M)
            if name_PM_inParam in self.request.params:
                list_PM += self.request.params[name_PM_inParam]+unichr(171)
            else:
                break
            count_P_M+=1

        if "P_P" in self.request.params:
            project_activity_location = self.request.params.get("P_P",'')

        if "P_C" in self.request.params:
            project_activity_type = self.request.params["P_C"]

        count_DB = 1
        if "D_B1_1" in self.request.params:
            list_DB = ''
        while True:
            name_DB1_inParam = "D_B1_"+str(count_DB)
            name_DB2_inParam = "D_B2_"+str(count_DB)
            name_DB3_inParam = "D_B3_"+str(count_DB)
            if name_DB1_inParam in self.request.params and name_DB2_inParam in self.request.params and name_DB3_inParam in self.request.params:
                list_DB += self.request.params[name_DB1_inParam]+unichr(172)+self.request.params[name_DB2_inParam]+unichr(172)+self.request.params[name_DB3_inParam]+unichr(171)
            else:
                break
            count_DB+=1

        count_criteria = 1
        if "S_P1_1" in self.request.params:
            project_criteria = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "S_P1_"+str(count_criteria)
            if name_inParam in self.request.params:
                project_criteria += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_criteria+=1

        if "save_proposal" in self.request.params:
            if is_exist == False:
                with transaction.manager:

                    proposal = Proposal(year = project_year,
                                        location = project_place,
                                        activity_location=project_activity_location,
                                        Reason = project_reason,
                                        type_of_activity = project_activity_type,
                                        profit = project_Bene,
                                        advisor_for_proposal = project_advisor,
                                        success_criteria = project_criteria,
                                        objective = list_OJ,
                                        owner_for_proposal = list_PR,
                                        member_for_proposal = list_PM,
                                        delicate_budget = list_DB,
                                        )
                    if type(start_date) != str:
                        project.start_date = start_date
                    proposal.parent_project = project
                    # for i in list_OJ:
                    #     obj = Objective(text = i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text = i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text = i)
                    #     proposal.member_for_proposal.append(PM)
                    # # for i in list_BGT:
                    # #     BGT = Cost(text = i)
                    # #     proposal.cost.append(BGT)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                    #     proposal.delicate_budget.append(DB)
                    # # for i in list_schedule:
                    # #     sch = Schedule(time=i[0],descrip = i[1])
                    # #     proposal.schedule.append(sch)

                    self.request.db_session.add(proposal)

            else:
                with transaction.manager:
                    proposal = self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).first()
                    project = self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first()
                    proposal.year = project_year
                    proposal.location = project_place
                    proposal.activity_location=project_activity_location
                    proposal.Reason = project_reason
                    proposal.type_of_activity = project_activity_type
                    proposal.profit = project_Bene
                    proposal.advisor_for_proposal = project_advisor
                    proposal.success_criteria = project_criteria
                    proposal.objective = list_OJ
                    proposal.owner_for_proposal = list_PR
                    proposal.member_for_proposal = list_PM
                    proposal.delicate_budget = list_DB
                    if type(start_date)!= str:
                        project.start_date = start_date
                    # for i in list_OJ:
                    #     obj = Objective(text = i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text = i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text = i)
                    #     proposal.member_for_proposal.append(PM)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                    #     proposal.delicate_budget.append(DB)

        if "Date" in self.request.params:
            start_date_fot_return = self.request.params["Date"]
        else:
            start_date_fot_return = ''
        dict2return =  dict(project_title=project_title,
                    project_year = project_year,
                    project_place= project_place,
                    project_activity_location = project_activity_location,
                    project_reason = project_reason,
                    project_activity_type = project_activity_type,
                    project_Bene = [i for i in project_Bene.split(unichr(171)) if i!=''],
                    project_advisor = project_advisor,
                    project_criteria = [i for i in project_criteria.split(unichr(171)) if i!=''],
                    start_date=start_date_fot_return,
                    OJ_=[i for i in list_OJ.split(unichr(171)) if i!=''],
                    PR_=[i for i in list_PR.split(unichr(171)) if i!= ''],
                    PM_=[i for i in list_PM.split(unichr(171)) if i!= ''],
                    DB_=[i.split(unichr(172)) for i in list_DB.split(unichr(171)) if len(i.split(unichr(172)))==3 and '' not in i.split(unichr(172))],
                    )
        # split_calibration = project_Calibration.split(",")
        # print "\n\n\n\n this is fucking split text",split_calibration,"\n\n\n\n\n"
        # if split_calibration == u"กิจกรรมที่ไม่นับหน่วยlenชั่วโมง":
        #     dict2return.update(dict(myradio2="checked"))

        # else:
        #     dict2return.update(dict(myradio1="checked"))
        #     for i in range(1,len(split_calibration)-1):
        #         if split_calibration[i].split(":")[0] in dict_type:
        #             if dict_type[split_calibration[i].split(":")[0]]==1:
        #                 dict2return.update(dict(Checkbox1=split_calibration[i].split(":")[1]))
        #             if dict_type[split_calibration[i].split(":")[0]] == 2:
        #                 dict2return.update(dict(Checkbox2=split_calibration[i].split(":")[1]))
        #             if dict_type[split_calibration[i].split(":")[0]] == 3:
        #                 dict2return.update(dict(Checkbox3=split_calibration[i].split(":")[1]))
        #             if dict_type[split_calibration[i].split(":")[0]] == 4:
        #                 dict2return.update(dict(Checkbox4=split_calibration[i].split(":")[1]))
        #             if dict_type[split_calibration[i].split(":")[0]] == 5:
        #                 dict2return.update(dict(Checkbox5=split_calibration[i].split(":")[1]))
        #             if dict_type[split_calibration[i].split(":")[0]] == 6:
        #                 dict2return.update(dict(Checkbox6=split_calibration[i].split(":")[1]))
        print "\n\n\n\n this is fucking fucking return dick",dict2return,"\n\n\n\n\n\n\n"
        return dict2return

    @view_config(route_name = 'proposal',match_param="type_project=volunteer",renderer = "../templates/formVolunteer.pt")
    def form_volunteer(self):
        try:
            with self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).one() as proposal:
                project_year=proposal.year
                project_activity_location = proposal.activity_location
                project_reason= proposal.Reason
                project_Bene=proposal.profit
                project_Calibration = proposal.activity_comparition
                project_advisor = proposal.advisor_for_proposal
                project_activity_type = proposal.type_of_activity
                project_previouse_result = proposal.previouse_result
                project_criteria = proposal.success_criteria
                project_evaluation = proposal.evaluation_index
                project_duration = proposal.duration
                list_OJ = proposal.objective
                # list_OJ = [ i.text for i in proposal.objective]
                # count_OJ = len(list_OJ)
                list_PR = proposal.owner_for_proposal
                # list_PR = [i.text for i in proposal.owner_for_proposal]
                # count_P_R = len(list_PR)
                list_PM = proposal.member_for_proposal
                # list_PM = [i.text for i in proposal.member_for_proposal]
                # count_P_M = len
                list_DB = proposal.delicate_budget
                # list_DB = [[i.order,i.descrip,i.value] for i in proposal.delicate_budget]
                # count_DB = len(list_DB)
                list_schedule = proposal.schedule
            is_exist = True
        except NoResultFound:
            project_year=''
            project_activity_location = ''
            project_reason= ''
            project_Bene= ''
            project_Calibration = ''
            project_advisor = ''
            project_activity_type = ''
            project_previouse_result = ''
            project_criteria = ''
            project_evaluation = ''
            project_duration = ''
            list_OJ = ''
            list_PR = ''
            list_PM = ''
            list_DB = ''
            list_schedule = ''
            is_exist = False


        try:
            with self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first() as project:
                # start_date = str(project.start_date.day) + "/" + str(project.start_date.month) + "/" + str(project.start_date.year)
                # finish_date = str(project.finish_date.day) + "/" + str(project.finish_date.month) + "/" + str(project.finish_date.year)
                project_title = project.title
                if project.start_date is not None:
                    start_date = str(project.start_date.day)+"/"+str(project.start_date.month)+"/"+str(project.start_date.year)
                elif project.start_date is None:
                    start_date = ''
                # if project.finish_date is not None:
                #     finish_date = str(project.finish_date.day)+"/"+str(project.finish_date.month)+"/"+str(project.finish_date.year)
                # else:
                #     finish_date = ''
        except NoResultFound:
            print "\n\n\n\n\n\n\nwhy the fuck there is no result\n\n\n\n\n\n\n"
            return HTTPFound(location=self.request.route_url("addProject"))
        if self.request.params.get("OJ","0") == "0":list_OJ = ''
        if self.request.params.get("P_R","0") == "0":list_PR = ''
        if self.request.params.get("P_M","0") == "0":list_PM = ''
        if self.request.params.get("S_P","0") == "0":project_criteria = ''
        if self.request.params.get("Benefits","0") == "0":project_Bene = ''
        if self.request.params.get("BGT","0") == "0":list_DB = ''
        if self.request.params.get("schedule","0") == "0":list_schedule = ''

        if "Year" in self.request.params:
            project_year = self.request.params.get("Year",'')

        if "Reason_Project" in self.request.params:
            project_reason = self.request.params.get('Reason_Project',"")

        if "myradio" in self.request.params:
            print "\n\n\n\nHave myradio\n\n\n\n\n\n"
            if self.request.params["myradio"] == "2":
                project_Calibration = u"กิจกรรมที่ไม่นับหน่วยชั่วโมง,"
            elif self.request.params["myradio"] == "1":
                project_Calibration = u"กิจกรรมเลือกเข้าร่วม,"
                if self.request.params.get("checkbox1","") != "":
                    project_Calibration += u"ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ:"+self.request.params.get("CB1",'')+","
                if self.request.params.get("checkbox2","") != "":
                    project_Calibration += u"ด้านกีฬาและการส่งเสริมสุขภาพ:"+self.request.params.get("CB2",'')+","
                if self.request.params.get("checkbox3","") != "":
                    project_Calibration += u"ด้านบำเพ็ญประโยชน์และรักษาสิ่งแวดล้อม:"+self.request.params.get("CB3","")+","
                if self.request.params.get("checkbox4","") != "":
                    project_Calibration += u"ด้านทำนุบำรุงศิลปะและวัฒนธรรม:"+self.request.params.get("CB4","")+","
                if self.request.params.get("checkbox5","") != "":
                    project_Calibration += u"ด้านนันทนาการและการพัฒนาบุคลิกภาพ:"+self.request.params.get("CB5","")+","
                if self.request.params.get("checkbox6","") != "" :
                    project_Calibration += u"ด้านความภูมิใจ ความรัก ความผูกพันธ์มหาวิทยาลัย:"+self.request.params.get("CB6","")+","
        dict_type = {u"ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ":1,u"ด้านกีฬาและการส่งเสริมสุขภาพ":2,u"ด้านบำเพ็ญประโยชน์และรักษาสิ่งแวดล้อม":3,u"ด้านทำนุบำรุงศิลปะและวัฒนธรรม":4,u"ด้านนันทนาการและการพัฒนาบุคลิกภาพ":5,u"ด้านความภูมิใจ ความรัก ความผูกพันธ์มหาวิทยาลัย":6}

        count_OJ = 1
        if "OJ1" in self.request.params:
            list_OJ = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "OJ"+str(count_OJ)
            if name_inParam in self.request.params:
                list_OJ += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_OJ+=1

        count_Bene = 1
        if "Benefits1_1" in self.request.params:
            project_Bene = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "Benefits1_"+str(count_Bene)
            if name_inParam in self.request.params:
                project_Bene += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_Bene+=1

        count_P_R = 1
        if "P_R1" in self.request.params:
            list_PR = ''
        while True:
            name_PR_inParam = "P_R"+str(count_P_R)
            if name_PR_inParam in self.request.params:
                list_PR += self.request.params[name_PR_inParam]+unichr(171)
            else:
                break
            count_P_R+=1

        if "Advisor" in self.request.params:
            project_advisor = self.request.params.get("Advisor",'')

        count_P_M = 1
        if "P_M1" in self.request.params:
            list_PM = ''
        while True:
            name_PM_inParam = "P_M"+str(count_P_M)
            if name_PM_inParam in self.request.params:
                list_PM += self.request.params[name_PM_inParam]+unichr(171)
            else:
                break
            count_P_M+=1

        if "P_P" in self.request.params:
            project_activity_location = self.request.params.get("P_P",'')

        if "P_C" in self.request.params:
            project_activity_type = self.request.params["P_C"]

        if "O_E" in self.request.params:
            project_previouse_result = self.request.params["O_E"]

        count_DB = 1
        if "BGT1_1" in self.request.params:
            list_DB = ''
        while True:
            name_DB1_inParam = "BGT1_"+str(count_DB)
            name_DB2_inParam = "BGT2_"+str(count_DB)
            name_DB3_inParam = "BGT3_"+str(count_DB)
            if name_DB1_inParam in self.request.params and name_DB2_inParam in self.request.params and name_DB3_inParam in self.request.params:
                list_DB += self.request.params[name_DB1_inParam]+unichr(172)+self.request.params[name_DB2_inParam]+unichr(172)+self.request.params[name_DB3_inParam]+unichr(171)
            else:
                break
            count_DB+=1

        count_criteria = 1
        if "S_P1_1" in self.request.params:
            project_criteria = ''
        while True:
            print "\n\nfucking loop\n\n"
            name_inParam = "S_P1_"+str(count_criteria)
            if name_inParam in self.request.params:
                project_criteria += self.request.params[name_inParam]+unichr(171)
            else:
                break
            count_criteria+=1

        if "evaluation" in self.request.params:
            project_evaluation = self.request.params["evaluation"]

        if "Duration" in self.request.params:
            project_duration = self.request.params["Duration"]

        count_schedule = 1
        if "schedule1_1" in self.request.params:
            print "\n\n\n\n\nin this fucking condition\n\n\n\n\n"
            list_schedule = ''
        while True:
            name_schedule1_inParam = "schedule1_"+str(count_schedule)
            name_schedule2_inParam = "schedule2_" + str(count_schedule)
            if name_schedule1_inParam in self.request.params and name_schedule1_inParam in self.request.params:
                list_schedule+=self.request.params[name_schedule1_inParam]+unichr(172)+self.request.params[name_schedule2_inParam]+unichr(171)
            else:
                break
            count_schedule+=1

        if "save_proposal" in self.request.params:
            if is_exist == False:
                with transaction.manager:
                    proposal = Proposal(year = project_year,
                                        activity_location=project_activity_location,
                                        Reason = project_reason,
                                        type_of_activity = project_activity_type,
                                        activity_comparition = project_Calibration,
                                        previouse_result = project_previouse_result,
                                        evaluation_index = project_evaluation,
                                        profit = project_Bene,
                                        advisor_for_proposal = project_advisor,
                                        success_criteria = project_criteria,
                                        objective = list_OJ,
                                        owner_for_proposal = list_PR,
                                        duration = project_duration,
                                        member_for_proposal = list_PM,
                                        delicate_budget = list_DB,
                                        schedule = list_schedule,
                                        )
                    if type(start_date) != str:
                        project.start_date = start_date
                    proposal.parent_project = project
                    # for i in list_OJ:
                    #     obj = Objective(text = i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text = i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text = i)
                    #     proposal.member_for_proposal.append(PM)
                    # # for i in list_BGT:
                    # #     BGT = Cost(text = i)
                    # #     proposal.cost.append(BGT)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                    #     proposal.delicate_budget.append(DB)
                    # # for i in list_schedule:
                    # #     sch = Schedule(time=i[0],descrip = i[1])
                    # #     proposal.schedule.append(sch)
                    print "\n\n\n\n\n\n\n\nadded added added added added\n\n\n\n\n\n"
                    self.request.db_session.add(proposal)

            else:
                with transaction.manager:
                    proposal = self.request.db_session.query(Proposal).filter_by(parent_id=self.request.matchdict["project_id"]).first()
                    project = self.request.db_session.query(Project).filter_by(id=self.request.matchdict["project_id"]).first()
                    proposal.year = project_year
                    proposal.activity_location=project_activity_location
                    proposal.Reason = project_reason
                    proposal.type_of_activity = project_activity_type
                    proposal.previouse_result = project_previouse_result
                    proposal.profit = project_Bene
                    proposal.activity_comparition = project_Calibration
                    proposal.advisor_for_proposal = project_advisor
                    proposal.success_criteria = project_criteria
                    proposal.evaluation_index = project_evaluation
                    proposal.objective = list_OJ
                    proposal.owner_for_proposal = list_PR
                    proposal.member_for_proposal = list_PM
                    proposal.delicate_budget = list_DB
                    proposal.duration = project_duration
                    proposal.schedule = list_schedule
                    if type(start_date)!= str:
                        project.start_date = start_date
                    print "\n\n\n\n\n\n\n\nchanged\n\n\n\n\n\n"
                    # for i in list_OJ:
                    #     obj = Objective(text = i)
                    #     proposal.objective.append(obj)
                    # for i in list_PR:
                    #     PR = Owner_for_proposal(text = i)
                    #     proposal.owner_for_proposal.append(PR)
                    # for i in list_PM:
                    #     PM = Member_for_proposal(text = i)
                    #     proposal.member_for_proposal.append(PM)
                    # for i in list_DB:
                    #     DB = Delicate_budget(order = i[0],descrip = i[1], value = i[2])
                    #     proposal.delicate_budget.append(DB)

        if "Date" in self.request.params:
            start_date_fot_return = self.request.params["Date"]
        else:
            start_date_fot_return = ''
        dict2return =  dict(project_title=project_title,
                    project_year = project_year,
                    project_activity_location = project_activity_location,
                    project_reason = project_reason,
                    project_activity_type = project_activity_type,
                    project_previouse_result = project_previouse_result,
                    project_Bene = [i for i in project_Bene.split(unichr(171)) if i!=''],
                    project_advisor = project_advisor,
                    project_criteria = [i for i in project_criteria.split(unichr(171)) if i!=''],
                    project_evaluation = project_evaluation,
                    start_date=start_date_fot_return,
                    project_duration = project_duration,
                    OJ_=[i for i in list_OJ.split(unichr(171)) if i!=''],
                    PR_=[i for i in list_PR.split(unichr(171)) if i!= ''],
                    PM_=[i for i in list_PM.split(unichr(171)) if i!= ''],
                    DB_=[i.split(unichr(172)) for i in list_DB.split(unichr(171)) if len(i.split(unichr(172)))==3 and '' not in i.split(unichr(172))],
                    Sch_=[i.split(unichr(172)) for i in list_schedule.split(unichr(171)) if len(i.split(unichr(172)))==2 and '' not in i.split(unichr(172))]
                    )
        split_calibration = project_Calibration.split(",")
        print "\n\n\n\n this is fucking split text",split_calibration,"\n\n\n\n\n"
        if split_calibration == u"กิจกรรมที่ไม่นับหน่วยlenชั่วโมง":
            dict2return.update(dict(myradio2="checked"))

        else:
            dict2return.update(dict(myradio1="checked"))
            for i in range(1,len(split_calibration)-1):
                if split_calibration[i].split(":")[0] in dict_type:
                    if dict_type[split_calibration[i].split(":")[0]]==1:
                        dict2return.update(dict(Checkbox1=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 2:
                        dict2return.update(dict(Checkbox2=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 3:
                        dict2return.update(dict(Checkbox3=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 4:
                        dict2return.update(dict(Checkbox4=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 5:
                        dict2return.update(dict(Checkbox5=split_calibration[i].split(":")[1]))
                    if dict_type[split_calibration[i].split(":")[0]] == 6:
                        dict2return.update(dict(Checkbox6=split_calibration[i].split(":")[1]))
        print "\n\n\n\n this is fucking fucking return dick",dict2return,"\n\n\n\n\n\n\n"
        return dict2return














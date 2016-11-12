from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm.exc import NoResultFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User

import transaction

@view_config(route_name='login', renderer='../templates/login.pt')
def login(request):
    # next_url = request.params.get('next', request.referrer)
    next_url = request.route_url('home')
    # if not next_url:
    #     next_url = request.route_url('home')
    print '\n\n\n\n\n####################################################\n\n\n\n\n\n'
    message = 'what'
    message2 = ''
    login = 'Username...'
    form_user_name = 'User name...'
    form_student_id = 'Student id...'
    form_pass_word = 'password...'
    form_repass_word = 'retype password...'
    form_first_name = 'First name...'
    form_last_name = 'Last name...'
    form_email = 'Email...'
    form_role = 'Please choose your status'

    is_exist = True
    if 'form.submitted' in request.params:
        login = request.params['form-username']
        password = request.params['form-password']
        try:
            user = request.db_session.query(User).filter_by(user_id=login).first()
            if user is not None and user.check_password(password):
                headers = remember(request, user.id)
                message = 'grat'
                print "\n\n\n\n\n grat \n\n\n\n\n\n",next_url,'\n\n\n\n\n\n'
                return HTTPFound(location=next_url, headers=headers)
            message = 'Failed login'
        except NoResultFound:
            message = 'Failed login'

    elif 'form.signup' in request.params:
        form_user_name = request.params.get("form-user-name")
        form_student_id = request.params.get("form-student-id")
        form_pass_word = request.params.get("form-pass-word")
        form_repass_word = request.params.get("form-repass-word")
        form_first_name = request.params.get("form-first-name")
        form_last_name = request.params.get("form-last-name")
        form_email = request.params.get("form-email")
        form_role = request.params.get("form-user-role")
        if form_user_name is not None:
            try:
                user = request.db_session.query(User).filter_by(user_id=form_user_name).first()
                if user is None:
                    is_exist = False
                else:
                    print  'fuck'
                    is_exist = True
                    message2 = 'Already have this user id'
            except NoResultFound:
                is_exist = False
                pass
        if form_user_name is None or form_user_name == '':
            message2 = 'User name Invalid'
        elif form_student_id is None or form_student_id == '' or form_student_id.isdigit() == False:
            message2 = 'Student ID Invalid'
        elif int(form_student_id)/10000000000 == 0:
            message2 = 'Student ID Invalid'
        elif form_pass_word is None or form_pass_word == '' or form_pass_word != form_repass_word:
            message2 = 'password Invalid'
        elif form_first_name is None or form_first_name == '' :
            message2 = 'First name Invalid'
        elif form_last_name is None or form_last_name == '':
            message2 = 'Last name Invalid'
        elif form_email is None or form_email == '' :
            message2 = 'email Invalid'
        elif form_role is None or form_role == 'Please choose your statue' or (form_role != 'Teacher' and form_role != 'Student'):
            message2 = 'choose your Statue'
        elif is_exist == False:
            with transaction.manager:
                session = request.db_session
                user = User(First_name = form_first_name, Last_name= form_last_name,role=form_role,student_id=int(form_student_id),Email=form_email,user_id=form_user_name,year=int(form_student_id)/1000000000)
                user.hash_password(form_pass_word)
                print '\n\n\n\n',user.id,user.user_id,'\n\n\n\n\n'
                session.add(user)
            user = request.db_session.query(User).filter_by(user_id=form_user_name).first()
            headers = remember(request,user.id)
            return HTTPFound(location=next_url, headers=headers)
    print '\n\n\n\n\n#########################under###########################\n\n\n\n\n\n'

    return dict(
        message=message,
        message2 = message2,
        url=request.route_url('login'),
        next_url=next_url,
        )
@view_config(route_name = 'logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('login')
    return HTTPFound(location=next_url, headers=headers)
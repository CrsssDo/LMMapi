from lib2to3.pgen2 import token
from fastapi_mail import MessageSchema, FastMail
from app.core.settings import Conf, settings
from fastapi import BackgroundTasks


conf = Conf()


def email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict, change_pass: bool = False , locking: bool = False):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html')
    fm = FastMail(conf)
    if change_pass == True:
        background_tasks.add_task(
            fm.send_message, message, template_name='password_email.html')
    elif locking == True:
        background_tasks.add_task(
            fm.send_message, message, template_name='notification_email.html')
    else:
        background_tasks.add_task(
            fm.send_message, message, template_name='email.html')


def send_email_background(backround_task: BackgroundTasks, email: str, password: str, name: str, by_admin: bool = False):
    if by_admin == True:
        return email_background(
            backround_task, 'Nghenongviet: Password has changed!', email,
         {
            'username': email,
            'password':password,
            'name': name,
            'title': 'Password',
            'sub_title' : 'Cập nhật mật khẩu mới',
            'message' : 'mật khẩu của bạn đã được thay đổi, vui lòng xem thông tin bên dưới.'
        })
    else:
        return email_background(
            backround_task, 'Welcome to Nghenongviet!', email,
         {
            'username': email,
            'password':password,
            'name': name,
            'title': 'Welcome',
            'sub_title' : 'Chào mừng thành viên mới.',
            'message' : 'chào mừng a/c đến với gia đình Nghề Nông Việt'
        })


def send_change_password_background(backround_task: BackgroundTasks, email: str, name: str, token: str, app: str):
    if app == 'admin':
        return email_background(
                backround_task, 'Nghenongviet: Change password request!', email,
            {
                'host': settings.server,
                'token': token, 
                'name': name,
                'title': 'Password',
                'sub_title' : 'Đổi mật khẩu mới',
                'message' : 'bạn đang yêu cầu đổi mật khẩu vui lòng click vào link bên dưới để đổi mật khẩu.'
            }, change_pass=True
            )
    if app == 'app':
        return email_background(
                backround_task, 'Nghenongviet: Change password request!', email,
            {
                'host': settings.app_server,
                'token': token, 
                'name': name,
                'title': 'Password',
                'sub_title' : 'Đổi mật khẩu mới',
                'message' : 'bạn đang yêu cầu đổi mật khẩu vui lòng click vào link bên dưới để đổi mật khẩu.'
            }, change_pass=True
            )


def send_email_lock_user(backround_task: BackgroundTasks, email: str, name: str, unactivated_reason: str,  activate: bool = True):
    if activate == True:
        status = 'mở khóa'
        color = '#009900'
    else:
        status = 'bị khóa'
        color = '#BB0000'

    return email_background(
            backround_task, 'Nghenongviet: Notifications!', email,
        {
            'title': 'Notifications',
            'name' : name,
            'sub_title' : 'Thông báo về tài khoản',
            'message' : 'tài khoản của bạn đã',
            'color' : color,
            'status' : status,
            'reason' : unactivated_reason
        }, locking=True
        )




# -*- encoding: utf-8 -*-
import sys
import models
import databases

sys.dont_write_bytecode = True
def select_all_user():
    session = databases.create_new_session()
    user_list = session.query(models.user).\
            filter(models.user.status == 'created').\
            all()
    if user_list == None:
        user_list = []
    return user_list

def create_user(user_name, user_mail):
    session = databases.create_new_session()
    user = models.user()
    user.name = user_name
    user.mail_address = user_mail
    user.status = 'created'
    session.add(user)
    session.commit()
    return 0

def select_user(user_id):
    session = databases.create_new_session()
    user = session.query(models.user).\
                filter(models.user.id == user_id).\
                first()           
    if user == None:
        user = ""
    return user

def update_user(user_id, user_name, user_mail, user_status):
    session = databases.create_new_session()
    user = session.query(models.user).\
                filter(models.user.id == user_id).\
                first()
    if user == None:
        return 1
    user.name = user_name
    user.mail_address = user_mail
    user.status = user_status
    session.commit()
    return 0

def delete_user(user_id):
    session = databases.create_new_session()
    user = session.query(models.user).\
                filter(models.user.id == user_id).\
                first()
    if user == None:
        return 1
    user.status = "deleted"
    session.commit()
    return 0

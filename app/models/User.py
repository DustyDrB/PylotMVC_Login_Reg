
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    def get_email(self, info):
        query = "SELECT * from users where email = '{}'".format(info)
        return self.db.query_db(query)

    def validate_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        redundancy_check = self.get_email(info['email'])

        if not info['first_name']:
            errors.append('Fields cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('First name must have at least two characters')
        if not info['last_name']:
            errors.append('Cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last name must have at least two characters')
        if not info['email']:
            errors.append('Fields cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid')
        if not info['password']:
            errors.append('Fields cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must contain at least 8 characters')
        elif info['password'] != info['confirm_pw']:
            errors.append('Passwords much match')
        if errors:
            print "/"*50
            print "Errors!"
            return {"status": False, "errors": errors}
        return {"status": True}

    def create_user(self, info):
        validity_check = self.validate_user(info)
        if validity_check['status']:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            query = "insert into users (first_name, last_name, pw_hash, email, created_at, updated_at) values ('{}', '{}', '{}', '{}', now(),now())".format(info['first_name'], info['last_name'], pw_hash,info['email'])
            self.db.query_db(query)
            self.db.query_db(query)
            return {'status': True, 'user':self.get_email(info['email'])}
        else:
            print "invalid"
            return validity_check
            
    # def get_user_by_id(self, id):
    #     id_query = "SELECT id, first_name, last_name, email FROM users WHERE id = :id"
    #     data = {'id' : id}
    #     result = self.db.query_db(id_query, data)

    def login_user(self, info):
        user = self.get_email(info['email'])
        if len(user)<0:
            if self.bcrypt.check_password_hash(user[0]['password'], info['password']):
                return {'status': True, 'user':user}
        return {'status': False}
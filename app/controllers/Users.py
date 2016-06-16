"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db

    def index(self):     
        return self.load_view('index.html')
    
    def create(self):
        # info = {
        #     "first_name": request.form['first_name'],
        #     "last_name": request.form['last_name'],
        #     "email": request.form['email'],
        #     "pw": request.form['pw'],
        #     "confirm_pw": request.form['confirm_pw']
        # }
        register_status = self.models['User'].create_user(request.form)
        print register_status
        # create_status=self.models['User'].validate_user(info)
        if register_status['status'] == True:
            session['user'] = register_status['user'][0]['id']
            # session['first_name'] = create_status['user']['first_name']
            # user = session['first_name']
            return self.load_view('success.html', user=register_status['user'][0])
        session['errors'] = register_status['errors']
        return redirect('/')
    def login(self):
        log_user = self.models['User'].login_user(request.form)
        print log_user

        if log_user['status'] == True:
            session['user'] = log_user['user'][0]['id']
            return self.load_view('success.html', user = log_user['user'][0])
        else:
            return redirect('/')
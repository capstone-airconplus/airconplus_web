import firebase_admin
from flask import Flask, render_template, request, session, flash
from firebase_admin import credentials
from firebase_admin import db, auth


app = Flask(__name__)
root_user = ""

try:
    cred = credentials.Certificate('./static/capstone-df6bb-firebase-adminsdk-4tkb4-d38a37bfae.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://capstone-df6bb.firebaseio.com/'
    })
except ValueError:
    print("valueError")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index', methods=['POST','GET'])
def index():
    try:
        login_id = request.form['login']
        login_pwd = request.form['password']

        print("#####")
        print(login_id)
        print(login_pwd)
        print("#####")

        global root_user
        root_user = login_id
        print("@@@@@@@global@@@@@@@@@@")
        print(root_user)
        print("@@@@@@@global@@@@@@@@@@")

        current_user = firebase_admin.auth.get_user_by_email(login_id)
        print(current_user.uid)

        uid = current_user.uid
        ref = db.reference(uid, url='https://capstone-df6bb.firebaseio.com/')
        indoor_hum = ref.child('indoor_hum').get()
        indoor_temp = ref.child('indoor_temp').get()
        outdoor_hum = ref.child('outdoor_fan_hum').get()
        outdoor_temp = ref.child('outdoor_fan_temp').get()


        return render_template('index.html', current_user=current_user.uid,
                               indoor_hum=indoor_hum, indoor_temp=indoor_temp,
                               outdoor_hum=outdoor_hum, outdoor_temp=outdoor_temp)
    except ValueError:
        print('valueError')
        return render_template('login_2.html')
    except KeyError:
        print('keyerror')

        global root_user
        login_id = root_user

        print("#####")
        print(login_id)
        print("#####")

        root_user = login_id
        print("@@@@@@@global@@@@@@@@@@")
        print(root_user)
        print("@@@@@@@global@@@@@@@@@@")

        current_user = firebase_admin.auth.get_user_by_email(login_id)
        print(current_user.uid)

        uid = current_user.uid
        ref = db.reference(uid, url='https://capstone-df6bb.firebaseio.com/')
        indoor_hum = ref.child('indoor_hum').get()
        indoor_temp = ref.child('indoor_temp').get()
        outdoor_hum = ref.child('outdoor_fan_hum').get()
        outdoor_temp = ref.child('outdoor_fan_temp').get()


        return render_template('index.html', current_user=current_user.uid,
                               indoor_hum=indoor_hum, indoor_temp=indoor_temp,
                               outdoor_hum=outdoor_hum, outdoor_temp=outdoor_temp)


    # if request.method == 'POST':
    #     page = auth.list_users()
    #     # print(page.users)
    #     while page:
    #         for user in page.users:
    #             print(user.email)
    #             if id is user.email:
    #                 print('User: ' + user.uid)
    #             # else:
    #                 # print("not registered user")
    #         page = page.get_next_page()


@app.route('/login')
def login():
    return render_template('login_2.html')


@app.route('/test')
def test():
    # ref = db.reference('/', url='https://capstone-df6bb.firebaseio.com/')
    # ref.set({
    #     'boxess':
    #         {
    #             'box001': {
    #                 'color': 'red',
    #                 'width': 1,
    #                 'height': 3,
    #                 'length': 2
    #             },
    #             'box002': {
    #                 'color': 'green',
    #                 'width': 1,
    #                 'height': 2,
    #                 'length': 3
    #             },
    #             'box003': {
    #                 'color': 'yellow',
    #                 'width': 3,
    #                 'height': 2,
    #                 'length': 1
    #             }
    #         }
    # })
    return render_template('test.html')


@app.route('/coming')
def coming():
    return render_template('coming-soon.html')


if __name__ == '__main__':
    app.run()

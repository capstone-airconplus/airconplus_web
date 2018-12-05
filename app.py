import firebase_admin
from flask import Flask, render_template, request, session, flash, jsonify
from firebase_admin import credentials
from firebase_admin import db, auth
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid
import json

app = Flask(__name__)
root_user = ""
uid = 'qi698BDarUgd2ERe1zLOr1GMx4D3'

try:
    cred = credentials.Certificate('./static/capstone-df6bb-firebase-adminsdk-4tkb4-d38a37bfae.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://capstone-df6bb.firebaseio.com/'
    })
    ref = db.reference(uid, url='https://capstone-df6bb.firebaseio.com/')
    ref.child('use_power').child("2018-12").child('2').update({
        'use':3.1,
        'reduction': 237
    })
    ref.child('use_power').child("2018-12").child('23').update({
        'use': 7.02,
        'reduction': 623
    })

except ValueError:
    print("valueError")


def fetch(login_id):
    global root_user
    root_user = login_id
    print("@@@@@@@global@@@@@@@@@@")
    print(root_user)
    print("@@@@@@@global@@@@@@@@@@")


@app.route('/signout')
def signout():
    global root_user
    root_user =''
    return render_template('login_2.html')


@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST' :
        login_id = request.form['login']
        login_pwd = request.form['password']

        print("#####")
        print(login_id)
        print(login_pwd)
        print("#####")

        global root_user
        root_user = login_id

    now = time.localtime()
    s = "%04d-%02d-%02d"%(now.tm_year, now.tm_mon, now.tm_mday)
    month = "%02d"%(now.tm_mon)
    print(s)

    try:
        current_user = firebase_admin.auth.get_user_by_email(root_user)
        uid = current_user.uid
        ref = db.reference(uid, url='https://capstone-df6bb.firebaseio.com/')
        indoor_hum = ref.child('indoor_hum').get()
        indoor_temp = ref.child('indoor_temp').get()
        outdoor_hum = ref.child('outdoor_fan_hum').get()
        outdoor_temp = ref.child('outdoor_fan_temp').get()
        on = ref.child('on').get()

        return render_template('index.html', current_user=current_user.uid,
                               indoor_hum=indoor_hum, indoor_temp=indoor_temp,
                               outdoor_hum=outdoor_hum, outdoor_temp=outdoor_temp,
                               time = s, month = month,on=on)
    except ValueError:
        print('valueError')
        return render_template('login_2.html')
    except KeyError:
        print('keyerror')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/refresh', methods=['POST'])
def refresh_func():
    indoor_hum = ref.child('indoor_hum').get()
    indoor_temp = ref.child('indoor_temp').get()
    outdoor_hum = ref.child('outdoor_fan_hum').get()
    outdoor_temp = ref.child('outdoor_fan_temp').get()
    current_month_price = ref.child('current_month_price').get()
    on = ref.child('on').get()
    current_month_price = format(current_month_price, ",")

    return json.dumps({'status':'OK', 'indoor_hum':indoor_hum,'indoor_temp':indoor_temp,
                       'outdoor_hum':outdoor_hum,'outdoor_temp':outdoor_temp, 'on':on,'current_month_price':current_month_price})


@app.route('/index', methods=['POST','GET'])
def index():
    if request.method == 'POST' :
        login_id = request.form['login']
        login_pwd = request.form['password']

        print("#####")
        print(login_id)
        print(login_pwd)
        print("#####")

        global root_user
        root_user = login_id

    now = time.localtime()
    s = "%04d-%02d-%02d"%(now.tm_year, now.tm_mon, now.tm_mday)
    month = "%02d"%(now.tm_mon)
    print(s)

    try:
        current_user = firebase_admin.auth.get_user_by_email(root_user)
        uid = current_user.uid
        ref = db.reference(uid, url='https://capstone-df6bb.firebaseio.com/')
        indoor_hum = ref.child('indoor_hum').get()
        indoor_temp = ref.child('indoor_temp').get()
        outdoor_hum = ref.child('outdoor_fan_hum').get()
        outdoor_temp = ref.child('outdoor_fan_temp').get()
        current_month_price = ref.child('current_month_price').get()
        on = ref.child('on').get()
        msg = ''
        # 3자리 마다 , 넣기
        current_month_price = format(current_month_price,",")

        if indoor_temp < 21:
            msg = '26도, 강풍, '
        elif 21 <= indoor_temp < 24:
            msg = '26도, 약풍, '
        elif 24 <= indoor_temp < 26:
            msg = '26도, 미풍, '
        elif 26 <= indoor_temp < 28:
            msg = '26도, 미풍, '
        elif 28 <= indoor_temp < 31:
            msg = '26도, 약풍, '
        elif indoor_temp >=31:
            msg = '26도, 강풍, '
        if indoor_hum >=70:
            msg = msg + "제습"
        else:
            if indoor_temp < 26:
                msg = msg + "난방"
            else:
                msg = msg + "냉방"

        return render_template('index.html', current_user=current_user.uid,
                               indoor_hum=indoor_hum, indoor_temp=indoor_temp,
                               outdoor_hum=outdoor_hum, outdoor_temp=outdoor_temp,
                               time = s, month = month,on=on,msg=msg,current_month_price=current_month_price)
    except ValueError:
        print('valueError')
        return render_template('login_2.html')
    except KeyError:
        print('keyerror')


def calculator(i, type):
    use_power = ref.child('use_power')
    data = use_power.get()
    print(data)

    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if type == 'use':
        for j in list(data.get(i).keys()):
            arr[int(j)-1] = data.get(i).get(j).get('use')
    else:
        for j in list(data.get(i).keys()):
            arr[int(j)-1] = data.get(i).get(j).get('reduction')

    return arr


@app.route('/use')
def use():
    return render_template('use_main.html')


@app.route('/use/<usename>')
def charttest(usename):

    try:
        randomString = uuid.uuid4()
        randomString2 = uuid.uuid4()

        strFile = './static/img/graph/'+str(randomString)+'.png'
        strFile2 = './static/img/graph/'+str(randomString2)+'.png'
        # strFile = './static/img/graph/test.png'
        # strFile2 = './static/img/graph/test2.png'

        plt.figure()
        plt.rcParams.update({'font.size': 8})

        if os.path.isfile(strFile):
            print('already exists')
            os.remove(strFile)
        if os.path.isfile(strFile2):
            print('already exists')
            os.remove(strFile2)

        print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        use = calculator(usename, 'use')
        print(use)

        print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        reduction = calculator(usename, 'reduction')
        print(reduction)

        t = np.array(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
             11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
             21, 22, 23, 24, 25, 26, 27, 28, 29, 30])

        y = np.array(use)

        plt.bar(t,y, color='r', width = 0.3, label='use')
        plt.xlabel('data')
        plt.ylabel('mount')
        plt.legend()

        plt.xticks(t, ('1','2','3','4','5','6','7','8','9','10',
                       '11','12','13','14','15','16','17','18','19','20',
                       '21','22','23','24','25','26','27','28','29','30','31'))

        plt.savefig(strFile)
        plt.clf()  # clear figure
        plt.cla()  # clear axes
        plt.close()

        power = ref.child('aircon_power').get()
        use_price = []
        use_month_price = 0

        reduction_price = []
        reduction_month_price = 0

        gap_reduction_use = 0

        for i in use:
            use_price.append(i * int(power))
            use_month_price = use_month_price + i

        for i in reduction:
            reduction_price.append(i)
            reduction_month_price = reduction_month_price + i

        print("(((((((((((((()))))))))))))))))))")
        print(power)
        print(use_price)
        use_month_price = int(use_month_price * int(power))
        gap_reduction_use = use_month_price - reduction_month_price

        y_ = np.array(use_price)
        y1_ = np.array(reduction)
        plt.figure()
        plt.bar(t, y_, color='r', width=0.3, label='before')
        plt.bar(t + 0.4, y1_, color='g', width=0.3, label='after')
        plt.xlabel(usename+'month')
        plt.ylabel('use power')
        plt.legend()

        plt.xticks(t, ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                       '21', '22', '23', '24', '25', '26', '27', '28', '29', '30','31'))

        plt.savefig(strFile2)
        plt.clf()  # clear figure
        plt.cla()  # clear axes
        plt.close()

        new_strFile = '.'+strFile
        new_strFile2 = '.' + strFile2

        now = time.localtime()
        month = "%02d" % (now.tm_mon)

        if month == usename.split('-')[1]:
            ref.update({
                'current_month_price':reduction_month_price
            })


        return render_template('use.html',name=usename,url=new_strFile,url2=new_strFile2,
                               use_month_price=use_month_price, reduction_month_price=reduction_month_price,
                               gap_reduction_use=gap_reduction_use)
    except AttributeError:
        return render_template('no_attribute.html', name=usename)


@app.route('/login')
def login():
    return render_template('login_2.html')


@app.route('/login_validation', methods=['POST'])
def login_valitation():
    login_id = request.form['login']
    login_pwd = request.form['password']

    print("#####")
    print(login_id)
    print(login_pwd)
    print("#####")

    page = auth.list_users()
    # print(page.users)
    while page:
        for user in page.users:
            print(user.email)
            if id is user.email:
                print('User: ' + user.uid)
                fetch(login_id)
                current_user = firebase_admin.auth.get_user_by_email(login_id)
                print(current_user.uid)
                return 'OK'
            else:
                print("not registered user")
        page = page.get_next_page()
    return 'NO'


@app.route('/samsung')
def samsung():
    return render_template('samsung.html')


@app.route('/winia')
def winia():
    return render_template('winia.html')


@app.route('/question')
def question():
    return render_template('question.html')


@app.route('/lg')
def lg():
    return render_template('lg.html')


if __name__ == '__main__':
    app.run()

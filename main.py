from flask import Flask, make_response, jsonify, request, Response, flash, redirect, url_for
from flask_login import LoginManager
import flask_login, flask, generate, json, requests, os, base64
from flask import render_template as real_render_template
from functools import partial
from db import *
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'waterdishow'
app.config['UPLOAD_FOLDER'] = './static/signature/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

error = showerror()
user_recept = show_recept()
render_template = partial(real_render_template, error=error, user_recept=user_recept)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

dataexport = 0

@app.route('/postdata', methods=["GET", "POST"])
def postdata():
    if request.method == 'POST':
        print("post")
        data = request.json
        now = datetime.now()
        sec = now.strftime("%S")
        json_object = json.dumps(data)
        with open("data.json", "w") as outfile:
            outfile.write(json_object)
        
        if int(sec) % 10 == 0 :
            client = MongoClient('localhost',27017)
            db = client.Water_di
            tb = db['report']
            tb.insert_many(data)
            print('insert to mogodb')
            dataexport = 0


        return "postdata succress"

@app.route('/dataapi', methods=["GET", "POST"])
def dataapi():
    js = open('data.json')
    data = json.load(js) 
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return jsonify(data)

########################### Function Login ###########################
login_manager = LoginManager()
login_manager.init_app(app)

users = users()

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if flask.request.form['check'] == "login":
            username = flask.request.form['username']
            if username in users and flask.request.form['password'] == users[username]['password']:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('index'))
            
            errorpassword = "True"
            return render_template('index.html', sweetalert=errorpassword)
        if flask.request.form['check'] == "register":
            Name = flask.request.form['registerName']
            username = flask.request.form['registerUsername']
            password = flask.request.form['registerPassword']
            password_again = flask.request.form['registerRepeatPassword']
            department = flask.request.form['DP']
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            Signature = request.files['file']
            if Signature.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if password == password_again:
                if Signature and allowed_file(Signature.filename):
                    Signature.save(os.path.join(app.config['UPLOAD_FOLDER'], Name+'.png'))
                    file = open(f'./static/signature/{Name}.png','rb').read()
                    file = base64.b64encode(file)
                    insert_Pre_User(username, Name, password, file, department)
                    waitforrecept = "True"
                    return render_template('index.html', waitforrecept=waitforrecept)
            else:
                notmatchpassword = "True"
                return render_template('index.html', notmatchpassword=notmatchpassword)

@app.route('/addmachine', methods=['GET', 'POST'])
@flask_login.login_required
def addmachine():
    if request.method == 'POST':
        if flask.request.form['add'] == "machine":
            id = flask.request.form['MachineId']
            ip = flask.request.form['MachineIp']
            port = flask.request.form['MachinePort']
            station = flask.request.form['inputOpMac']
            phase = flask.request.form['inputPhaseMac']
            Add_Machine(id, ip, port, station, phase)
            return flask.redirect(flask.url_for('addmachine'))
        if flask.request.form['add'] == "device":
            Machine = flask.request.form['inputMachineID']
            Site = flask.request.form['inputSite']
            Slot_Temp = flask.request.form['Slot_temp']
            Slot_Water= flask.request.form['Water']
            Add_Device(Machine, Site, Slot_Temp, Slot_Water)
            return flask.redirect(flask.url_for('addmachine'))
        if flask.request.form['add'] == "phase":
            OPadd = flask.request.form['OPadd']
            Phaseadd = flask.request.form['Phaseadd']
            Siteadd = flask.request.form['Siteadd']
            add_phase(OPadd, Phaseadd, Siteadd)
            return flask.redirect(flask.url_for('addmachine'))
        
    station = get_dropdown_values()
    machine_data = get_dropdown_values_machine()
    slot = dynamic_slot()
    edit_delete = show_machine()
    site = get_values_site()
    
    return render_template('add.html', station = station, machine_data = machine_data, slot = slot, edit_delete = edit_delete, site = site)

@app.route('/delete', methods=['GET', 'POST'])
@flask_login.login_required
def delete():
    Site = request.args.get('Site')
    delete_device(Site)
    return flask.redirect(flask.url_for('addmachine'))

@app.route('/edit', methods=['GET', 'POST'])
@flask_login.login_required
def edit():
    Site = request.args.get('edit')
    edit = edit_machine_device(Site)
    station = get_dropdown_values()
    slot = dynamic_slot()
    return render_template('edit_device.html', edit = edit, station = station, slot = slot)

@app.route('/blank')
@flask_login.login_required
def blank():
    return render_template('blank.html')

@app.route('/edit_value', methods=['GET', 'POST'])
@flask_login.login_required
def edit_value():
    if request.method == 'POST':
        result = request.form.to_dict()
        values = result.values()
        values_Site = list(values)
        print(values_Site)
        Site = request.form.get(values_Site[0])
        Ip = request.form.get("Ip"+values_Site[0])
        Port = request.form.get("Port"+values_Site[0])
        Station = request.form.get("inputOP")
        Phase = request.form.get("Phase"+values_Site[0])
        Slot_Water = request.form.get("Slot_Water"+values_Site[0])
        Slot_Temp = request.form.get("Slot_Temp"+values_Site[0])
        if Slot_Water is None and Slot_Temp is None:
            edit = edit_machine_device(Site)
            Slot_Water = edit[0]['Slot_Water']
            Slot_Temp = edit[0]['Slot_Temp']
        print(Site, Ip, Port, Station, Phase, Slot_Water, Slot_Temp)
        edit_device(Ip, Port, Station, Phase, Slot_Water, Slot_Temp, Site)
    return flask.redirect(flask.url_for('blank'))
        
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
    
@app.route('/setup')
@flask_login.login_required
def setup():
    setup = setupMachine()
    show_machine = machine_DropDown_setup()
    return render_template('setup.html', setup = setup, show_machine = show_machine)

@app.route('/find_setup')
@flask_login.login_required
def find_setup():
    selectionMachine = request.args.get('selectionMachine')
    setup = show_site_machine(selectionMachine)
    show_machine = machine_DropDown_setup()
    return render_template('setup.html', setup = setup, show_machine = show_machine, selectionMachine=selectionMachine)

@app.route('/confirm_reject', methods=['GET', 'POST'])
@flask_login.login_required
def confirm_reject():
    if request.args.get('confirm'):
        user_confirm = request.args.get('confirm')
        confirm_User(user_confirm)
        return flask.redirect(flask.url_for('index'))
    if request.args.get('reject'):
        user_reject = request.args.get('reject')
        reject_User(user_reject)        
        return flask.redirect(flask.url_for('index'))
    return flask.redirect(flask.url_for('index'))

@app.route('/change_setup' , methods=['GET', 'POST'])
@flask_login.login_required
def change_setup():
    setup = setupMachine()
    name_site = []
    for i in setup:
        name_site.append(i['Site'])
    for j in range(len(name_site)):
        site = request.args.get(f'{name_site[j]}')
        low_water = request.args.get(f'Low_Water_{name_site[j]}')
        high_water = request.args.get(f'High_Water_{name_site[j]}')
        plus_water = request.args.get(f'Plus_Water_{name_site[j]}')
        minus_water = request.args.get(f'Minus_Water_{name_site[j]}')
        plus_temp = request.args.get(f'Plus_Temp_{name_site[j]}')
        minus_temp = request.args.get(f'Minus_Temp_{name_site[j]}')
        update_setup(site, low_water, high_water, plus_water, minus_water, plus_temp, minus_temp)
    return flask.redirect(flask.url_for('setup'))

@app.route('/sendfile', methods=['POST', 'GET'])
@flask_login.login_required
def sendfile():
   template = './static/document/ใบขอใช้บริการระบบงานคอมพิวเตอร์.docx'
   signature = './static/signature/pramote.png'
   order_id = request.form['order_id']
   invoice = {
        'invoice_no': request.form['order_id'],
        'detail' : request.form['detail'],
        'order_name' : request.form['order_name'],
        'name': request.form['name'],
        'repair_name': request.form['repair_name'],
        'total': request.form['price'],
    
    }
   print(invoice)
   document = generate.from_template(template, signature, invoice)
   document.seek(0)

   return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename=f'ใบเสร็จที่ {order_id}.docx')

########################### End Function Login ###########################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line', methods=['GET', 'POST'])
def line():
    if request.method == 'POST':
        if request.values["selection_day"] != "0":
            day = flask.request.form['selection_day']
            month = flask.request.form['selection_month']
            year = flask.request.form['year']
            report = di_report_custom_day(day, month, year)
            table = report_line_day(day, month ,year)
            column = somlinecolumn()
            customday = "True"
            return render_template('line.html', report = report, table = table, column = column, customday = customday)
        month = flask.request.form['selection_month']
        year = flask.request.form['year']
        report = di_report_custom(month, year)
        table = report_line_month(month ,year)
        column = somlinecolumn()
        custom = "True"
        return render_template('line.html', report = report, table = table, column = column, custom = custom)
    report = di_report_now()
    table = reportsomline()
    column = somlinecolumn()
    now = "True"
    return render_template('line.html', report = report, table = table, column = column, now = now)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/alert')
def alert():
    report = error_report()
    return render_template('alert.html', report = report)

@app.route('/trendDi')
def trendDi():
    P4 = trend_DI_P4()
    P5 = trend_DI_P5()
    P9 = trend_DI_P9()
    print(P4)
    return render_template('TrendDiwater.html', P4 = P4, P5 = P5, P9 = P9)

@app.route('/trendDi-chart')
def trendDiChart():
    P4 = trend_DI_P4()
    P5 = trend_DI_P5()
    P9 = trend_DI_P9()
    print(P4)
    return render_template('trend-di-chart.html', P4 = P4, P5 = P5, P9 = P9)

@app.route('/document')
def document():
    return render_template('document.html')

@app.route('/status-carbon-resin')
def statusCR():
    return render_template('status-carbon-resin.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
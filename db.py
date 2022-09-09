import pymysql

import itertools

########################### Function DB ###########################

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_di',
        user='root',
        password='',
        charset='utf8',
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    
###################################### Line notify ######################################################
import requests
url = 'https://notify-api.line.me/api/notify'
token = '1ynH4ehbVZZK3ngffNqBjnZVdnU5gKtNIYLu14IOLD8'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
###########################################################################################################    
    
def showerror():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            WHERE di_error.Date = CURDATE()"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    # requests.post(url, headers=headers, data = {'message':"dfa"})
    return error

def error_report():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            ORDER BY di_error.Date DESC"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error

def show_recept():
    connection = getConnection()
    sql_recept = "SELECT Name from Pre_User"
    cursor = connection.cursor()
    cursor.execute(sql_recept)
    user = cursor.fetchall()
    return user

def Add_Machine(Machine, IP, PORT, Station, Phase):
    connection = getConnection()
    insert_Machine_Master = "INSERT INTO Machine_Master(Machine, Ip, Port) VALUES('%s', '%s', '%s')" % (Machine, IP, PORT)
    insert_Machine_Station = "INSERT INTO Machine_Station(Station, Phase) VALUES('%s', '%s')" % (Station, Phase)
    insert_Machine = "INSERT INTO Machine(Machine) VALUES('%s')" % (Machine)
    cursor = connection.cursor()
    cursor.execute(insert_Machine_Master)
    cursor.execute(insert_Machine_Station)
    cursor.execute(insert_Machine)
    connection.commit()

def Add_Device(Machine, Site, Slot_Temp, Slot_Water):
    connection = getConnection()
    cursor = connection.cursor()
    insert_Machine_Data = "INSERT INTO Machine_Data(Site, Machine, Slot_Temp, Slot_Water) VALUES('%s', '%s', '%s', '%s')" % (Site, Machine, Slot_Temp, Slot_Water)
    cursor.execute(insert_Machine_Data)
    connection.commit()
    
def Di_error(Machine, Detail, Date):
    connection = getConnection()
    insert_error = "INSERT INTO DI_Error(Machine, Detail, Date) VALUES('%s', '%s', '%s')" % (Machine, Detail, Date)
    cursor = connection.cursor()
    cursor.execute(insert_error)
    connection.commit()
    
def DI_Report(Station, Phase, Site, Temp, Water, Date, Time, TimeStamp):
    connection = getConnection()
    insert_report = """INSERT INTO DI_Report(Station, Phase, Site, Temp, Water, Date, Time, TimeStamp) 
                        VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (Station, Phase, Site, Temp, Water, Date, Time, TimeStamp)
    cursor = connection.cursor()
    cursor.execute(insert_report)
    connection.commit()
    
def log_status(Machine, Status, Datetime):
    connection = getConnection()
    insert_error = "INSERT INTO Log_Status(Machine, Status, DateTime) VALUES('%s', '%s', '%s')" % (Machine, Status, Datetime)
    cursor = connection.cursor()
    cursor.execute(insert_error)
    connection.commit()
    
def add_phase(OP, Phase, Site):
    op = []
    OP = OP
    Phase = Phase
    connection = getConnection()
    cursor = connection.cursor()
    select_op = "select * from OP"
    cursor.execute(select_op)
    data = cursor.fetchall()
    for row in data:
        op.append(row["OP"])
    if OP in op:
        insert_site = "INSERT INTO Off_Set VALUES('%s', 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'N', 'N')" % (Site)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_phase)
        connection.commit()
    else:
        insert_site = "INSERT INTO Off_Set VALUES('%s', 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'N', 'N')" % (Site)
        insert_op = "INSERT INTO OP(OP) VALUES('%s')" % (OP)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_op)
        cursor.execute(insert_phase)
        connection.commit()
        
def dynamicop():
    op = []
    connection = getConnection()
    cursor = connection.cursor()
    select_op = "select * from OP"
    cursor.execute(select_op)
    data = cursor.fetchall()
    for row in range(len(data)):
        op.append(data[row]["OP"])
    return op
    
def dynamicphase(op_id):
    ph = []
    connection = getConnection()
    cursor = connection.cursor()
    select_phase = "select * from phase where OP = '%s'" % (op_id)
    cursor.execute(select_phase)
    data = cursor.fetchall()
    for row in range(len(data)):
        ph.append(data[row]["Phase"])
    return ph
        
def get_dropdown_values():
    op = dynamicop()
    myDict = {}
    for station in op:
    
        key = station
        op_id = station
        
        dataphase = dynamicphase(op_id)
        lst_p = []
        for phase in dataphase:
            if phase not in lst_p:
                lst_p.append( phase )
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    return class_entry_relations

def dynamic_machine(OP):
    machine = []
    connection = getConnection()
    cursor = connection.cursor()
    select_machine = """SELECT machine.Machine, machine_station.Phase
                        FROM machine
                        INNER JOIN machine_station ON machine_station.ID=machine.ID and machine_station.Station='%s'""" % (OP)
    cursor.execute(select_machine)
    data = cursor.fetchall()
    for row in range(len(data)):
        machine.append(data[row]["Machine"])
    return machine
    
def dynamic_op_machine():
    op = []
    connection = getConnection()
    cursor = connection.cursor()
    select_op = "select * from OP"
    cursor.execute(select_op)
    data = cursor.fetchall()
    for row in range(len(data)):
        op.append(data[row]["OP"])
    return op   
    
def get_dropdown_values_machine():
    OP = dynamic_op_machine()
    myDict = {}
    for station in OP:
    
        key = station
        op = station
        
        dataphase = dynamic_machine(op)
        lst_p = []
        for phase in dataphase:
            lst_p.append( phase )
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    return class_entry_relations

def dynamic_slot():
    machine = []
    slot = []
    connection = getConnection()
    cursor = connection.cursor()
    select_slot = "select * from Machine_Data"
    cursor.execute(select_slot)
    data = cursor.fetchall()
    for row in range(len(data)):
        if data[row]["Machine"] not in machine:
            machine.append(data[row]["Machine"])
        if data[row]["Machine"] == "001":
            if data[row]["Slot_Water"] and data[row]["Slot_Temp"] not in slot:
                slot.clear()
                slot.append([data[row]["Slot_Water"], data[row]["Slot_Temp"]])
                finalslot001 = list(itertools.chain.from_iterable(slot))
        # if data[row]["Machine"] == "002":
        #     if data[row]["Slot_Water"] and data[row]["Slot_Temp"] not in slot:
        #         slot.append([data[row]["Slot_Water"], data[row]["Slot_Temp"]])
        #         finalslot002 = list(itertools.chain.from_iterable(slot))
    slot.clear()
    # slot.append(finalslot002)
    slot.append(finalslot001)
    dictionary = dict(zip(machine, slot))
    return dictionary

def show_machine():
    connection = getConnection()
    cursor = connection.cursor()
    show_machine = """SELECT machine_master.Ip, 
                            machine_master.Port,
                            machine_station.Station, 
                            machine_station.Phase,
                            machine_data.Site,
                            machine_data.Slot_Water,
                            machine_data.Slot_Temp,
                            machine_data.Machine
                        FROM machine_master
                        INNER JOIN machine ON machine_master.Machine = machine.Machine
                        INNER JOIN machine_station ON machine.ID = machine_station.ID
                        INNER JOIN machine_data ON machine_data.Machine = machine_master.Machine"""
    cursor.execute(show_machine)
    data = cursor.fetchall()
    return data

def setupMachine():
    connection = getConnection()
    cursor = connection.cursor()
    show_setup = """SELECT off_set.Site, off_set.Low_Water, off_set.Hight_Water, off_set.Plus_Water, off_set.Minus_Water, 
                    off_set.Low_Temp, off_set.Hight_Temp, off_set.Plus_Temp, off_set.Minus_Temp
                     FROM off_set
                     JOIN machine_data ON machine_data.Site=off_set.Site"""
    cursor.execute(show_setup)
    data = cursor.fetchall()
    return data

def dynamic_phase_site():
    phase = []
    connection = getConnection()
    cursor = connection.cursor()
    select_phase = "select * from phase"
    cursor.execute(select_phase)
    data = cursor.fetchall()
    for row in range(len(data)):
        phase.append(data[row]["Phase"])
    return phase
    
def dynamic_site_phase(phase):
    site = []
    connection = getConnection()
    cursor = connection.cursor()
    select_site = "select * from phase where phase = '%s'" % (phase)
    cursor.execute(select_site)
    data = cursor.fetchall()
    for row in range(len(data)):
        site.append(data[row]["Site"])
    return site
        
def get_values_site():
    phase = dynamic_phase_site()
    myDict = {}
    for site in phase:
    
        key = site
        phase_id = site
        
        data_site = dynamic_site_phase(phase_id)
        lst_p = []
        for phase in data_site:
            if phase not in lst_p:
                lst_p.append( phase )
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    print(class_entry_relations)
    
    return class_entry_relations

def find_users():
    users = []
    connection = getConnection()
    cursor = connection.cursor()
    find_users = "select * from user"
    cursor.execute(find_users)
    data = cursor.fetchall()
    for row in range(len(data)):
        users.append(data[row]["Username"])
    return users

def find_password(user):
    password = []
    connection = getConnection()
    cursor = connection.cursor()
    find_password = "select * from user where Username = '%s'" % (user)
    cursor.execute(find_password)
    data = cursor.fetchall()
    for row in range(len(data)):
        password.append(data[row]["Password"])
    return password

def users():
    users = find_users()
    myDict = {}
    for username in users:
        
        key = username
        user = username
        
        lst_p = {}
        password = find_password(user)
        for word in password:
            lst_p["password"] = (word)
        myDict[key] = lst_p
    class_entry_relations = myDict
    return class_entry_relations

def insert_Pre_User(username, Name, password, Signature, Department):
    connection = getConnection()
    cursor = connection.cursor()
    insert_Pre_User = "INSERT INTO pre_user VALUES ('%s','%s','%s','%s','%s')" % (username, Name, password, Signature, Department)
    cursor.execute(insert_Pre_User)
    connection.commit()
    
def confirm_User(Name):
    connection = getConnection()
    cursor = connection.cursor()
    add_pre_user = "INSERT INTO User SELECT Username, Name, Password, Signature, DepartmentID FROM Pre_User WHERE Name='%s'" % (Name)
    delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
    cursor.execute(add_pre_user)
    cursor.execute(delete_pre_user)
    connection.commit()
        
def reject_User(Name):
    connection = getConnection()
    cursor = connection.cursor()
    delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
    cursor.execute(delete_pre_user)
    connection.commit()
    
def show_site_machine(Machine):
    connection = getConnection()
    cursor = connection.cursor()
    show_site = f"""SELECT off_set.Site, off_set.Low_Water, off_set.Hight_Water, off_set.Plus_Water, off_set.Minus_Water,
                    off_set.Low_Temp, off_set.Hight_Temp , off_set.Plus_Temp, off_set.Minus_Temp FROM off_set
                    INNER JOIN machine_data on machine_data.Site = off_set.Site
                    WHERE Machine = '{Machine}'"""
    cursor.execute(show_site)
    data = cursor.fetchall()
    print(data)
    return data

def find_machine():
    machine = []
    connection = getConnection()
    cursor = connection.cursor()
    find_machine = "select * from machine_master"
    cursor.execute(find_machine)
    data = cursor.fetchall()
    for row in range(len(data)):
        machine.append(data[row]["Machine"])
    return machine
    
def machine_DropDown_setup():
    Machine = find_machine()
    myDict = {}
    for result in Machine:
        
        key = result
        result = result
        myDict[key] = result
        
    class_entry_relations = myDict
    return class_entry_relations

def update_setup(Site, low_water, high_water, plus_water, minus_water, plus_temp, minus_temp):
    connection = getConnection()
    cursor = connection.cursor()
    update_setup = f"""UPDATE off_set SET Low_Water='{low_water}',Hight_Water='{high_water}',Plus_Water='{plus_water}',
    Minus_Water='{minus_water}', Plus_Temp='{plus_temp}',Minus_Temp='{minus_temp}' WHERE Site = '{Site}'"""
    cursor.execute(update_setup)
    connection.commit()
    
def delete_device(Site):
    connection = getConnection()
    sql = f"DELETE FROM machine_data WHERE Site='{Site}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    
def edit_device(Ip, Port, Station, Phase, Slot_Water, Slot_Temp, Site):
    connection = getConnection()
    sql = f"""UPDATE machine_master
                JOIN machine ON machine_master.Machine = machine.Machine
                JOIN machine_station ON machine.ID = machine_station.ID
                JOIN machine_data ON machine_data.Machine = machine_master.Machine
                SET machine_master.Ip = '{Ip}', machine_master.Port = '{Port}', machine_station.Station = '{Station}',
                machine_station.Phase = '{Phase}', machine_data.Slot_Water='{Slot_Water}', machine_data.Slot_Temp='{Slot_Temp}'
                WHERE machine_data.Site = '{Site}'"""
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    
def edit_machine_device(Site):
    connection = getConnection()
    cursor = connection.cursor()
    edit_machine_device = f"""SELECT machine_master.Ip, 
                            machine_master.Port,
                            machine_station.Station, 
                            machine_station.Phase,
                            machine_data.Site,
                            machine_data.Slot_Water,
                            machine_data.Slot_Temp,
                            machine_data.Machine
                        FROM machine_master
                        INNER JOIN machine ON machine_master.Machine = machine.Machine
                        INNER JOIN machine_station ON machine.ID = machine_station.ID
                        INNER JOIN machine_data ON machine_data.Machine = machine_master.Machine
                        Where machine_data.Site = '{Site}'"""
    cursor.execute(edit_machine_device)
    data = cursor.fetchall()
    return data

def di_report():
    connection = getConnection()
    cursor = connection.cursor()
    di_report = "SELECT Date, Phase, Site, Water, Temp FROM di_report ORDER BY Date DESC, Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def di_report_now():
    connection = getConnection()
    cursor = connection.cursor()
    di_report = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report ORDER BY Date DESC, Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def di_report_custom(month, year):
    connection = getConnection()
    cursor = connection.cursor()
    di_report = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE MONTH(Date) = {month} and YEAR(Date) = {year} ORDER BY Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def di_report_custom_day(Day, month, year):
    connection = getConnection()
    cursor = connection.cursor()
    di_report = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE DAY(date) = {Day} and MONTH(Date) = {month} and YEAR(Date) = {year} ORDER BY Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def trend_DI_P4():
    connection = getConnection()
    cursor = connection.cursor()
    trend_DI_P4 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 4' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P4)
    data = cursor.fetchall()
    return data

def trend_DI_P5():
    connection = getConnection()
    cursor = connection.cursor()
    trend_DI_P5 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 5' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P5)
    data = cursor.fetchall()
    return data

def trend_DI_P9():
    connection = getConnection()
    cursor = connection.cursor()
    trend_DI_P9 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 9' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P9)
    data = cursor.fetchall()
    return data

def reportsomline():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT di_report.Time,
    MAX(CASE WHEN di_report.Site = "HC-6" THEN di_report.Water END) "HC-6",
    MAX(CASE WHEN di_report.Site = "HC-3" THEN di_report.Water END) "HC-3",
    MAX(CASE WHEN di_report.Site = "Fisa 2" THEN di_report.Water END) "Fisa 2",
    MAX(CASE WHEN di_report.Site = "Fisa 3" THEN di_report.Water END) "Fisa 3",
    MAX(CASE WHEN di_report.Site = "AI" THEN di_report.Water END) "AI",
    MAX(CASE WHEN di_report.Site = "Fisa 4" THEN di_report.Water END) "Fisa 4",
    MAX(CASE WHEN di_report.Site = "HC-4" THEN di_report.Water END) "HC-4",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 1" THEN di_report.Water END) "HC-5 Station 1",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 2" THEN di_report.Water END) "HC-5 Station 2",
    MAX(CASE WHEN di_report.Site = "L13" THEN di_report.Water END) "L13",
    MAX(CASE WHEN di_report.Site = "L14" THEN di_report.Water END) "L14",
    MAX(CASE WHEN di_report.Site = "L15 Station 1" THEN di_report.Water END) "L15 Station 1",
    MAX(CASE WHEN di_report.Site = "L15 Station 2" THEN di_report.Water END) "L15 Station 2",
    MAX(CASE WHEN di_report.Site = "ROBOT" THEN di_report.Water END) "ROBOT"
    FROM di_report
    WHERE Date = CURDATE()
    GROUP BY di_report.Time
    ORDER BY di_report.Date ASC, di_report.Time ASC
    LIMIT 24"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

def somlinecolumn():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT * from Off_set"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    return data

def report_line_month(month, year):
    connection = getConnection()
    cursor = connection.cursor()
    datatable = f"""SELECT di_report.Date,
    MAX(CASE WHEN di_report.Site = "HC-6" THEN di_report.Water END) "HC-6",
    MAX(CASE WHEN di_report.Site = "HC-3" THEN di_report.Water END) "HC-3",
    MAX(CASE WHEN di_report.Site = "Fisa 2" THEN di_report.Water END) "Fisa 2",
    MAX(CASE WHEN di_report.Site = "Fisa 3" THEN di_report.Water END) "Fisa 3",
    MAX(CASE WHEN di_report.Site = "AI" THEN di_report.Water END) "AI",
    MAX(CASE WHEN di_report.Site = "Fisa 4" THEN di_report.Water END) "Fisa 4",
    MAX(CASE WHEN di_report.Site = "HC-4" THEN di_report.Water END) "HC-4",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 1" THEN di_report.Water END) "HC-5 Station 1",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 2" THEN di_report.Water END) "HC-5 Station 2",
    MAX(CASE WHEN di_report.Site = "L13" THEN di_report.Water END) "L13",
    MAX(CASE WHEN di_report.Site = "L14" THEN di_report.Water END) "L14",
    MAX(CASE WHEN di_report.Site = "L15 Station 1" THEN di_report.Water END) "L15 Station 1",
    MAX(CASE WHEN di_report.Site = "L15 Station 2" THEN di_report.Water END) "L15 Station 2",
    MAX(CASE WHEN di_report.Site = "ROBOT" THEN di_report.Water END) "ROBOT"
    FROM di_report
    WHERE MONTH(Date) = {month} and YEAR(Date) = {year}
    GROUP BY di_report.Date
    ORDER BY di_report.Date ASC, di_report.Time ASC"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

def report_line_day(Day,month, year):
    connection = getConnection()
    cursor = connection.cursor()
    datatable = f"""SELECT di_report.Time,
    MAX(CASE WHEN di_report.Site = "HC-6" THEN di_report.Water END) "HC-6",
    MAX(CASE WHEN di_report.Site = "HC-3" THEN di_report.Water END) "HC-3",
    MAX(CASE WHEN di_report.Site = "Fisa 2" THEN di_report.Water END) "Fisa 2",
    MAX(CASE WHEN di_report.Site = "Fisa 3" THEN di_report.Water END) "Fisa 3",
    MAX(CASE WHEN di_report.Site = "AI" THEN di_report.Water END) "AI",
    MAX(CASE WHEN di_report.Site = "Fisa 4" THEN di_report.Water END) "Fisa 4",
    MAX(CASE WHEN di_report.Site = "HC-4" THEN di_report.Water END) "HC-4",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 1" THEN di_report.Water END) "HC-5 Station 1",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 2" THEN di_report.Water END) "HC-5 Station 2",
    MAX(CASE WHEN di_report.Site = "L13" THEN di_report.Water END) "L13",
    MAX(CASE WHEN di_report.Site = "L14" THEN di_report.Water END) "L14",
    MAX(CASE WHEN di_report.Site = "L15 Station 1" THEN di_report.Water END) "L15 Station 1",
    MAX(CASE WHEN di_report.Site = "L15 Station 2" THEN di_report.Water END) "L15 Station 2",
    MAX(CASE WHEN di_report.Site = "ROBOT" THEN di_report.Water END) "ROBOT"
    FROM di_report
    WHERE DAY(date) = {Day} and MONTH(Date) = {month} and YEAR(Date) = {year}
    GROUP BY di_report.Time
    ORDER BY di_report.Date ASC, di_report.Time ASC"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

########################### End Function DB ###########################

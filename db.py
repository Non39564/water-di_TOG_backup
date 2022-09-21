from xml.dom.minidom import Document
import pymysql

import itertools

########################### Function DB ###########################

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_test',
        user='root',
        password='',
        charset='utf8',
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit = True
    )
    
def showerror():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            WHERE di_error.Date = CURDATE()
            """
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error

def error_report():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            ORDER BY di_error.Date DESC"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error

def error_report_find(startdate, enddate):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            ORDER BY di_error.Date DESC, di_error.Time DESC"""
    else :
        sql = f"""SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Date BETWEEN '{startdate}' and '{enddate}'
                ORDER BY di_error.Date DESC"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error

def get_error_name():
    Name = []
    connection = getConnection()
    sql = """SELECT machine_data.Site
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            GROUP BY machine_data.Site"""
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        Name.append(d['Site'])
    return Name



#########################################################################################################################################
def error_report_limit(startdate, enddate, row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                ORDER BY di_error.Date DESC limit %s,%s""" % (row, rowperpage)
    else :
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Date BETWEEN '%s' and '%s'
                ORDER BY di_error.Date DESC limit %s,%s""" % (startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error


def filter_table(startdate, enddate, likeString):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Site LIKE '%s' OR machine_station.Phase LIKE '%s' OR machine_station.Station LIKE '%s'
                ORDER BY di_error.Date DESC""" % (likeString, likeString, likeString)
    else :
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Site LIKE '%s' OR machine_station.Phase LIKE '%s' OR machine_station.Station LIKE '%s' 
                and di_error.Date BETWEEN '%s' and '%s'
                ORDER BY di_error.Date DESC""" % (likeString, likeString, likeString, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def filter_table_limit(startdate,enddate,likeString,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Site LIKE '%s' OR machine_station.Phase LIKE '%s' OR machine_station.Station LIKE '%s'
                ORDER BY di_error.Date DESC limit %s, %s""" % (likeString, likeString, likeString, row, rowperpage)
    else :
        sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail, di_error.Date, di_error.Time
                FROM machine_station
                JOIN machine ON machine_station.ID = machine.ID
                JOIN machine_data ON machine_data.Machine = machine.Machine
                JOIN di_error ON di_error.Site = machine_data.Site
                WHERE di_error.Site LIKE '%s' OR machine_station.Phase LIKE '%s' OR machine_station.Station LIKE '%s'
                and di_error.Date BETWEEN '%s' and '%s'
                ORDER BY di_error.Date DESC limit %s, %s""" % (likeString, likeString, likeString, startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
###################################################################################################################################
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
        insert_maintain_data = "INSERT INTO Maintain_data VALUES('%s', 'admin', 0)" % (Site)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_maintain_data)
        cursor.execute(insert_phase)
        connection.commit()
    else:
        insert_site = "INSERT INTO Off_Set VALUES('%s', 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'N', 'N')" % (Site)
        insert_maintain_data = "INSERT INTO Maintain_data VALUES('%s', 'admin, 0)" % (Site)
        insert_op = "INSERT INTO OP(OP) VALUES('%s')" % (OP)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_maintain_data)
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
                # slot.clear()
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
                            phase.OP, 
                            phase.Phase,
                            machine_data.Site,
                            machine_data.Slot_Water,
                            machine_data.Slot_Temp,
                            machine_data.Machine
                        FROM machine_master
                        INNER JOIN machine ON machine_master.Machine = machine.Machine
                        INNER JOIN machine_station ON machine.ID = machine_station.ID
                        INNER JOIN machine_data ON machine_data.Machine = machine_master.Machine
                        INNER JOIN phase ON machine_data.Site = phase.Site"""
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
    insert_Pre_User = "INSERT INTO pre_user(Username, Name, Password, Signature, DepartmentID) VALUES (%s,%s,%s,%s,%s)"
    args = (username, Name, password, Signature, Department)
    cursor.execute(insert_Pre_User, args)
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
                JOIN phase on phase.Site = machine_data.Site
                SET machine_master.Ip = '{Ip}', machine_master.Port = '{Port}', phase.OP = '{Station}',
                phase.Phase = '{Phase}', machine_data.Slot_Water='{Slot_Water}', machine_data.Slot_Temp='{Slot_Temp}'
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

def di_report_now(startdate, enddate):
    connection = getConnection()
    cursor = connection.cursor()
    if startdate == '' or enddate == '':
        di_report = "SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report ORDER BY Date DESC, Time DESC"
    else :
        di_report = f"SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report WHERE Date BETWEEN '{startdate}' and '{enddate}' ORDER BY Date DESC, Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def report_Site_Name():
    Name = []
    connection = getConnection()
    sql = 'SELECT Site FROM di_report GROUP BY Site'
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        Name.append(d['Site'])
    return Name



###############################################################################################################################
def di_report_limit(startdate, enddate, row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report ORDER BY Date DESC, Time DESC limit %s,%s""" % (row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report WHERE Date BETWEEN '%s' and '%s' ORDER BY Date DESC, Time DESC limit %s,%s""" % (startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error


def di_report_filter_table(startdate, enddate, likeString):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report 
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report 
                WHERE Date BETWEEN '%s' and '%s' and Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s'
                ORDER BY Date DESC, Time DESC
                """ % (startdate, enddate, likeString, likeString, likeString)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def di_report_filter_table_limit(startdate, enddate, likeString,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp, State FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage, startdate, enddate)
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
#############################################################################################################################################
def di_report_custom(date):
    connection = getConnection()
    cursor = connection.cursor()
    di_report = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Date = '{date}' ORDER BY Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    return data

def trend_DI_P4(startdate, enddate):
    connection = getConnection()
    cursor = connection.cursor()
    if startdate == '' or enddate == '':
        trend_DI_P4 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 4' ORDER BY Date DESC, Time DESC"
    else :
        trend_DI_P4 = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 4' and Date BETWEEN '{startdate}' and '{enddate}' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P4)
    data = cursor.fetchall()
    return data

def get_trendDI_Site(phase):
    Name = []
    connection = getConnection()
    sql = f"SELECT Site FROM di_report WHERE Phase='Phase {phase}' GROUP BY Site"
    print(phase)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        Name.append(d['Site'])
    return Name
###############################################################################################################################

def trend_DI_P4_limit(startdate, enddate, row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 4' ORDER BY Date DESC, Time DESC limit %s,%s""" % (row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 4' and Date BETWEEN '%s' and '%s' ORDER BY Date DESC, Time DESC limit %s,%s""" % (startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error


def trend_DI_P4_filter_table(startdate ,enddate ,likeString):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 4'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 4' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def trend_DI_P4_filter_table_limit(startdate, enddate, likeString,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 4'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 4' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

###############################################################################################################################

def trend_DI_P5(startdate,enddate):
    connection = getConnection()
    cursor = connection.cursor()
    if startdate == '' or enddate == '':
        trend_DI_P5 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 5' ORDER BY Date DESC, Time DESC"
    else :
        trend_DI_P5 = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 5' and Date BETWEEN '{startdate}' and '{enddate}' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P5)
    data = cursor.fetchall()
    return data

###############################################################################################################################

def trend_DI_P5_limit(startdate,enddate,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 5' ORDER BY Date DESC, Time DESC limit %s,%s""" % (row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 5' and Date BETWEEN '%s' and '%s' ORDER BY Date DESC, Time DESC limit %s,%s""" % (startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error


def trend_DI_P5_filter_table(startdate,enddate,likeString):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 5'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 5' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def trend_DI_P5_filter_table_limit(startdate,enddate,likeString,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 5'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 5' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

###############################################################################################################################

def trend_DI_P9(startdate,enddate):
    connection = getConnection()
    cursor = connection.cursor()
    if startdate == '' or enddate == '':
        trend_DI_P9 = "SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 9' ORDER BY Date DESC, Time DESC"
    else :
        trend_DI_P9 = f"SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 9' and Date BETWEEN '{startdate}' and '{enddate}' ORDER BY Date DESC, Time DESC"
    cursor.execute(trend_DI_P9)
    data = cursor.fetchall()
    return data

###############################################################################################################################

def trend_DI_P9_limit(startdate,enddate,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 9' ORDER BY Date DESC, Time DESC limit %s,%s""" % (row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report WHERE Phase='Phase 9' and Date BETWEEN '%s' and '%s' ORDER BY Date DESC, Time DESC limit %s,%s""" % (startdate, enddate, row, rowperpage)
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error


def trend_DI_P9_filter_table(startdate,enddate,likeString):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 9'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 9' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                """ % (likeString, likeString, likeString, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def trend_DI_P9_filter_table_limit(startdate,enddate,likeString,row, rowperpage):
    connection = getConnection()
    if startdate == '' or enddate == '':
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 9'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage)
    else :
        sql = """SELECT Date, Time, Phase, Site, Water, Temp FROM di_report
                WHERE Site LIKE '%s' OR Phase LIKE '%s' OR Station LIKE '%s' and Phase='Phase 9' and Date BETWEEN '%s' and '%s'
                ORDER BY Date DESC, Time DESC
                limit %s, %s""" % (likeString, likeString, likeString,row, rowperpage, startdate, enddate)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

###############################################################################################################################

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

def columnP4():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT off_set.Site FROM off_set
    JOIN Phase ON Phase.Site = off_set.Site
    WHERE Phase.Phase ='Phase 4'"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    return data

def tableP4():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT di_report.Date,
    MAX(CASE WHEN di_report.Site = "Fisa 2" THEN di_report.Water END) "Fisa 2",
    MAX(CASE WHEN di_report.Site = "Fisa 4" THEN di_report.Water END) "Fisa 4",
    MAX(CASE WHEN di_report.Site = "ROBOT" THEN di_report.Water END) "ROBOT"
    FROM di_report
    GROUP BY di_report.Date
    ORDER BY di_report.Date ASC, di_report.Time ASC
    LIMIT 31"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

def columnP5():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT off_set.Site FROM off_set
    JOIN Phase ON Phase.Site = off_set.Site
    WHERE Phase.Phase ='Phase 5'"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    return data

def tableP5():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT di_report.Date,
    MAX(CASE WHEN di_report.Site = "Fisa 3" THEN di_report.Water END) "Fisa 3",
    MAX(CASE WHEN di_report.Site = "L13" THEN di_report.Water END) "L13",
    MAX(CASE WHEN di_report.Site = "L14" THEN di_report.Water END) "L14",
    MAX(CASE WHEN di_report.Site = "L15 Station 1" THEN di_report.Water END) "L15 Station 1",
    MAX(CASE WHEN di_report.Site = "L15 Station 2" THEN di_report.Water END) "L15 Station 2"
    FROM di_report
    GROUP BY di_report.Date
    ORDER BY di_report.Date ASC, di_report.Time ASC
    LIMIT 31"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

def columnP9():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT off_set.Site FROM off_set
    JOIN Phase ON Phase.Site = off_set.Site
    WHERE Phase.Phase ='Phase 9'"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    return data

def tableP9():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT di_report.Date,
    MAX(CASE WHEN di_report.Site = "HC-6" THEN di_report.Water END) "HC-6",
    MAX(CASE WHEN di_report.Site = "HC-3" THEN di_report.Water END) "HC-3",
    MAX(CASE WHEN di_report.Site = "AI" THEN di_report.Water END) "AI",
    MAX(CASE WHEN di_report.Site = "HC-4" THEN di_report.Water END) "HC-4",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 1" THEN di_report.Water END) "HC-5 Station 1",
    MAX(CASE WHEN di_report.Site = "HC-5 Station 2" THEN di_report.Water END) "HC-5 Station 2"
    FROM di_report
    GROUP BY di_report.Date
    ORDER BY di_report.Date ASC, di_report.Time ASC
    LIMIT 31"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())   
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    return data

def report_line_month(date):
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
    WHERE di_report.Date = '{date}'
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

def find_DepartmentID(user):
    DepartmentID = []
    connection = getConnection()
    cursor = connection.cursor()
    find_DepartmentID = "select * from user where Username = '%s'" % (user)
    cursor.execute(find_DepartmentID)
    data = cursor.fetchall()
    for row in range(len(data)):
        DepartmentID.append(data[row]["DepartmentID"])
    return DepartmentID

def users_permission():
    users = find_users()
    myDict = {}
    for username in users:
        
        key = username
        user = username
        
        lst_p = {}
        password = find_DepartmentID(user)
        for word in password:
            lst_p["DepartmentID"] = (word)
        myDict[key] = lst_p
    class_entry_relations = myDict
    return class_entry_relations

def find_Maintain():
    connection = getConnection()
    cursor = connection.cursor()
    find_Maintain = """SELECT phase.OP, phase.Phase, phase.Site, off_set.Status_Di, off_set.Status_Temp, state_maintain.Detail,
    (di_error.Date) as Date, Max(di_error.Time) as Time, MAX(di_error.Water) as Water
    FROM off_set
    JOIN phase on phase.Site = off_set.Site
    JOIN Maintain_data on Maintain_data.Site = off_set.Site
    JOIN State_maintain on maintain_data.StateID = state_maintain.StateID
    JOIN di_error ON di_error.Site = maintain_data.Site
    WHERE off_set.Status_Di != 'N' and off_set.Status_Temp != 'N' and di_error.Date IN(SELECT MAX(di_error.Date) FROM di_error)
    GROUP BY phase.Site
    ORDER BY di_error.Date DESC, di_error.Time DESC"""
    cursor.execute(find_Maintain)
    data = cursor.fetchall()
    return data

def find_user_data(Username):
    connection = getConnection()
    cursor = connection.cursor()
    update = f"""SELECT * from user
    JOIN Department ON Department.DepartmentID = user.DepartmentID
    WHERE username = '{Username}'"""
    cursor.execute(update)
    data = cursor.fetchall()
    return data

def update_process(Username, State, Site):
    connection = getConnection()
    cursor = connection.cursor()
    update = f"""UPDATE maintain_data SET Username='{Username}', StateID='{State}' WHERE Site = '{Site}'"""
    cursor.execute(update)
    data = cursor.fetchall()
    return data

def insert_process(Username, State, Site, Date, Time):
    connection = getConnection()
    cursor = connection.cursor()
    insert_process = f"""INSERT INTO log_matain(Username, Site, StateID, Date, Time) VALUES ('{Username}','{Site}','{State}','{Date}','{Time}')"""
    cursor.execute(insert_process)
    connection.commit()

def show_process(Site):
    connection = getConnection()
    cursor = connection.cursor()
    show_process = f"""SELECT * FROM log_matain
    JOIN state_maintain on state_maintain.StateID = log_matain.StateID
    JOIN user on log_matain.Username = user.Username
    JOIN department on department.departmentID = user.departmentID
    WHERE log_matain.Site = '{Site}' ORDER BY Date DESC, Time DESC LIMIT 1"""
    cursor.execute(show_process)
    data = cursor.fetchall()
    return data

def insertDocument(Username, date, time, place, service, reason, system_now, detail, date_end, note):
    connection = getConnection()
    cursor = connection.cursor()
    Documentdata = f"""INSERT INTO documentdata(Username, date, time, place, service, reason, system_now, detail, date_end, note, StatusID) 
    VALUES ('{Username}','{date}','{time}','{place}','{service}','{reason}','{system_now}','{detail}','{date_end}','{note}','1')"""
    cursor.execute(Documentdata)
    connection.commit()

def countdataDoc():
    connection = getConnection()
    cursor = connection.cursor()
    Count_data = f"""SELECT COUNT(*) as alldata FROM documentdata"""
    cursor.execute(Count_data)
    data = cursor.fetchall()
    return data

def insertDocumentit(keyWork):
    connection = getConnection()
    cursor = connection.cursor()
    Documentdata = f"""INSERT INTO documentit(KeyWork, Username, Cando, Effect, Detail, date_finish, date_deliver, date_getWork, Sum_date) 
    VALUES ('{keyWork}','admin','-','-','-','0000-00-00','0000-00-00','0000-00-00','0')"""
    cursor.execute(Documentdata)
    connection.commit()
    
def SelectDoc_IT():
    connection = getConnection()
    cursor = connection.cursor()
    SelectDoc_IT = f"""SELECT documentdata.KeyWork, documentdata.service, user.Name, documentdata.date, documentdata.time, filterwork.Status,
    documentdata.StatusID FROM documentdata
    JOIN user ON user.Username = documentdata.Username
    JOIN filterwork ON filterwork.StatusID = documentdata.StatusID
    WHERE documentdata.StatusID != 4"""
    cursor.execute(SelectDoc_IT)
    data = cursor.fetchall()
    return data

def Update_Doc_IT(Username, Cando, Effect, Detail, date_finish, date_deliver, date_getWork, Sum_date, KeyWork):
    connection = getConnection()
    cursor = connection.cursor()
    Update = f"""UPDATE documentit SET Username='{Username}', Cando='{Cando}', Effect='{Effect}', Detail ='{Detail}', date_finish ='{date_finish}',
    date_deliver ='{date_deliver}', date_getWork ='{date_getWork}', Sum_date ='{Sum_date}' WHERE KeyWork = '{KeyWork}'"""
    updateStatus = f"""UPDATE documentdata SET StatusID='2' WHERE KeyWork = '{KeyWork}'"""
    cursor.execute(Update)
    cursor.execute(updateStatus)
    connection.commit()
    
def update_state_doc(Status, KeyWork):
    connection = getConnection()
    cursor = connection.cursor()
    updateStatus = f"""UPDATE documentdata SET StatusID='{Status}' WHERE KeyWork = '{KeyWork}'"""
    cursor.execute(updateStatus)
    connection.commit()
    
def Select_Timeline():
    connection = getConnection()
    cursor = connection.cursor()
    Select_Timeline = f"""SELECT documentdata.KeyWork, documentdata.service, user.Name, documentit.date_getWork, filterwork.Status,
    documentdata.StatusID FROM documentdata
    JOIN documentit ON documentit.KeyWork = documentdata.KeyWork
    JOIN user ON user.Username = documentit.Username
    JOIN filterwork ON filterwork.StatusID = documentdata.StatusID"""
    cursor.execute(Select_Timeline)
    data = cursor.fetchall()
    return data

def detail_timeline(KeyWork):
    connection = getConnection()
    cursor = connection.cursor()
    Select_Timeline = f"""SELECT user.Name, User.Phone, user.position, user.Email, department.Department, user.part, documentdata.date,
    documentdata.time, documentdata.place, documentdata.service, documentdata.reason, documentdata.system_now, documentdata.detail,
    documentdata.date_end, documentdata.note, documentdata.StatusID
	FROM documentdata
    JOIN documentit ON documentit.KeyWork = documentdata.KeyWork
    JOIN user ON user.Username = documentit.Username
    JOIN filterwork ON filterwork.StatusID = documentdata.StatusID
    JOIN department ON department.DepartmentID = user.DepartmentID
    WHERE documentdata.KeyWork = '{KeyWork}'"""
    cursor.execute(Select_Timeline)
    data = cursor.fetchall()
    return data    

########################### End Function DB ###########################

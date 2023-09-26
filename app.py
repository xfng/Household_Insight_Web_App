from flask import Flask, request, session, render_template, flash, redirect, url_for, request
from flask_session import Session
from flask_mysqldb import MySQL
import csv


app = Flask(__name__)

app.secret_key = 'cs6400_fa22_team005'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'gatechUser'
app.config['MYSQL_PASSWORD'] = 'gatech123'
app.config['MYSQL_DB'] = 'cs6400_fa22_team005'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html', title='Home')

@app.route('/seed')
def seed():
    cursor = mysql.connection.cursor()

    cursor.execute(f'''
        DELETE FROM RefrigeratorFreezer;
        DELETE FROM Cooker;
        DELETE FROM Oven;
        DELETE FROM OvenHeatSource;
        DELETE FROM Cooktop;
        DELETE FROM Washer;
        DELETE FROM Dryer;
        DELETE FROM TV;
        DELETE FROM HalfBathroom;
        DELETE FROM FullBathroom;
        DELETE FROM PhoneNumber;
        DELETE FROM Household;
        DELETE FROM Location;
        DELETE FROM Manufacturer;
    ''')

    row_count = 0

    with open('seed/demo_data/postal_codes.csv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(row)
            row_count += 1
            cursor.execute(f'''
                INSERT INTO Location(postal_code, city, state, latitude, longitude)
                VALUES("{row['Zip']}", "{row['City']}", "{row['State']}", {float(row['Latitude'])}, {float(row['Longitude'])});
            ''')

    with open('seed/demo_data/Manufacturer.tsv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            print(row)
            row_count += 1
            cursor.execute(f'''
                INSERT INTO Manufacturer(manufacturer)
                VALUES("{row['manufacturer_name']}");
            ''')

    with open('seed/demo_data/Household.tsv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            print(row)
            row_count += 1
            cursor.execute(f'''
                INSERT INTO Household(email, square_footage, number_of_occupants, number_of_bedrooms, type, postal_code)
                VALUES("{row['email']}", {row['footage']}, {row['num_occupants']}, {row['bedroom_count']}, "{row['household_type']}", "{row['postal_code']}");
            ''')

    with open('seed/demo_data/Household.tsv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            if not row['area_code']:
                continue
            print(row)
            row_count += 1
            cursor.execute(f'''
                INSERT INTO PhoneNumber(email, area_code, last_7_digits, type)
                VALUES("{row['email']}", "{row['area_code']}", "{row['phone_number']}", "{row['phone_type']}");
            ''')

    with open('seed/demo_data/Bathrooms.tsv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            print(row)
            if row['tub_count']:
                print('full bathroom')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO FullBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, number_of_bathtubs, number_of_showers, number_of_tubs_showers, whether_primary)
                    VALUES("{row['household_email']}", "{row['bathroom_number']}", "{row['sink_count']}", "{row['commode_count']}", "{row['bidet_count']}", "{row['tub_count']}", "{row['shower_count']}", "{row['tub_shower_count']}", "{row['primary_bathroom']}");
                ''')
            else:
                print('half bathroom')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO HalfBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, name)
                    VALUES("{row['household_email']}", "{row['bathroom_number']}", "{row['sink_count']}", "{row['commode_count']}", "{row['bidet_count']}", "{row['bathroom_name']}");
                ''')

    with open('seed/demo_data/Appliance.tsv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            print(row)
            if row['refrigerator_type']:
                print('RefrigeratorFreezer')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO RefrigeratorFreezer(email, appliance_order, model_name, manufacturer, type)
                    VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['model']}", "{row['manufacturer_name']}", "{row['refrigerator_type']}");
                ''')
            elif row['oven_type'] or row['cooktop_heat_source']:
                print('Cooker')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO Cooker(email, appliance_order, model_name, manufacturer)
                    VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['model']}", "{row['manufacturer_name']}");
                ''')
                if row['oven_type']:
                    print('Oven')
                    row_count += 1
                    cursor.execute(f'''
                        INSERT INTO Oven(email, appliance_order, type)
                        VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['oven_type']}");
                    ''')
                    for oven_heat_source in row['oven_heat_sources'].split(';'):
                        print('OvenHeatSource')
                        row_count += 1
                        cursor.execute(f'''
                            INSERT INTO OvenHeatSource(email, appliance_order, heat_source)
                            VALUES("{row['household_email']}", "{row['appliance_number']}", "{oven_heat_source}");
                        ''')
                if row['cooktop_heat_source']:
                    print('Cooktop')
                    row_count += 1
                    cursor.execute(f'''
                        INSERT INTO Cooktop(email, appliance_order, heat_source)
                        VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['cooktop_heat_source']}");
                    ''')
            elif row['washer_load_type']:
                print('Washer')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO Washer(email, appliance_order, model_name, manufacturer, loading_type)
                    VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['model']}", "{row['manufacturer_name']}", "{row['washer_load_type']}");
                ''')
            elif row['dryer_heat_source']:
                print('Dryer')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO Dryer(email, appliance_order, model_name, manufacturer, heat_source)
                    VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['model']}", "{row['manufacturer_name']}", "{row['dryer_heat_source']}");
                ''')
            elif row['display_size']:
                print('TV')
                row_count += 1
                cursor.execute(f'''
                    INSERT INTO TV(email, appliance_order, model_name, manufacturer, display_type, display_size, maximum_resolution)
                    VALUES("{row['household_email']}", "{row['appliance_number']}", "{row['model']}", "{row['manufacturer_name']}", "{row['display_type']}", "{row['display_size']}", "{row['resolution']}");
                ''')

    mysql.connection.commit()

    return {'added_rows': row_count}

@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/getemail', methods=['GET', 'POST'])
def getemail():
    message = ''
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute(f'''
               SELECT email FROM Household WHERE Household.email = '{email}';
        ''')
        result = cursor.fetchone()
        if not result:
            session['email'] = email
            return redirect('postalcode')
        else:
            message = 'Email is registered!'
    return render_template('getemail.html', title='Get Email', msg=message)


@app.route('/postalcode', methods=['GET', 'POST'])
def postalcode():
    return render_template('postalcode.html', title='Get Postal Code')



@app.route('/postal_confirm', methods=['GET', 'POST'])
def postalconfirm():
    message = ''
    if request.method == 'POST':
        postal_code = request.form['postal_code']
        cursor = mysql.connection.cursor()
        cursor.execute(f'''
               SELECT postal_code, city, state FROM Location WHERE Location.postal_code = '{postal_code}';
        ''')
        result = cursor.fetchone()
        if result:
            session['postal_code'] = result['postal_code']
            session['city'] = result['city']
            session['state'] = result['state']
            return render_template('postal_confirm.html', title='Confirm Postal Code', postal_code=session['postal_code'], city=session['city'], state=session['state'])
        else:
            message="Postal code not found!"
    return render_template('postalcode.html', title='Get Postal Code', msg=message)



@app.route('/phonenumber', methods=['GET','POST'])
def phonenumber():
    message = ''
    if request.method == 'POST':
        if 'area_code' in request.form:
            area_code = request.form['area_code']
            last_7_digits = request.form['last_7_digits']
            phone_type = request.form['phone_type']
            cursor = mysql.connection.cursor()
            cursor.execute(f'''
                SELECT area_code, last_7_digits FROM PhoneNumber WHERE area_code = '{area_code}' AND last_7_digits = '{last_7_digits}';
            ''')
            result = cursor.fetchone()
            if not result:
                session['area_code'] = area_code
                session['last_7_digits'] = last_7_digits.replace('-', '')
                session['phone_type'] = phone_type
                return redirect('householdinfo')
            else:
                message = 'Phone number is registered!'
        else:
            session['area_code'] = None
            session['last_7_digits'] = None
            session['phone_type'] = None
            return redirect('householdinfo')

    return render_template('phonenumber.html', title='Enter Phone Number', msg=message)


@app.route('/householdinfo', methods=['GET','POST'])
def householdinfo():
    if request.method == 'POST':
        session['home_type'] = request.form['home_type']
        session['square_footage'] = int(request.form['square_footage'])
        session['number_of_occupants'] = int(request.form['number_of_occupants'])
        session['number_of_bedrooms'] = int(request.form['number_of_bedrooms'])
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(f'''
                INSERT INTO Household(email, square_footage, number_of_occupants, number_of_bedrooms, type, postal_code)
                VALUES('{session['email']}', {session['square_footage']}, {session['number_of_occupants']}, {session['number_of_bedrooms']}, '{session['home_type']}', '{session['postal_code']}');
            ''')
            cursor.execute(f'''
                INSERT INTO PhoneNumber (email, area_code, last_7_digits, type) VALUES('{session['email']}','{session['area_code']}', '{session['last_7_digits']}', '{session['phone_type']}');
            ''')
            mysql.connection.commit()
            for key in list(session.keys()):
                if key != "email":
                    session.pop(key)
            return redirect('add_bathroom')
        except:
            return redirect('submission_fail')
    return render_template('householdinfo.html', title='Household Info')


@app.route('/add_bathroom', methods=['GET','POST'])
def add_bathroom():
    message = ''
    if request.method == 'POST': 
        if 'whether_primary' in request.form:
            session['number_of_sinks'] = int(request.form['number_of_sinks'])
            session['number_of_commodes'] = int(request.form['number_of_commodes'])
            session['number_of_bidets'] = int(request.form['number_of_bidets'])
            session['number_of_bathtubs'] = int(request.form['number_of_bathtubs'])
            session['number_of_showers'] = int(request.form['number_of_showers'])
            session['number_of_tubs_showers'] = int(request.form['number_of_tubs_showers'])
            session['whether_primary'] = int(request.form['whether_primary'])
            
            cursor = mysql.connection.cursor()     
            cursor.execute(f'''Select whether_primary from FullBathroom where email='{session['email']}' and whether_primary = 1;''')        
            result_0 = cursor.fetchone()   
            if result_0 and session['whether_primary'] == 1:
                message = "Primary Bathroom is registered!"
                return render_template('add_bathroom.html', title='Add Bathroom', msg=message)

            if session['number_of_sinks'] < 0 or session['number_of_commodes'] < 0 or (session['number_of_sinks'] + session['number_of_commodes'] == 0):
                message = "Full Bathroom Should Have At Least One Sink or Commode!"
                return render_template('add_bathroom.html', title='Add Bathroom', msg=message)

            if session['number_of_bathtubs'] < 0 or session['number_of_showers'] < 0 or session['number_of_tubs_showers'] < 0 or (session['number_of_bathtubs'] + session['number_of_showers'] + session['number_of_tubs_showers'] == 0):
                message = "Full Bathroom Should Have At Least One Bath, Shower or Tub/Shower!"
                return render_template('add_bathroom.html', title='Add Bathroom', msg=message)
            
            cursor.execute(f'''Select email, count(email) as count, count(email)+1 as bathroom_order FROM
                    (
                    SELECT email
                    FROM FullBathroom WHERE email = '{session['email']}' 
                    UNION ALL
                    SELECT email
                    FROM HalfBathroom WHERE email = '{session['email']}'
                    ) as combined;''')
            result_1 = cursor.fetchone()
            if result_1['count'] > 0:
                try:
                    cursor.execute(f'''INSERT INTO FullBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, number_of_bathtubs, number_of_showers, number_of_tubs_showers, whether_primary)
                                    SELECT '{session['email']}', bathroom_order,'{session['number_of_sinks']}', {session['number_of_commodes']}, {session['number_of_bidets']}, {session['number_of_bathtubs']}, {session['number_of_showers']}, {session['number_of_tubs_showers']}, {session['whether_primary']}
                                    FROM (
                                    Select email, count(email) as count, count(email)+1 as bathroom_order FROM
                                    (
                                    SELECT email
                                    FROM FullBathroom WHERE email = '{session['email']}'
                                    UNION ALL
                                    SELECT email
                                    FROM HalfBathroom WHERE email = '{session['email']}'
                                    ) as combined ) as t;''')
                    mysql.connection.commit()
                    return redirect('bathroomlisting')
                except:
                    return redirect('submission_fail')
            else:
                try:
                    cursor.execute(f'''INSERT INTO FullBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, number_of_bathtubs, number_of_showers, number_of_tubs_showers, whether_primary)
                        VALUES('{session['email']}', '1', '{session['number_of_sinks']}', '{session['number_of_commodes']}', '{session['number_of_bidets']}', '{session['number_of_bathtubs']}', 
                        '{session['number_of_showers']}', '{session['number_of_tubs_showers']}', '{session['whether_primary']}'); 
                        ''')
                    mysql.connection.commit()
                    return redirect('bathroomlisting')
                except:
                    return redirect('submission_fail')        

        else: 
            session['number_of_sinks'] = int(request.form['number_of_sinks'])
            session['number_of_commodes'] = int(request.form['number_of_commodes'])
            session['number_of_bidets'] = int(request.form['number_of_bidets'])
            session['name'] = request.form['half_bathroom_name']
            cursor = mysql.connection.cursor() 
            cursor.execute(f'''Select email, count(email) as count, count(email)+1 as bathroom_order FROM
                    (
                    SELECT email
                    FROM FullBathroom WHERE email = '{session['email']}' 
                    UNION ALL
                    SELECT email
                    FROM HalfBathroom WHERE email = '{session['email']}'
                    ) as combined;''')
            result_1 = cursor.fetchone()

            if session['number_of_sinks'] < 0 or session['number_of_commodes'] < 0 or (session['number_of_sinks'] + session['number_of_commodes'] == 0):
                message = "Half Bathroom Should Have At Least One Sink or Commode!"
                return render_template('add_bathroom.html', title='Add Bathroom', msg=message)
            
            if result_1['count'] > 0:
                try:
                    cursor.execute(f'''
                    INSERT INTO HalfBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, name)
                            SELECT '{session['email']}', bathroom_order,'{session['number_of_sinks']}', '{session['number_of_commodes']}', '{session['number_of_bidets']}', '{session['name']}'
                            FROM (
                            Select email, count(email) as count, count(email)+1 as bathroom_order FROM
                            (
                            SELECT email
                            FROM FullBathroom WHERE email = '{session['email']}'
                            UNION ALL
                            SELECT email
                            FROM HalfBathroom WHERE email = '{session['email']}'
                            ) as combined ) as t;
                    ''')
                    mysql.connection.commit()
                    return redirect('bathroomlisting')
                except:
                    return redirect('submission_fail')
            else:    
                try:
                    cursor.execute(f'''
                        INSERT INTO HalfBathroom(email, bathroom_order, number_of_sinks, number_of_commodes, number_of_bidets, name)
                        VALUES('{session['email']}', '1','{session['number_of_sinks']}','{session['number_of_commodes']}','{session['number_of_bidets']}', '{session['name']}');
                    ''')
                    mysql.connection.commit()
                    return redirect('bathroomlisting')
                except:
                    return redirect('submission_fail')   
              
    return render_template('add_bathroom.html', title='Add Bathroom', msg=message)

@app.route('/bathroomlisting', methods=['GET','POST'])
def bathroomlisting():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT bathroom_order, type, whether_primary
        FROM
        (
            SELECT email, bathroom_order, 'full' AS type, whether_primary FROM FullBathroom
            WHERE email = '{session['email']}'
            UNION ALL
            SELECT email, bathroom_order, 'half' AS type, null as whether_primary FROM HalfBathroom
            WHERE email = '{session['email']}'
        ) AS combined
        ORDER BY bathroom_order
        ;
    ''')
    results = list(cur.fetchall())
    print(results)
    for r in results:
        if r['whether_primary'] == 1:
            r['whether_primary'] = 'Yes'
        else:
            r['whether_primary'] = ''

    return render_template('bathroomlisting.html', title='Bathroom Listing', data = results)

 
@app.route('/add_appliance', methods=['GET','POST'])
def add_appliance():
    for key in list(session.keys()):
        if key != "email":
            session.pop(key)
    cursor = mysql.connection.cursor()
    cursor.execute(f'''select manufacturer from Manufacturer;''')
    result_0 = cursor.fetchall()
    data = list(result_0)
    if request.method == 'POST':
        
        session['appliance_type'] = request.form['appliance_type']
        session['manufacturer'] = request.form['manufacturer_list']
        session['model_name'] = request.form['model_name']
        
        if session['appliance_type'] == 'Refrigeratorfreezer': 
            session['refrigerator_type'] = request.form['refrigerator_type']

        if session['appliance_type'] == 'Cooker':
            if 'cooker1' in request.form:
                session['cooker1'] = 'oven'
                try:
                    session['heat_source1'] = request.form['heat_source1']
                except:
                    session['heat_source1'] = ''
                try:
                    session['heat_source2'] = request.form['heat_source2']
                except:
                    session['heat_source2'] = ''
                try:
                    session['heat_source3'] = request.form['heat_source3']
                except:
                    session['heat_source3'] = ''
                oven_heat_source = [session['heat_source1'], session['heat_source2'], session['heat_source3']]
                session['oven_type'] = request.form['oven_type']
                print('oven_session_success')
                print(session)
            else:
                session['cooker1'] = ''
                oven_heat_source = ''
                oven_heat_source = ['']

            if 'cooker2' in request.form:
                session['cooker2'] = 'cooktop'
                session['cooktop_heat_source'] = request.form['cooktop_heat_source']
                print('cooktop_session_success')
            else:
                session['cooker2'] = ''
                session['cooktop_heat_source'] = ''   
        
        if session['appliance_type'] == 'Washer':
            session['loading_type'] = request.form['loading_type']
        
        if session['appliance_type'] == 'Dryer':
            session['dryer_heat_source'] = request.form['dryer_heat_source']
        
        if session['appliance_type'] == 'TV':
            session['display_type'] = request.form['display_type']
            session['display_size'] = request.form['display_size']
            session['maximum_resolution'] = request.form['maximum_resolution']

        cursor = mysql.connection.cursor()
        cursor.execute(f'''
                SELECT email, count(email) as count, (count(email) +1) as appliance_order from (
                SELECT email FROM RefrigeratorFreezer WHERE email = '{session['email']}'
                UNION ALL
                SELECT email FROM Cooker WHERE email = '{session['email']}'
                UNION ALL
                SELECT email FROM Washer WHERE email = '{session['email']}'
                UNION ALL
                SELECT email FROM Dryer WHERE email = '{session['email']}'
                UNION ALL
                SELECT email FROM TV WHERE email = '{session['email']}'
                ) as combined
                GROUP BY combined.email;
        ''')
        result_1 = cursor.fetchone()
        print(result_1)
        if result_1:
            appliance_order = result_1['appliance_order']
        else:
            appliance_order = 1
        print('appliance_order', appliance_order)

        if session['appliance_type'] == 'Refrigeratorfreezer':
            try:
                cursor.execute(f'''
                INSERT INTO RefrigeratorFreezer (email, appliance_order, type, manufacturer, model_name)
                VALUES ('{session['email']}', '{appliance_order}', '{session['refrigerator_type']}', '{session['manufacturer']}', '{session['model_name']}'); 
                ''')
                mysql.connection.commit()
                print("refrigeratorFreezer Success")
                return redirect('/appliancelisting') 
            except:
                return redirect('submission_fail')   

        if session['appliance_type'] == 'Cooker':
            try:
                cursor.execute(f'''
                INSERT INTO Cooker (email, appliance_order, manufacturer, model_name) 
                VALUES ('{session['email']}', '{appliance_order}', '{session['manufacturer']}', '{session['model_name']}');
                ''')
                mysql.connection.commit()
                print("isCooker")

                if session['cooker1'] == 'oven':
                    try:
                        cursor.execute(f'''
                            INSERT INTO Oven (email, appliance_order, type) 
                            VALUES ('{session['email']}', '{appliance_order}', '{session['oven_type']}');
                            ''')
                        mysql.connection.commit()
                        print("isCooker1") 
                    except:
                        return redirect('submission_fail')

                for heat_source in oven_heat_source:
                    try:
                        if heat_source != '':
                            cursor.execute(f'''
                            INSERT INTO OvenHeatSource (email, appliance_order,  heat_source) 
                            VALUES ('{session['email']}', '{appliance_order}', '{heat_source}');
                            ''') 
                            mysql.connection.commit()
                            print('insert OvenHeatSource Success')

                    except:
                        return redirect('submission_fail')

                if session['cooker2'] == 'cooktop':
                    try:
                        cursor.execute(f'''
                                INSERT INTO Cooktop (email, appliance_order, heat_source) 
                                VALUES ('{session['email']}', '{appliance_order}', '{session['cooktop_heat_source']}');
                                ''')
                        mysql.connection.commit()
                        print('cooker insert Cooktop success')
                    except:
                        return redirect('submission_fail')
                return redirect('/appliancelisting')
            except:
                return redirect('submission_fail')

        if session['appliance_type'] == 'Washer':
            try:
                cursor.execute(f''' 
                INSERT INTO Washer (email, appliance_order, manufacturer, model_name, loading_type)
                VALUES ('{session['email']}', '{appliance_order}', '{session['manufacturer']}', '{session['model_name']}', '{session['loading_type']}');
                ''')
                mysql.connection.commit()
                return redirect('/appliancelisting')
            except:
                return redirect('submission_fail')

        if session['appliance_type'] == 'Dryer':
            try:
                cursor.execute(f'''
                INSERT INTO Dryer (email, appliance_order, heat_source, manufacturer, model_name)
                VALUES ('{session['email']}', '{appliance_order}', '{session['dryer_heat_source']}', '{session['manufacturer']}', '{session['model_name']}'); 
                ''')
                mysql.connection.commit()
                return redirect('/appliancelisting')
            except:
                return redirect('submission_fail')

        if session['appliance_type'] == 'TV':
            if float(session['display_size']) <= 0:
                message = "TV display size should be larger than 0!"
                return render_template('add_appliance.html', title='Add Appliance', data=data, msg=message)
            try:
                cursor.execute(f'''
                INSERT INTO TV (email, appliance_order, display_type, display_size, maximum_resolution, manufacturer, model_name)
                VALUES ('{session['email']}', '{appliance_order}', '{session['display_type']}', '{session['display_size']}', '{session['maximum_resolution']}', '{session['manufacturer']}', '{session['model_name']}');
                ''')
                mysql.connection.commit()
                return redirect('/appliancelisting')
            except:
                return redirect('submission_fail')

    return render_template('add_appliance.html', title='Add Appliance', data=data)

@app.route('/appliancelisting', methods=['GET','POST'])
def appliancelisting():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT appliance_order, appliance_type, manufacturer, model_name
        FROM
        (
            SELECT email, appliance_order, 'Refrigerator/freezer' AS appliance_type, manufacturer, model_name
            FROM RefrigeratorFreezer
            WHERE email='{session['email']}'
            UNION ALL
            SELECT email, appliance_order, 'Cooker' AS appliance_type, manufacturer, model_name
            FROM Cooker
            WHERE email = '{session['email']}'
            UNION ALL
            SELECT email, appliance_order, 'Washer' AS appliance_type, manufacturer, model_name
            FROM Washer
            WHERE email = '{session['email']}'
            UNION ALL
            SELECT email, appliance_order, 'Dryer' AS appliance_type, manufacturer, model_name
            FROM Dryer
            WHERE email = '{session['email']}'
            UNION ALL
            SELECT email, appliance_order, 'TV' AS appliance_type, manufacturer, model_name
            FROM TV
            WHERE email = '{session['email']}'
        ) AS combined
        ORDER BY appliance_order
        ;
    ''')
    results = cur.fetchall()
    return render_template('appliancelisting.html', title='Appliance Listing', data=list(results))

@app.route('/wrapping_up', methods=['GET','POST'])
def wrapping_up():
    message = ''
    session.clear()
    return render_template('wrapping_up.html', title='Warpping Up', msg=message)

@app.route('/submission_fail')
def submission_fail():
    # message = ""
    # return render_template('submission_fail.html', title='Submission Failed', msg=message)
    return "submission fail"

@app.route('/view_reports')
def view_reports():
    return render_template('view_reports.html', title='View Reports')


@app.route('/current_session')
def current_session():
    return dict(session)

@app.route('/households')
def households():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Household''')
    results = cur.fetchall()
    return list(results)

@app.route('/phonenumber_db')
def phonenumber_db():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM PhoneNumber''')
    results = cur.fetchall()
    return list(results)

@app.route('/bathrooms/<email>')
def bathrooms(email):
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT bathroom_order, type, whether_primary
        FROM
        (
            SELECT email, bathroom_order, 'full' AS type, whether_primary FROM FullBathroom
            WHERE email = '{email}'
            UNION ALL
            SELECT email, bathroom_order, 'half' AS type, null as whether_primary FROM HalfBathroom
            WHERE email = '{email}'
        ) AS combined
        ORDER BY bathroom_order
        ;
    ''')
    results = cur.fetchall()
    return list(results)

@app.route('/bathroomlisting/<email>')
def bathroomslisting(email):
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT bathroom_order, type, whether_primary
        FROM
        (
            SELECT email, bathroom_order, 'full' AS type, whether_primary FROM FullBathroom
            WHERE email = '{email}'
            UNION ALL
            SELECT email, bathroom_order, 'half' AS type, null as whether_primary FROM HalfBathroom
            WHERE email = '{email}'
        ) AS combined
        ORDER BY bathroom_order
        ;
    ''')
    results = cur.fetchall()

    return list(results)

@app.route('/appliances/<email>')
def appliances(email):
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT appliance_order, appliance_type, manufacturer, model_name FROM
        (
            SELECT email, appliance_order, 'Refrigerator/freezer' as appliance_type, manufacturer, model_name
            FROM RefrigeratorFreezer
            WHERE email = '{email}'
            UNION ALL
            SELECT email, appliance_order, 'Cooker' AS appliance_type, manufacturer, model_name
            FROM Cooker
            WHERE email = '{email}'
            UNION ALL
            SELECT email, appliance_order, 'Washer' AS appliance_type, manufacturer, model_name
            FROM Washer
            WHERE email = '{email}'
            UNION ALL
            SELECT email, appliance_order, 'Dryer' AS appliance_type, manufacturer, model_name
            FROM Dryer
            WHERE email = '{email}'
            UNION ALL
            SELECT email, appliance_order, 'TV' AS appliance_type, manufacturer, model_name
            FROM TV
            WHERE email = '{email}'
        ) AS combined
        ORDER BY appliance_order
        ;
    ''')
    results = cur.fetchall()
    return list(results)

@app.route('/top_25_popular_manufacturers')
def top_25_popular_manufacturers():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT manufacturer, COUNT(manufacturer) AS count FROM
        (
            SELECT manufacturer FROM RefrigeratorFreezer
            UNION ALL
            SELECT manufacturer FROM Cooker
            UNION ALL
            SELECT manufacturer FROM Washer
            UNION ALL
            SELECT manufacturer FROM Dryer
            UNION ALL
            SELECT manufacturer FROM TV
        ) AS Combined
        GROUP BY Combined.manufacturer ORDER BY count DESC
        LIMIT 25
        ;
    ''')
    results = cur.fetchall()
    headings = ['Manufacturer', 'Count']
    return render_template('top_25_popular_manufacturers.html', title='Top 25 Popular Manufacturers Report', data=list(results))


@app.route('/view_manufacturer_drilldown', methods=['POST'])
def view_manufacturer_drilldown():
    manufacturer = request.form['manufacturer']

    cur = mysql.connection.cursor()
    cur.execute(f'''
        WITH dryer_count AS (
            SELECT '{manufacturer}' as manufacturer, 'Dryer' AS type, COUNT(manufacturer) AS count
            FROM Dryer
            WHERE manufacturer = '{manufacturer}'
        ),
        washer_count AS (
            SELECT '{manufacturer}' as manufacturer, 'Washer' AS type, COUNT(manufacturer) AS count
            FROM Washer
            WHERE manufacturer = '{manufacturer}'
        ),
        RefrigeratorFreezer_count AS (
            SELECT '{manufacturer}' as manufacturer, 'RefrigeratorFreezer' AS type, COUNT(manufacturer) AS count
            FROM RefrigeratorFreezer
            WHERE manufacturer = '{manufacturer}'
        ),
        Cooker_count AS (
            SELECT '{manufacturer}' as manufacturer, 'Cooker' AS type, COUNT(manufacturer) AS count
            FROM Cooker
            WHERE manufacturer = '{manufacturer}'
        ),
        TV_count AS (
            SELECT '{manufacturer}' as manufacturer, 'TV' AS type, COUNT(manufacturer) AS count
            FROM TV
            WHERE manufacturer = '{manufacturer}'
        )
        SELECT
            dryer_count.type as 'dryer type',
            dryer_count.count as 'dryer count',
            washer_count.type as 'washer type',
            washer_count.count as 'washer count',
            RefrigeratorFreezer_count.type as 'refrigerator / freezer type',
            RefrigeratorFreezer_count.count as 'refrigerator / freezer count',
            Cooker_count.type as 'cooker type',
            Cooker_count.count as 'cooker count',
            TV_count.type as 'tv type',
            TV_count.count as 'tv count'
        FROM dryer_count
        JOIN washer_count ON dryer_count.manufacturer = washer_count.manufacturer
        JOIN RefrigeratorFreezer_count ON RefrigeratorFreezer_count.manufacturer = dryer_count.manufacturer
        JOIN Cooker_count ON Cooker_count.manufacturer = dryer_count.manufacturer
        JOIN TV_count ON TV_count.manufacturer = dryer_count.manufacturer
        ;
    ''')
    results = cur.fetchall()
    return render_template('view_manufacturer_drilldown.html', title='Manufacturer Drilldown Report', manufacturer=manufacturer, data=list(results))

@app.route('/search_manufacturer_model', methods=['GET', 'POST'])
def search_manufacturer_model():
    data=''
    headings=['']
    search_input=['']
    if request.method == 'POST':
        search_input = request.form['search_input']
        cur = mysql.connection.cursor()
        cur.execute(f'''
            SELECT DISTINCT Manufacturer.manufacturer, temp.model_name from Manufacturer
            LEFT JOIN
            (
                SELECT manufacturer, model_name from RefrigeratorFreezer
                UNION
                SELECT manufacturer, model_name from Cooker
                UNION
                SELECT manufacturer, model_name from Washer
                UNION
                SELECT manufacturer, model_name from Dryer
                UNION
                SELECT manufacturer, model_name from TV
            ) temp
            ON Manufacturer.manufacturer = temp.manufacturer
            WHERE Manufacturer.manufacturer like CONCAT('%', '{search_input}', '%') OR temp.model_name like CONCAT('%', '{search_input}', '%')
            ORDER BY Manufacturer.manufacturer ASC, temp.model_name ASC
            ;
        ''')
        results = cur.fetchall()
        data = list(results)
        headings=['Manufacturer', 'Model Name']
    return render_template('search_manufacturer_model.html', title='Search Manufacturer Model Report', headings=headings, data=data, search_input=search_input)

@app.route('/view_avg_tv_display_size_by_state')
def view_avg_tv_display_size_by_state():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT temp.state, round(avg(temp.display_size),1) as average_display_size FROM
        (
            SELECT l.state, TV.display_size
            FROM TV
            JOIN (
                SELECT Household.email, Household.postal_code FROM Household
            ) AS h
            ON TV.email = h.email
            JOIN (
                SELECT Location.postal_code, Location.state FROM Location
            ) AS l
            ON h.postal_code = l.postal_code
        ) as temp
        GROUP BY temp.state
        ORDER BY temp.state ASC
        ;
    ''')
    results = cur.fetchall()

    return render_template('view_avg_tv_display_size_by_state.html', title='Avg TV Display Size by State Report', data=list(results))

@app.route('/view_avg_tv_display_size_by_state_drilldown', methods=['POST'])
def view_avg_tv_display_size_by_state_drilldown():
    state = request.form['state']
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT temp.display_type, temp.maximum_resolution, round(avg(temp.display_size),1) as average_display_size
        FROM (
            SELECT l.state, TV.display_type, TV.maximum_resolution, TV.display_size
            FROM TV
            JOIN (
                SELECT Household.email, Household.postal_code FROM Household
            ) AS h
            ON TV.email = h.email
            JOIN (
                SELECT Location.postal_code, Location.state FROM Location
            ) AS l
            ON h.postal_code = l.postal_code
            where l.state = '{state}'
        ) as temp
        GROUP BY temp.state, temp.display_type, temp.maximum_resolution ORDER BY average_display_size DESC
        ;
    ''')
    results = cur.fetchall()
    data =  list(results)
    return render_template('view_avg_tv_display_size_by_state_drilldown.html', title='Avg TV Display Size by State Drilldown Report', data=data, state=state)

@app.route('/extra_fridge_freezer_report')
def extra_fridge_freezer_report():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        SELECT count(c.household_emails) as household_count FROM
        (
            SELECT distinct(email) as household_emails FROM RefrigeratorFreezer
            GROUP BY email
            HAVING count(email) > 1
        ) AS c
        ;
    ''')
    results_0 = cur.fetchall()

    cur.execute(f'''
        WITH households_with_multiple_by_state as (
            SELECT Location.state, Household.email, count(Household.email) as multiple_count
            FROM RefrigeratorFreezer
            JOIN Household on RefrigeratorFreezer.email = Household.email
            JOIN Location on Household.postal_code = Location.postal_code
            GROUP BY Location.state, Household.email
            HAVING multiple_count>1
        ),
        with_chest_freezers_by_state as (
            SELECT Location.state, count(distinct(Household.email)) as with_chest_freezers_count
            FROM RefrigeratorFreezer
            JOIN Household on RefrigeratorFreezer.email = Household.email
            JOIN Location on Household.postal_code = Location.postal_code
            WHERE RefrigeratorFreezer.type = 'chest freezer'
                AND Household.email in (SELECT email from households_with_multiple_by_state)
            GROUP BY state
        ),
        with_upright_freezers_by_state as (
            SELECT Location.state, count(distinct(Household.email)) as with_upright_freezers_count
            FROM RefrigeratorFreezer
            JOIN Household on RefrigeratorFreezer.email = Household.email
            JOIN Location on Household.postal_code = Location.postal_code
            WHERE RefrigeratorFreezer.type = 'upright freezer'
                AND Household.email in (SELECT email from households_with_multiple_by_state)
            GROUP BY state
        ),
        with_others_by_state as (
            SELECT Location.state, count(distinct(Household.email)) as with_others_count FROM RefrigeratorFreezer
            JOIN Household on RefrigeratorFreezer.email = Household.email
            JOIN Location on Household.postal_code = Location.postal_code
            WHERE RefrigeratorFreezer.type != 'chest freezer'
                AND RefrigeratorFreezer.type != 'upright freezer'
                AND Household.email in (SELECT email from households_with_multiple_by_state)
            GROUP BY state
        )
        SELECT
            households_with_multiple_by_state.state,
            count(households_with_multiple_by_state.email) AS household_count,
            round(100 * with_chest_freezers_count / count(households_with_multiple_by_state.email),0) AS the_percentage_of_households_with_multiple_fridge_freezers_in_that_state_with_a_chest_freezer,
            round(100 * with_upright_freezers_count / count(households_with_multiple_by_state.email),0) AS the_percentage_of_households_with_multiple_fridge_freezers_in_that_state_with_an_upright_freezer,
            round(100 * with_others_count / count(households_with_multiple_by_state.email),0) AS the_percentage_of_households_with_multiple_fridge_freezers_in_that_state_with_something_else
        FROM households_with_multiple_by_state
            left join with_chest_freezers_by_state on households_with_multiple_by_state.state = with_chest_freezers_by_state.state
            left join with_upright_freezers_by_state on households_with_multiple_by_state.state = with_upright_freezers_by_state.state
            left join with_others_by_state on households_with_multiple_by_state.state = with_others_by_state.state
        GROUP BY households_with_multiple_by_state.state
        ORDER BY household_count DESC
        LIMIT 10
        ;
    ''')
    results_1 = cur.fetchall()
    total_count = list(results_0)[0]
    data = list(results_1)
    return render_template('extra_fridge_freezer_report.html', title='Extra Fridge Freezer Report', total_count=total_count, data=data)

@app.route('/laundry_center_report')
def laundry_center_report():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        with state_count_heat_source as (
            select Location.state, Dryer.heat_source, count(Dryer.heat_source) as count_heat_source
            from Household
            join Location on Household.postal_code = Location.postal_code
            join Dryer on Household.email = Dryer.email
            group by Location.state, Dryer.heat_source
            order by count_heat_source desc
        ),
        state_max_heat_source as (
            select state, max(count_heat_source) as max_count_heat_source from state_count_heat_source
            group by state
        ),
        state_most_common_dryer_heat_source as (
            select state_count_heat_source.state, state_count_heat_source.heat_source as most_common_dryer_heat_source
            from state_count_heat_source
            join state_max_heat_source on state_count_heat_source.state = state_max_heat_source.state
            where state_count_heat_source.count_heat_source = state_max_heat_source.max_count_heat_source
        ),
        state_count_loading_type as
        (
            select Location.state, Washer.loading_type, count(Washer.loading_type) as count_loading_type
            from Household
            join Location on Household.postal_code = Location.postal_code join Washer on Household.email = Washer.email
            group by Location.state, Washer.loading_type
            order by count_loading_type desc
        ),
        state_max_loading_type as (
            select state, max(count_loading_type) as max_count_loading_type from state_count_loading_type
            group by state
        ),
        state_most_common_washer_loading_type as (
            select state_count_loading_type.state, state_count_loading_type.loading_type as most_common_washer_loading_type
            from state_count_loading_type
            join state_max_loading_type on state_count_loading_type.state = state_max_loading_type.state
            where state_count_loading_type.count_loading_type = state_max_loading_type.max_count_loading_type
        )
        SELECT
            COALESCE(state_most_common_dryer_heat_source.state, state_most_common_washer_loading_type.state) as state,
            most_common_dryer_heat_source,
            most_common_washer_loading_type
        FROM state_most_common_dryer_heat_source
        LEFT JOIN state_most_common_washer_loading_type
            ON state_most_common_dryer_heat_source.state = state_most_common_washer_loading_type.state
        UNION
        SELECT
            COALESCE(state_most_common_dryer_heat_source.state, state_most_common_washer_loading_type.state) as state,
            most_common_dryer_heat_source,
            most_common_washer_loading_type
        FROM state_most_common_dryer_heat_source
        RIGHT JOIN state_most_common_washer_loading_type
            ON state_most_common_dryer_heat_source.state = state_most_common_washer_loading_type.state
        ;
    ''')
    results_0 = cur.fetchall()

    cur.execute(f'''
        with households_with_washer as (
            select Location.state, Household.email
            from Household
            join Location on Household.postal_code = Location.postal_code
            join Washer on Household.email = Washer.email
            group by Household.email
        ),
        households_with_dryer as (
            select Location.state, Household.email
            from Household
            join Location on Household.postal_code = Location.postal_code
            join Dryer on Household.email = Dryer.email
            group by Household.email
        )
        select state, count(email) as household_count from households_with_washer
        where households_with_washer.email not in
        (
            select email from households_with_dryer
        )
        group by state
        order by household_count desc
        ;
    ''')
    results_1 = cur.fetchall()
    data_0 = list(results_0)
    data_1 = list(results_1)
    return render_template('laundry_center_report.html', title='Laundry Center Report', data_0=data_0, data_1=data_1)

@app.route('/bathroom_statistics')
def bathroom_statistics():
    cur = mysql.connection.cursor()
    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, count(*) as full_bathroom_count from Household
            join FullBathroom on Household.email = FullBathroom.email group by Household.email
        ),
        households_half_bathrooms as (
            select Household.email, count(*) as half_bathroom_count from Household
            join HalfBathroom on Household.email = HalfBathroom.email group by Household.email
        )
        select
            min(full_bathroom_count+half_bathroom_count) as min_bathroom_count,
            round(avg(full_bathroom_count+half_bathroom_count), 1) as avg_bathroom_count,
            max(full_bathroom_count+half_bathroom_count) as max_bathroom_count
        from households_full_bathrooms
        join households_half_bathrooms on households_full_bathrooms.email = households_half_bathrooms.email
        ;
    ''')
    results_0 = cur.fetchall()

    cur.execute(f'''
        with households_half_bathrooms as (
            select Household.email, count(*) as half_bathroom_count from Household
            join HalfBathroom on Household.email = HalfBathroom.email group by Household.email
        ) select
            min(half_bathroom_count) as min_bathroom_count,
            round(avg(half_bathroom_count), 1) as avg_bathroom_count,
            max(half_bathroom_count) as max_bathroom_count
        from households_half_bathrooms
        ;
    ''')
    results_1 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, count(*) as full_bathroom_count from Household
            join FullBathroom on Household.email = FullBathroom.email group by Household.email
        ) select
            min(full_bathroom_count) as min_bathroom_count,
            round(avg(full_bathroom_count), 1) as avg_bathroom_count,
            max(full_bathroom_count) as max_bathroom_count
        from households_full_bathrooms
        ;
    ''')
    results_2 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_commodes
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        ),
        households_half_bathrooms as
        (
            select Household.email, number_of_commodes
            from Household
            join HalfBathroom on Household.email = HalfBathroom.email
        ) select
            min(households_full_bathrooms.number_of_commodes+households_half_bathrooms.number_of_commodes) as min_commodes_count,
            round(avg(households_full_bathrooms.number_of_commodes+households_half_bathrooms.number_of_commodes), 1) as avg_commodes_count,
            max(households_full_bathrooms.number_of_commodes+households_half_bathrooms.number_of_commodes) as max_commodes_count
        from households_full_bathrooms
        join households_half_bathrooms on households_full_bathrooms.email = households_half_bathrooms.email
        ;
    ''')
    results_3 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_sinks
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        ),
        households_half_bathrooms as (
            select Household.email, number_of_sinks
            from Household
            join HalfBathroom on Household.email = HalfBathroom.email
        ) select
            min(households_full_bathrooms.number_of_sinks+households_half_bathrooms.number_of_sinks) as min_sinks_count,
            round(avg(households_full_bathrooms.number_of_sinks+households_half_bathrooms.number_of_sinks), 1) as avg_sinks_count,
            max(households_full_bathrooms.number_of_sinks+households_half_bathrooms.number_of_sinks) as max_sinks_count
        from households_full_bathrooms
        join households_half_bathrooms on households_full_bathrooms.email = households_half_bathrooms.email
        ;
    ''')
    results_4 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_bidets
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        ),
        households_half_bathrooms as (
            select Household.email, number_of_bidets
            from Household
            join HalfBathroom on Household.email = HalfBathroom.email
        ) select
            min(households_full_bathrooms.number_of_bidets+households_half_bathrooms.number_of_bidets) as min_bidets_count,
            round(avg(households_full_bathrooms.number_of_bidets+households_half_bathrooms.number_of_bidets), 1) as avg_bidets_count,
            max(households_full_bathrooms.number_of_bidets+households_half_bathrooms.number_of_bidets) as max_bidets_count
        from households_full_bathrooms
        join households_half_bathrooms on households_full_bathrooms.email = households_half_bathrooms.email
        ;
    ''')
    results_5 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_bathtubs from Household
            join FullBathroom on Household.email = FullBathroom.email
        )
        select
            min(households_full_bathrooms.number_of_bathtubs) as min_bathtubs_count,
            round(avg(households_full_bathrooms.number_of_bathtubs), 1) as avg_bathtubs_count,
            max(households_full_bathrooms.number_of_bathtubs) as max_bathtubs_count
        from households_full_bathrooms
        ;
    ''')
    results_6 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_showers
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        )
        select
            min(households_full_bathrooms.number_of_showers) as min_showers_count,
            round(avg(households_full_bathrooms.number_of_showers), 1) as avg_showers_count,
            max(households_full_bathrooms.number_of_showers) as max_showers_count
        from households_full_bathrooms
        ;
    ''')
    results_7 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.email, number_of_tubs_showers
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        )
        select
            min(households_full_bathrooms.number_of_tubs_showers) as min_tubs_showers_count,
            round(avg(households_full_bathrooms.number_of_tubs_showers), 1) as avg_tubs_showers_count,
            max(households_full_bathrooms.number_of_tubs_showers) as max_tubs_showers_count
        from households_full_bathrooms
        ;
    ''')
    results_8 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Location.state, number_of_bidets
            from Household
            join Location on Household.postal_code = Location.postal_code
            join FullBathroom on Household.email = FullBathroom.email
        ),
        households_half_bathrooms as (
            select Location.state, number_of_bidets
            from Household
            join Location on Household.postal_code = Location.postal_code
            join HalfBathroom on Household.email = HalfBathroom.email
        ),
        max_state_sum_bidets_count as (
            select (sum(households_full_bathrooms.number_of_bidets) + sum(households_half_bathrooms.number_of_bidets)) as sum_bidets_count
            from households_full_bathrooms
            join households_half_bathrooms on households_full_bathrooms.state = households_half_bathrooms.state
            group by households_full_bathrooms.state
            order by sum_bidets_count desc
            limit 1
        ),
        state_sum_bidets_count as (
            select households_full_bathrooms.state,
            (sum(households_full_bathrooms.number_of_bidets) + sum(households_half_bathrooms.number_of_bidets)) as sum_bidets_count
            from households_full_bathrooms
            join households_half_bathrooms on households_full_bathrooms.state = households_half_bathrooms.state
            group by households_full_bathrooms.state
        )
        select state_sum_bidets_count.state, state_sum_bidets_count.sum_bidets_count from state_sum_bidets_count
        join max_state_sum_bidets_count on state_sum_bidets_count.sum_bidets_count = max_state_sum_bidets_count.sum_bidets_count
        order by state_sum_bidets_count.state
        ;
    ''')
    results_9 = cur.fetchall()

    cur.execute(f'''
        with households_full_bathrooms as (
            select Household.postal_code, number_of_bidets
            from Household
            join FullBathroom on Household.email = FullBathroom.email
        ),
        households_half_bathrooms as (
            select Household.postal_code, number_of_bidets
            from Household
            join HalfBathroom on Household.email = HalfBathroom.email
        ),
        max_postal_code_sum_bidets_count as (
            select (sum(households_full_bathrooms.number_of_bidets) + sum(households_half_bathrooms.number_of_bidets)) as sum_bidets_count
            from households_full_bathrooms
            join households_half_bathrooms on households_full_bathrooms.postal_code = households_half_bathrooms.postal_code
            group by households_full_bathrooms.postal_code
            order by sum_bidets_count desc
            limit 1
        ),
        postal_code_sum_bidets_count as (
            select households_full_bathrooms.postal_code,
            (sum(households_full_bathrooms.number_of_bidets) + sum(households_half_bathrooms.number_of_bidets)) as sum_bidets_count
            from households_full_bathrooms
            join households_half_bathrooms on households_full_bathrooms.postal_code = households_half_bathrooms.postal_code
            group by households_full_bathrooms.postal_code
        )
        select postal_code_sum_bidets_count.postal_code, postal_code_sum_bidets_count.sum_bidets_count
        from postal_code_sum_bidets_count
        join max_postal_code_sum_bidets_count on postal_code_sum_bidets_count.sum_bidets_count = max_postal_code_sum_bidets_count.sum_bidets_count
        order by postal_code_sum_bidets_count.postal_code
        ;
    ''')
    results_10 = cur.fetchall()

    cur.execute(f'''
        with households_full_primary_bathrooms as (
            select Household.email
            from Household
            join FullBathroom on Household.email = FullBathroom.email where FullBathroom.whether_primary = 1
        ),
        households_single_bathroom as (
            select email from (
                select Household.email, count(Household.email) as count_bathrooms from Household
                join FullBathroom on Household.email = FullBathroom.email
                group by Household.email
                union all
                select Household.email, count(Household.email) as count_bathrooms from Household
                join HalfBathroom on Household.email = HalfBathroom.email
                group by Household.email
            ) as households_all_bathrooms_union
            group by email
            having sum(count_bathrooms) = 1
        )
        select count(households_full_primary_bathrooms.email) as household_only_single_primary_bathroom_count
        from households_full_primary_bathrooms
        join households_single_bathroom on households_full_primary_bathrooms.email = households_single_bathroom.email
        ;
    ''')
    results_11 = cur.fetchall()

    data_0 = list(results_0)[0]
    data_1 = list(results_1)[0]
    data_2 = list(results_2)[0]
    data_3 = list(results_3)[0]
    data_4 = list(results_4)[0]
    data_5 = list(results_5)[0]
    data_6 = list(results_6)[0]
    data_7 = list(results_7)[0]
    data_8 = list(results_8)[0]
    data_9 =list(results_9)
    data_10 =list(results_10)
    data_11 =list(results_11)

    return render_template(
        'bathroom_statistics.html',
        title='Bathroom Statistics Report',
        data_0=data_0,
        data_1=data_1,
        data_2=data_2,
        data_3=data_3,
        data_4=data_4,
        data_5=data_5,
        data_6=data_6,
        data_7=data_7,
        data_8=data_8,
        data_9=data_9,
        data_10=data_10,
        data_11=data_11
    )

@app.route('/household_avg_by_radius', methods=['GET', 'POST'])
def household_avg_by_radius():
    data = [""]*5
    message = ""
    if request.method == 'POST':
        search_postal_code = request.form['search_postal_code']
        search_radius = request.form['search_radius']

        try:
            cur = mysql.connection.cursor()
            cur.execute(f'''
                with postal_codes_in_radius as (
                    with search_postal_code as (
                        select latitude * 3.14 / 180 as latr, longitude * 3.14 / 180 as lonr from Location
                        where postal_code = '{search_postal_code}'
                    ),
                    all_postal_code as (
                        select postal_code, latitude * 3.14 / 180 as latr, longitude * 3.14 / 180 as lonr
                        from Location
                    ),
                    all_postal_code_delta as (
                        select
                            all_postal_code.postal_code,
                            all_postal_code.latr - search_postal_code.latr as latrdelta, all_postal_code.lonr - search_postal_code.lonr as lonrdelta
                        from all_postal_code, search_postal_code
                    ),
                    all_postal_code_distance as (
                        select
                            all_postal_code.postal_code,
                            @a := SIN(latrdelta/2) * SIN(latrdelta/2) + COS(search_postal_code.latr) * COS(all_postal_code.latr) * SIN(lonrdelta/2) * SIN(lonrdelta/2) as a,
                            @c := 2 * ATAN2(SQRT(@a), SQRT(1-@a)) as c,
                            @d := 3958.75 * @c as d
                        from
                            all_postal_code_delta join all_postal_code on all_postal_code_delta.postal_code = all_postal_code.postal_code,
                            search_postal_code
                    )
                    select postal_code
                    from all_postal_code_distance where d <= '{search_radius}'
                ),
                bathrooms_count_avg_in_radius as (
                    select '1' as search_postal_code, round(avg(count_bathrooms_in_radius), 1) as avg_count_bathrooms
                    from (
                        select sum(count_bathrooms_in_radius) as count_bathrooms_in_radius from (
                            select Household.email, count(Household.email) as count_bathrooms_in_radius
                            from Household
                            join FullBathroom on Household.email = FullBathroom.email where Household.postal_code in (
                                select postal_code from postal_codes_in_radius
                            )
                            group by Household.email
                            union all
                            select Household.email, count(Household.email) as count_bathrooms_in_radius
                            from Household
                            join HalfBathroom on Household.email = HalfBathroom.email where Household.postal_code in (
                                select postal_code from postal_codes_in_radius
                            )
                            group by Household.email
                        ) as households_full_half_bathrooms
                        group by email
                    ) as households_full_half_bathrooms_combined
                ),
                bedrooms_count_avg_in_radius as (
                    select '1' as search_postal_code, round(avg(number_of_bedrooms), 1) as avg_count_bedrooms
                    from Household
                    where Household.postal_code in (select postal_code from postal_codes_in_radius)
                ),
                occupants_count_avg_in_radius as
                (
                    select '1' as search_postal_code, round(avg(number_of_occupants), 1) as avg_count_occupants
                    from Household
                    where Household.postal_code in (select postal_code from postal_codes_in_radius)
                ),
                ratio_of_commodes_to_occupants_in_radius as
                (
                    select '1' as search_postal_code, concat('1:', round((
                            select sum(sum_number_of_commodes_in_radius) as sum_number_of_commodes_in_radius
                            from (
                                select sum(FullBathroom.number_of_commodes) as
                                sum_number_of_commodes_in_radius from Household
                                join FullBathroom on Household.email = FullBathroom.email
                                where Household.postal_code in (
                                    select postal_code from postal_codes_in_radius
                                )
                                union all
                                select sum(HalfBathroom.number_of_commodes) as sum_number_of_commodes_in_radius
                                from Household
                                join HalfBathroom on Household.email = HalfBathroom.email
                                where Household.postal_code in (
                                    select postal_code from postal_codes_in_radius
                                )
                            ) as households_full_half_bathrooms
                        ) / (
                            select sum(number_of_occupants) as sum_number_of_occupants_in_radius from Household
                            where Household.postal_code in (select postal_code from
                            postal_codes_in_radius)),
                            2
                        )
                    ) as ratio_of_commodes_to_occupants
                ),
                appliances_count_avg_in_radius as (
                    select '1' as search_postal_code, round(avg(count_appliances_in_radius), 1) as avg_count_appliances
                    from (
                        select sum(count_appliances_in_radius) as count_appliances_in_radius from (
                            select Household.email, count(Household.email) as count_appliances_in_radius
                            from Household
                            join Cooker on Household.email = Cooker.email
                            where Household.postal_code in (select postal_code from postal_codes_in_radius)
                            group by Household.email
                            union all
                            select Household.email, count(Household.email) as count_appliances_in_radius
                            from Household
                            join Washer on Household.email = Washer.email
                            where Household.postal_code in (select postal_code from postal_codes_in_radius)
                            group by Household.email
                            union all
                            select Household.email, count(Household.email) as
                            count_appliances_in_radius from Household
                            join Dryer on Household.email = Dryer.email
                            where Household.postal_code in (select postal_code from postal_codes_in_radius)
                            group by Household.email
                            union all
                            select Household.email, count(Household.email) as
                            count_appliances_in_radius from Household
                            join RefrigeratorFreezer on Household.email = RefrigeratorFreezer.email
                            where Household.postal_code in (select postal_code from postal_codes_in_radius)
                            group by Household.email
                            union all
                            select Household.email, count(Household.email) as
                            count_appliances_in_radius from Household
                            join TV on Household.email = TV.email
                            where Household.postal_code in (select postal_code from postal_codes_in_radius)
                            group by Household.email
                        ) as households_all_appliances group by email
                    ) as households_all_appliances_combined
                ),
                most_common_heat_source_in_radius as (
                    select '1' as search_postal_code, heat_source as most_common_heat_source from (
                        select OvenHeatSource.heat_source
                        from Household
                        join OvenHeatSource on Household.email = OvenHeatSource.email
                        where Household.postal_code in (select postal_code from postal_codes_in_radius)
                        group by Household.email
                        union all
                        select Cooktop.heat_source
                        from Household
                        join Cooktop on Household.email = Cooktop.email
                        where Household.postal_code in (select postal_code from postal_codes_in_radius)
                        group by Household.email
                        union all
                        select Dryer.heat_source
                        from Household
                        join Dryer on Household.email = Dryer.email
                        where Household.postal_code in (select postal_code from postal_codes_in_radius)
                        group by Household.email
                    ) as households_all_appliances group by heat_source
                    order by count(heat_source) desc limit 1
                )
                select
                    bathrooms_count_avg_in_radius.avg_count_bathrooms,
                    bedrooms_count_avg_in_radius.avg_count_bedrooms,
                    occupants_count_avg_in_radius.avg_count_occupants,
                    ratio_of_commodes_to_occupants_in_radius.ratio_of_commodes_to_occupants,
                    appliances_count_avg_in_radius.avg_count_appliances,
                    most_common_heat_source_in_radius.most_common_heat_source
                from bathrooms_count_avg_in_radius
                join bedrooms_count_avg_in_radius on bathrooms_count_avg_in_radius.search_postal_code = bedrooms_count_avg_in_radius.search_postal_code
                join occupants_count_avg_in_radius on bathrooms_count_avg_in_radius.search_postal_code = occupants_count_avg_in_radius.search_postal_code
                join ratio_of_commodes_to_occupants_in_radius on bathrooms_count_avg_in_radius.search_postal_code = ratio_of_commodes_to_occupants_in_radius.search_postal_code
                join appliances_count_avg_in_radius on bathrooms_count_avg_in_radius.search_postal_code = appliances_count_avg_in_radius.search_postal_code
                join most_common_heat_source_in_radius on bathrooms_count_avg_in_radius.search_postal_code = most_common_heat_source_in_radius.search_postal_code
                ;
            ''')
            results_0 = cur.fetchall()
            data = list(results_0)[0]
        except:
            message = "Postal Code is invalid!"
    return render_template('household_avg_by_radius.html', title='Household Avg by Radius Report', data=data, msg=message)


if __name__ == '__main__':
    app.run(debug=True)


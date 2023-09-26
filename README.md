# Household_Insight_Web_App
Track various characteristics of households and allow users to view different reports based on their inputs

Setting Up
1. Clone the Repository

```
git clone https://github.com/xfng/Household_Insight_Web_App.git
cd Household_Insight_Web_App
```

2. Create a Virtual Environment and Activate It

```
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

4. Set up the MySQL Database


Start the MySQL server:

If you have MySQL installed as a service, you might need to start it first:


```
mysql.server start
```

Login to MySQL:

Access your MySQL server with the appropriate credentials:


```
mysql -u root -p
```

When prompted, enter your password.

Import the Schema from the SQL File:

Once logged in, you can import the SQL file directly from the MySQL prompt:


```
source database_schema.sql;
```

5. Running the App
```
export FLASK_APP=app.py  
export FLASK_ENV=development 
flask run
```

Visit http://127.0.0.1:5000/ in your browser to access the app.
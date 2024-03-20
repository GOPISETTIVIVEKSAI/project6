from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('response.html',context='you are in home page')

@app.route('/user',methods=['GET'])
def user():
    return render_template('form.html',path='/user-data')
 
import pymysql as sql
my_connection=sql.connect(
    host='localhost',
    user='root',
    password='password',
    database='project'
)
my_cursor=my_connection.cursor()
@app.route('/user-data',methods=['POST'])
def user_data():
    u_id = request.form['u_id']
    u_name =request.form['u_name']
    u_age =request.form['u_age']
    u_salary=request.form['u_salary']
#before typing below create database project and create table user_data
    query='''
        insert into user_data(u_id,u_name,u_age,u_salary)
        values(%s,%s,%s,%s);
        '''
    values = (u_id,u_name,u_age,u_salary)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('response.html',context='Data Inserted,check in mysql')

@app.route('/update',methods=['GET'])
def update():
    return render_template('update.html',path='/update-form')
@app.route('/update-form',methods=['POST'])
def update_form():
    u_id=request.form['u_id']
    #u_name=request.form['u_name']
    u_age=request.form['u_age']
    #u_salary=request.form['u_salary']
    query='''
        update user_data
        set u_age =(%s)
        where u_id=(%s)
    '''
    values=(u_age,u_id)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('update.html',context=f'u_id {u_id} age has updated')

@app.route('/delete/<_id>',methods=['GET'])
def delete(_id):
    query='''
        delete from user_data
        where u_id=%s;
        '''
    values=(_id)
    my_cursor.execute(query,values)
    my_connection.commit()
    return render_template('response.html',context=f'user having {_id} has been deleted')

app.run()
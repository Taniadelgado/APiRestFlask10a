from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'personas'
mysql = MySQL(app)

# settings  
app.secret_key = 'mysecretkey' 

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        password = request.form['password']
        edad = request.form['edad']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO personas (nombres, apellidos, identificacion, email, password, edad) VALUES (%s, %s, %s, %s, %s, %s)',
        (nombres, apellidos, identificacion, email, password, edad))
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM personas WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        indentificacion = request.form['identificacion']
        email = request.form['email']
        password = request.form['password']
        edad = request.form['edad']
        cur=mysql.connection.cursor()
        cur.execute("""
        UPDATE personas
        SET nombres = %s,
            apellidos = %s,
            identificacion = %s,
            email = %s,
            password = %s,
            edad = %s
        WHERE id = %s
        """, (nombres, apellidos, indentificacion, email, password, edad,id))
        mysql.connection.commit()
        flash('Contact Update Successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<int:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM personas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
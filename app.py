from flask import Flask,render_template,request, url_for, redirect
import sqlite3 as sql
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER="static/uploads"
web=Flask(__name__)
web.secret_key="secret key"
web.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
@web.route('/')
def index():
    return render_template('index.html')
@web.route('/salbar',methods=['GET','POST'])
def salbarInsert():
    if request.method=='POST':
        con=sql.connect('Employee.db')
        cur=con.cursor()
        sname=request.form['sname']
        image=request.files['image']
        if image and allowed_file(image.filename):
            filename=secure_filename(image.filename)
            zurag=os.path.join(web.config['UPLOAD_FOLDER'],filename)
            image.save(os.path.join(web.config['UPLOAD_FOLDER'],filename))
        cur.execute(f'INSERT INTO salbar VALUES(null, "{sname}","{zurag}")')
        con.commit()
        return redirect(url_for('salbarInsert'))
    elif request.method=='GET':
        con=sql.connect('Employee.db')
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute(f'SELECT * from salbar')
        data=cur.fetchall()
        return render_template('salbar.html',salbaruud=data)
@web.route('/ajiltan',methods=['GET','POST'])
def ajiltan():
    if request.method=='POST':
        con=sql.connect('Employee.db')
        cur=con.cursor()
        sid=request.form['sid']
        ajiltanNer=request.form['ajiltanner']
        cur.execute(f'INSERT INTO ajiltan VALUES(null,"{ajiltanNer}","{sid}")')
        con.commit()
        return redirect(url_for('ajiltan'))
    elif request.method=='GET':
        con=sql.connect('Employee.db')
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute('Select ajiltanid, ajiltanner, sname from ajiltan a INNER JOIN salbar s on a.sid=s.sid')
        data=cur.fetchall()
        cur1=con.cursor()
        cur1.execute('select * from salbar')
        salbar=cur1.fetchall()
    return render_template('ajiltan.html',ajiltnuud=data,salbaruud=salbar)
@web.route('/delete/<int:id>',methods=['GET','POST'])
def ustgah(id):
    con=sql.connect('Employee.db')
        # холбогдсон бааз дээрээ комманд оруулах боломжтой
    cur=con.cursor()
        # cursor обьект дээр л query бичиж болдог ямар функцээр query бичдэг вэ гэвэл execute()
    cur.execute(f'DELETE FROM salbar WHERE sid={id}')
    con.commit()
    return redirect(url_for('salbarInsert'))
@web.route('/edit/<int:id>',methods=['GET','POST'])
def zasah(id):
    if request.method=='GET':
        con=sql.connect('Employee.db')
        con.row_factory=sql.Row
        # холбогдсон бааз дээрээ комманд оруулах боломжтой
        cur=con.cursor()
        # cursor обьект дээр л query бичиж болдог ямар функцээр query бичдэг вэ гэвэл execute()
        cur.execute(f"select * from salbar where sid={id}")
        data=cur.fetchall()
        return render_template('zasah.html',salbar=data)
    elif request.method=="POST":
        con=sql.connect('Employee.db')
        cur=con.cursor()
        sname=request.form['sname']
        image=request.files['image']
        if image and allowed_file(image.filename):
            filename=secure_filename(image.filename)
            zurag=os.path.join(web.config['UPLOAD_FOLDER'],filename)
            image.save(os.path.join(web.config['UPLOAD_FOLDER'],filename))
        cur.execute(f"UPDATE salbar set sname='{sname}',image='{zurag}' where sid={id}")
        con.commit()
        return redirect(url_for('salbarInsert'))
@web.route('/ajustgah/<int:id>',methods=['GET','POST'])
def ajustgah(id):
    con=sql.connect('Employee.db')
        # холбогдсон бааз дээрээ комманд оруулах боломжтой
    cur=con.cursor()
        # cursor обьект дээр л query бичиж болдог ямар функцээр query бичдэг вэ гэвэл execute()
    cur.execute(f'DELETE FROM ajiltan WHERE ajiltanid={id}')
    con.commit()
    return redirect(url_for('ajiltan'))
@web.route('/ajiltanEdit/<int:id>',methods=['GET','POST'])
def ajiltanEdit(id):
    if request.method=='GET':
        con=sql.connect('Employee.db')
        con.row_factory=sql.Row
        # холбогдсон бааз дээрээ комманд оруулах боломжтой
        cur=con.cursor()
        # cursor обьект дээр л query бичиж болдог ямар функцээр query бичдэг вэ гэвэл execute()
        cur.execute(f'Select ajiltanid, ajiltanner, sname from ajiltan a INNER JOIN salbar s on a.sid=s.sid WHERE a.ajiltanid={id}')
        data=cur.fetchall()
        cur.execute('select * from salbar')
        sname=cur.fetchall()
        return render_template('ajiltanEdit.html',ajiltnuud=data,sname=sname)
    elif request.method=="POST":
        con=sql.connect('Employee.db')
        cur=con.cursor()
        ajiltanname=request.form['ajiltanner']
        sname=request.form['sname']
        cur.execute(f"UPDATE ajiltan set ajiltanner='{ajiltanname}',sid={sname} WHERE ajiltanid={id}")
        con.commit()
        return redirect(url_for('ajiltan'))

if __name__=="__main__":
    web.run(debug=True)

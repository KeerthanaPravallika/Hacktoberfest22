

import os

import matplotlib.pyplot as plt
import matplotlib.dates as md

from datetime import datetime



from flask import Flask, redirect
from flask import render_template
from flask import request, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "mainDB.sqlite3")
db = SQLAlchemy(app)


## Models
class user(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String)
    def __init__(self, usn, pwd):
        self.username = usn
        self.password = pwd

class tracker(db.Model):
    __tablename__ = 'Trackers'
    tracker_id = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    tuser_id = db.Column(db.Integer, db.ForeignKey(user.user_id), nullable = False)
    tracker_type = db.Column(db.String, nullable=False)
    tracker_name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    min_val = db.Column(db.String)
    max_val = db.Column(db.String)
    options = db.Column(db.String)
    def __init__(self, tname, ttype, tuid, tdesc, minv, maxv, opts):
        self.tracker_type = ttype
        self.tracker_name = tname
        self.tuser_id = tuid
        self.description = tdesc
        self.min_val = minv
        self.max_val = maxv
        self.options = opts

class userlogs(db.Model):
    __tablename__ = 'UserLogs'
    log_id = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    ltracker_id = db.Column(db.Integer, db.ForeignKey(tracker.tracker_id), nullable = False)
    luser_id = db.Column(db.Integer, db.ForeignKey(user.user_id), nullable = False)
    value = db.Column(db.String, nullable = False)
    note = db.Column(db.String)
    TimeStamp = db.Column(db.String, nullable = False)
    def __init__(self, ltid, luid, val, note, time):
        self.ltracker_id = ltid
        self.luser_id = luid
        self.value = val
        self.note = note
        self.TimeStamp = time



db.create_all()
db.session.commit()
app.app_context().push()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

## Controllers
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template("login.html", message='Welcome Back!')
    else:
        # check if user exists
        # check if password is correct
        usn = request.form['username']
        pwd = request.form['password']
        print(usn, pwd)
        curr_user = user.query.filter_by(username=usn).first()
        if not curr_user:
            return render_template("login.html", message='User does not exist. Enter correct Username.')
        if curr_user.password != pwd:
            return render_template("login.html", message='Incorrect Password.')
    return redirect(url_for('show_dashboard', username=usn))

@app.route('/<username>/dashboard')
def show_dashboard(username):
    curr_user = user.query.filter_by(username=username).first()
    trackers = tracker.query.filter_by(tuser_id=curr_user.user_id).all()
    last_log = []
    for t in trackers:
        last_log.append((userlogs.query.filter_by(luser_id=curr_user.user_id, ltracker_id=t.tracker_id).order_by(userlogs.TimeStamp.desc()).first(), t.tracker_name))
        
    tracker_names = []
    print(last_log)
    for t in trackers:
        tracker_names.append(t.tracker_name)
    print(tracker_names)
    not_yet_set = list(set(tracker_names) - set([l[1] for l in last_log if l[0] != None]))
    print([l[1] for l in last_log if l[0] != None])
    last_log = list(set([l for l in last_log]) - set(l for l in last_log if l[0] == None))
    print([l[1] for l in last_log])
    print(not_yet_set)
    for n in not_yet_set:
        obj = userlogs(0, 0, 'Not Yet Set', '', '----------')
        last_log.append((obj, n))
    for l in last_log:
        print(l[0].value, l[0].note, l[0].TimeStamp)
    print(trackers)
    return render_template("dashboard.html", username=username, trackers=trackers, last_log=last_log)
    
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template("signup.html", message='Create Account to get started!')
    else:
        # check if user is unique
        usn = request.form['username']
        pwd = request.form['password']
        print(usn, pwd)
        obj1 = user(usn, pwd)
        try:
            db.session.add(obj1)
            db.session.commit()
        except:
            db.session.rollback()
            return render_template("signup.html", message='User already exists. Please Choose a different Username.')
    return render_template("login.html", message='Profile Created Successfully. Login to access dashboard.')

@app.route('/<username>/update', methods=['GET', 'POST'])
def update_user(username):
    if request.method == 'GET':
        return render_template("update_user.html", username=username, message="Update User Profile.")
    else:
        nusn = request.form['username']
        npwd = request.form['password']
        try:
            curr_user = user.query.filter_by(username=username).first()
            curr_user.username = nusn
            curr_user.password = npwd
            db.session.commit()
        except:
            db.session.rollback()
            return render_template("update_user.html", username=username, message="User already exists. Please Choose a different Username.")
        return render_template("login.html", message='Profile Updated Successfully. Login to access dashboard.')

@app.route('/<username>/delete')
def delete_user(username):
    try:
        curr_user = user.query.filter_by(username=username).first()
        trackers = tracker.query.filter_by(tuser_id=curr_user.user_id).all()
        for t in trackers:
            userlogs.query.filter_by(luser_id=curr_user.user_id, ltracker_id=t.tracker_id).delete()
            tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=t.tracker_id).delete()
        user.query.filter_by(username=username).delete()
        db.session.commit()
    except:
        print("Something went wrong :(")
        db.session.rollback()
    return redirect("/")

@app.route('/<username>/tracker/add', methods=['GET', 'POST'])
def add_tracker(username):
    if request.method == 'GET':
        print(username)
        return render_template("add_tracker.html", username=username, message="Enter details of the tracker.")
    else:
        curr_user = user.query.filter_by(username=username).first()
        tuid = curr_user.user_id
        ttype = request.form['ttype']
        tname = request.form['tname']
        tdesc = request.form['tdesc']
        tminv = request.form['min_val']
        tmaxv = request.form['max_val']
        topts = request.form['options']
        print(topts, ttype)
        if topts:
            tminv = "None"
            tmaxv = "None"
        elif ttype == 'Real' and (not tminv or not tmaxv):
            return render_template("add_tracker.html", username=username, message="Both minimum and maximum value must be entered if tracker is numeric.")
        elif ttype == 'Real' and (not isfloat(tminv) or not isfloat(tmaxv)):
            return render_template("add_tracker.html", username=username, message="Minimum and maximum value must be numeric.")
        elif ttype == 'SMCQ' and not topts:
            return render_template("add_tracker.html", username=username, message="Must enter options if tracker is of MCQ type")
        elif tminv:
            topts = "None"
        obj = tracker(tname, ttype, tuid, tdesc, tminv, tmaxv, topts)
        try:
            db.session.add(obj)
            db.session.commit()
        except:
            print("Something went wrong")
            db.session.rollback()
        print(tuid, tname, ttype, tdesc, tminv, tmaxv, topts)
        print(username)
    return redirect(url_for('show_dashboard', username=username))

@app.route('/<username>/<tracker_id>/delete')
def delete_tracker(username, tracker_id):
    try:
        curr_user = user.query.filter_by(username=username).first()
        userlogs.query.filter_by(luser_id=curr_user.user_id, ltracker_id=tracker_id).delete()
        tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(url_for('show_dashboard', username=username))

@app.route('/<username>/<tracker_id>/update', methods=['GET', 'POST'])
def update_tracker(username, tracker_id):
    if request.method == 'GET':
        curr_user = user.query.filter_by(username=username).first()
        tracker_info = tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).first()
        return render_template("update_tracker.html", username=username, tracker_info=tracker_info, tracker_id=tracker_id)
    else:
        curr_user = user.query.filter_by(username=username).first()
        tracker_info = tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).first()
        tname = request.form['tname']
        tdesc = request.form['tdesc']
        tracker_info.tracker_name = tname
        tracker_info.description = tdesc
        db.session.commit()
    return redirect(url_for('show_dashboard', username=username))
    
@app.route('/<username>/<tracker_id>/<tracker_name>')
def show_tracker_screen(username, tracker_id, tracker_name):
    plot_graph = 'False'
    curr_user = user.query.filter_by(username=username).first()
    tracker_info = tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).first()
    print(tracker_info)
    print('************************************************************')
    recent_logs = userlogs.query.filter_by(ltracker_id=tracker_info.tracker_id, luser_id=tracker_info.tuser_id).order_by(userlogs.TimeStamp.desc()).limit(5).all()
    if tracker_info.tracker_type == 'Real':
        all_logs = userlogs.query.filter_by(ltracker_id=tracker_info.tracker_id, luser_id=tracker_info.tuser_id).order_by(userlogs.TimeStamp.desc()).all() #change?
        if len(all_logs) > 1:
            plot_graph = 'True'
        timestamps = [str(l.TimeStamp)[:10] + " " + str(l.TimeStamp)[11:] for l in all_logs]
        print(timestamps)
        dates = [datetime.fromisoformat(t) for t in timestamps]
        print(dates)
        values = [float(l.value) for l in all_logs]
        plt.subplots_adjust(bottom=0.2)
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%m-%d-%Y %H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(dates,values)
        plt.savefig('./static/graph.png')
        plt.close()
    if tracker_info.tracker_type == 'SMCQ':
        all_logs = userlogs.query.filter_by(ltracker_id=tracker_info.tracker_id, luser_id=tracker_info.tuser_id).order_by(userlogs.TimeStamp.desc()).all() #change?
        if len(all_logs) > 1:
            plot_graph = 'True'
        timestamps = [str(l.TimeStamp)[:10] + " " + str(l.TimeStamp)[11:] for l in all_logs]
        print(timestamps)
        dates = [datetime.fromisoformat(t) for t in timestamps]
        print(dates)
        values = [str(l.value) for l in all_logs]
        plt.subplots_adjust(bottom=0.2)
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%m-%d-%Y %H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        plt.scatter(dates,values)
        plt.savefig('./static/graph.png')
        plt.close()

    return render_template("tracker_screen.html", username=username, tracker_info=tracker_info, recent_logs=recent_logs, plot_graph=plot_graph)

@app.route('/<username>/<tracker_id>/<tracker_name>/log', methods=['GET', 'POST'])
def user_log(username, tracker_id, tracker_name):
    if request.method == 'GET':
        curr_user = user.query.filter_by(username=username).first()
        tracker_info = tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).first()
        timestamp = str(datetime.now())[:16]
        if tracker_info.tracker_type == 'SMCQ':
            options = str(tracker_info.options).split(',')
            print(options)
            return render_template("log_smcq.html", username=username, tracker_info=tracker_info, options=options)
        if tracker_info.tracker_type == 'Real':
            return render_template("log_numeric.html", username=username, tracker_info=tracker_info, message="Enter Log value")
    else:
        curr_user = user.query.filter_by(username=username).first()
        tracker_info = tracker.query.filter_by(tuser_id=curr_user.user_id, tracker_id=tracker_id).first()
        curr_val = request.form["val"]
        curr_note = request.form["note"]
        curr_time = request.form["timestamp"]
        print(curr_val, curr_note, curr_time)
        if tracker_info.tracker_type == 'Real':
            if not isfloat(curr_val):
                return render_template("log_numeric.html", username=username, tracker_info=tracker_info, message="Value must be numeric")
            if 2 * float(curr_val) > float(tracker_info.max_val) or 2 * float(curr_val) < float(tracker_info.min_val):
                return render_template("log_numeric.html", username=username, tracker_info=tracker_info, message="Value must be between " + tracker_info.min_val + " and " + tracker_info.max_val)
        obj = userlogs(tracker_id, curr_user.user_id, 2 * float(curr_val), curr_note, curr_time)
        try:
            db.session.add(obj)
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('show_tracker_screen', username=username, tracker_id=tracker_id, tracker_name=tracker_info.tracker_name))

@app.route('/<username>/<log_id>/update_log', methods=['GET', 'POST'])
def update_log(username, log_id):
    if request.method == 'GET':
        log_info = userlogs.query.filter_by(log_id=log_id).first()
        tracker_info = tracker.query.filter_by(tracker_id=log_info.ltracker_id).first()
        print(log_info.log_id, log_info.ltracker_id, log_info.value)
        if tracker_info.tracker_type == 'Real':
            return render_template("update_numeric.html", username=username, log_info=log_info, message="Enter information")
        if tracker_info.tracker_type == 'SMCQ':
            options = str(tracker_info.options).split(',')
            return render_template("update_smcq.html", username=username, log_info=log_info, options=options)
    else:
        log_info = userlogs.query.filter_by(log_id=log_id).first()
        tracker_info = tracker.query.filter_by(tracker_id=log_info.ltracker_id).first()
        print(log_info.log_id, log_info.ltracker_id, log_info.value)
        curr_val = request.form["val"]
        curr_note = request.form["note"]
        curr_time = request.form["timestamp"]
        if tracker_info.tracker_type == 'Real':
            if not isfloat(curr_val):
                return render_template("update_numeric.html", username=username, log_info=log_info, message="Value must be numeric")
            if float(curr_val) > float(tracker_info.max_val) or float(curr_val) < float(tracker_info.min_val):
                return render_template("update_numeric.html", username=username, log_info=log_info, message="Value must be between " + tracker_info.min_val + " and " + tracker_info.max_val)
        obj = userlogs.query.filter_by(log_id=log_id).first()
        try:
            obj.value = curr_val
            obj.note = curr_note
            obj.TimeStamp = curr_time
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('show_tracker_screen', username=username, tracker_id=log_info.ltracker_id, tracker_name=tracker_info.tracker_name))

@app.route('/<username>/<log_id>/delete_log')
def delete_log(username, log_id):
    log_info = userlogs.query.filter_by(log_id=log_id).first()
    tracker_info = tracker.query.filter_by(tracker_id=log_info.ltracker_id).first()
    try:
        userlogs.query.filter_by(log_id=log_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(url_for('show_tracker_screen', username=username, tracker_id=tracker_info.tracker_id, tracker_name=tracker_info.tracker_name))


@app.route('/<username>/<tracker_id>/all_stats')
def show_all_logs(username, tracker_id):
    curr_user = user.query.filter_by(username=username).first()
    tracker_info = tracker.query.filter_by(tracker_id=tracker_id).first()
    all_logs = userlogs.query.filter_by(luser_id=curr_user.user_id, ltracker_id=tracker_id).all()
    return render_template('all_logs_screen.html', username=username, tracker_info=tracker_id, all_logs=all_logs)



if __name__ == "__main__":
    app.run(
        host='localhost', port=5000
    )
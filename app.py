from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import db, User, Event
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        hashed_pw = generate_password_hash(request.form['password'])
        new_user = User(name=request.form['name'], email=request.form['email'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    events = Event.query.all()
    return render_template('dashboard.html', events=events)

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        new_event = Event(
            title=request.form['title'],
            category=request.form['category'],
            organizer=request.form['organizer'],
            date=request.form['date'],
            venue=request.form['venue'],
            description=request.form['description']
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_event.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

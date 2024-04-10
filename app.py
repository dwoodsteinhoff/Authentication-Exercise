from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import SignUpForm, UserForm,FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_exer"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():

    return render_template('index.html')

@app.route('/register', methods=["GET","POST"])
def register_user():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another Username')
            form.email.errors.append('Email already in use')
            return render_template('register.html', form=form)
        
        session['username'] = new_user.username
        flash('Account Created Successfully', "success")

        return redirect(f'/users/{new_user.username}')
    
    else:
        return render_template('register.html', form = form)
    
@app.route('/users/<string:username>')
def show_user_stuff(username):
    
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    the_user = User.query.get_or_404(username)

    all_feedback = Feedback.query.all()    

    return  render_template('user.html', user=the_user, all_feedback = all_feedback)

@app.route('/users/<string:username>/delete', methods=["POST"])
def delete_user(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    the_user = User.query.get_or_404(username)
    
    all_feedback = Feedback.query.all()

    for feedback in all_feedback:
        if feedback.username == username:
            db.session.delete(feedback)

    db.session.delete(the_user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<string:username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user = username

        add_feedback = Feedback(title=title, content=content, username=user)

        db.session.add(add_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    
    else:

        return render_template('feedback.html',form=form)
    
@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        to_update = Feedback.query.get_or_404(feedback_id)
        to_update.title = title
        to_update.content = content
        db.session.add(to_update)
        db.session.commit()

        return redirect(f'/users/{to_update.user.username}')
    
    else:
        return render_template('update_feedback.html',form=form)
    
@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)

    if feedback.user.username == session["username"]:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback Deleted', "info")
        return redirect (f'/users/{feedback.user.username}')
    
    return redirect (f'/users/{feedback.user.username}')

@app.route('/login', methods=["GET", "POST"])
def login_user():

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username

            return redirect(f'/users/{user.username}')
        
        else:
            form.username.errors =['Invalid username/password']
        
    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET"])
def logout_user():
    session.pop('username')
    flash('Goodbye!', "info")
    return redirect('/')
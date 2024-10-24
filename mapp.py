from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '30aef842dea691068e0f7697d64cea14')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///colossus_technovation_ltd.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for BlogPost
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# ContactForm model
class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)  # Added phone_number field
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# About route
@app.route('/services')
def services():
    return render_template('services.html')

# Services route
@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

# Events route
@app.route('/events')
def events():
    return render_template('events.html')

# Blog route with GET and POST methods
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        
        if not title or not author or not content:
            flash('All fields are required!', 'error')
        else:
            new_post = BlogPost(title=title, author=author, content=content)
            try:
                db.session.add(new_post)
                db.session.commit()
                flash('Blog post created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error! Could not create blog post. Error: {str(e)}', 'error')
        
        return redirect(url_for('blog'))
    
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

# Contact route with GET and POST methods
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        message = request.form['message']
        
        if not name or not email or not phone_number or not message:
            flash('All fields are required!', 'error')
        else:
            new_message = ContactForm(name=name, email=email, phone_number=phone_number, message=message)
            try:
                db.session.add(new_message)
                db.session.commit()
                flash('Message sent successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error! Could not send message. Error: {str(e)}', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Route to view messages
@app.route('/view_messages')
def view_messages():
    with app.app_context():
        messages = ContactForm.query.order_by(ContactForm.date_sent.desc()).all()
        return render_template('view_messages.html', messages=messages)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        
        db.create_all()
    app.run(debug=True)

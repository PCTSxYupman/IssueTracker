from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issues.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Issue model for the database
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=True)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    issues = Issue.query.all()
    return render_template('issues.html', issues=issues)

@app.route('/create', methods=['GET', 'POST'])
def create_issue():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = request.form['status']
        assigned_to = request.form['assigned_to']

        # Create a new issue
        new_issue = Issue(
            title=title,
            description=description,
            priority=priority,
            status=status,
            assigned_to=assigned_to
        )

        # Add to the database
        db.session.add(new_issue)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_issue.html')

if __name__ == '__main__':
    app.run(debug=True)

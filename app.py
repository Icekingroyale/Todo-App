from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# init the app
app = Flask(__name__)

# link database with app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


# Create a class for the database table ie database model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Task {self.id}'


with app.app_context():
    db.create_all()


# Routes to Webpages
# Home page
@app.route('/', methods=['POST', 'GET'])
def index():
    # Add a Task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error:{e}')
            return f'Error:{e}'

    else:
        # Retrieve all tasks from the database
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/edit/<int:id>', methods=['GEt', 'POST'])
def edit(id: int):
    task_to_edit = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'ERROR:{e}'

    else:
        return render_template('edit.html', task=task_to_edit)


@app.route('/delete/<int:id>')
def delete(id: int):
    task_to_delete = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'ERROR:{e}'


# running in debug mode
if __name__ == '__main__':
    app.run(debug=True)

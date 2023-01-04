from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
# Track modification needed to be false.
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    descript = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


#this is for homepage.
@app.route('/', methods=['GET', 'POST'])
def NotesApp_On():
    if request.method == "POST":
        Title = request.form['title']
        Descript = request.form['descript']
        todo = Todo(title=Title, descript=Descript)
        db.session.add(todo)
        db.session.commit()
 
    allTodo = Todo.query.all()
    #Todo app appeared on screen.
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        descript = request.form['descript']
        todo = Todo.query.filter_by(sno=sno).first()  
        todo.title = title
        todo.descript = descript
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()  
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    #this to get the record you want to delete , first shows --> the record 
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

#Driver Code.

if __name__ == "__main__":
    app.run(debug=True)

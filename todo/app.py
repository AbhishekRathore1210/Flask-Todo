from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    Topic=db.Column(db.String(100),nullable=False)
    Description=db.Column(db.String(500),nullable=False)
    DateTime=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Topic}"
    
    
with app.app_context():
    db.create_all()

@app.route("/",methods=['GET','POST'])
def hello_world():
    if(request.method=="POST"):
        t=request.form['topic']
        d=request.form['desc']
        todo=Todo(Topic=t, Description=d)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route("/delete/<int:Sno>")
def delete(Sno):
    todo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:Sno>", methods=['GET','POST'])
def update(Sno):
    todo = Todo.query.filter_by(Sno=Sno).first()
    if(request.method=="POST"):
        t=request.form['topic']
        d=request.form['desc']
        todo.Topic=t
        todo.Description=d
        db.session.commit()
        return redirect("/")
    return render_template('update.html',todo=todo)

if __name__ == "__main__":
        app.run(debug=True)



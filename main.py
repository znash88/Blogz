from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog2:zackattack1@localhost:8889/build-a-blog2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
   
    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        if request.form['blog'] == "":
            error = "Please insert valid blog name" 
            return render_template('todos.html' ,error=error)  
        else:
            db.session.add(new_blog)
            db.session.commit()
    
    blogs = Blog.query.all()
    
    return render_template('todos.html',title="Build-a-Blog!", blogs=blogs)

@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.add(blog)
    db.session.commit()

    return redirect('/')

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(title=blog_name, body=blog_body)
        if request.form['title'] == "":
            error = "Please insert valid blog name" 
            return render_template('blogs.html' ,error=error)  
        else:
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.all()
            return redirect("/")

    if request.method == 'GET':
        return render_template('blogs.html', title="New Blog Post")



@app.route("/blog")
def blog():
    
    blog_id = request.args.get("id") 
    blog = Blog.query.filter_by(id=blog_id).first()   
    
    return render_template('pre_blogs.html', blog=blog)



if __name__ == '__main__':
    app.run()
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-blog:Cosmos314@localhost:8889/build-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self,name,body):
        self.name = name 
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'] ) 
def blog(): 
 
    blogpost = Blog.query.all()

    return render_template('index.html',title="Build a blog",blogpost=blogpost) 


@app.route('/add', methods = ['POST','GET'])
def newpost():
    newpost_error = ''
    body_error = ''
    
    if request.method == "GET":
        return render_template('newpost.html',title='New blog entry',newpost_error=newpost_error, body_error=body_error)    

    if request.method == 'POST':
        blog_name = request.form['newpost']
        blog_body = request.form['body']
        new_post = Blog(blog_name,blog_body)
        db.session.add(new_post)
        db.session.commit()

        if blog_name == '':
            newpost_error = 'Your new blog needs a title'
    
        elif blog_body=='':
            body_error = 'You need to add some content to your blog post'    

    if not newpost_error and not body_error:    
    
        return redirect('/blog')
    else:
        return render_template('newpost.html',title='New blog entry',newpost_error=newpost_error, body_error=body_error)


  



if __name__ == '__main__':
    app.run()
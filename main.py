from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:supahotboi@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(200))

	def __init__(self, title, body):
		self.title = title
		self.body = body

@app.route('/')
def index():
	return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

	blogs = Blog.query.all()

	return render_template('blog.html', title="Devan's Blog", blogs=blogs)

@app.route('/post/<id>')
def post(id):

	blog = Blog.query.filter_by(id=id).first()

	if not blog:
		#Flash message
		return redirect('/')

	return render_template('post.html', title=blog.title, body=blog.body)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
	if request.method == 'POST':
		title = request.form.get('blogtitle')
		body = request.form.get('blogbody')

		new_blog = Blog(title,body)
		db.session.add(new_blog)
		db.session.commit()

		return render_template('post.html', title=title, body=body)

	return render_template('newpost.html')

@app.route('/deleteblogs', methods=['POST', 'GET'])
def deleteblogs():
	db.drop_all()
	db.create_all()
	return redirect('/blog')

if __name__ == '__main__':
	app.run()
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import Column, String,create_engine, Integer, Table, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
Base = declarative_base()


class User(Base):  
    __tablename__ = "user"  
      
    id = Column("id", Integer, primary_key=True)  
    name = Column("name", String)  
    password = Column("password", String)  
      
      
    def __init__(self, id=None, name=None,  password=None):  
        self.id = id  
        self.name = name  
        self.password = password  
     
          
    def __repr__(self):  
        return "<User '{name}' '{password}' >".format(name=self.name,  password=self.password)  




engine = create_engine('mysql+pymysql://testuser:password@localhost:3306/BucketList')

metadata = MetaData(engine)

user=Table('user',metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String(20)),
    Column('password',String(40)),
    )


metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/login',methods=['POST'])
def login():

		_name = request.form['inputName']
		_password = request.form['inputPassword']

		users = session.query(User).filter(User.name == _name).all()

		if len(users) is 0:

			return json.dumps({'message':'user %s not exist !' % _name})

		else:

			user = users[0]

			if user.password == _password:
				#return json.dumps({'message': 'welcome %s !' % _name})
				return render_template("welcome.html",title = user.name , user = user)
			else:
				return json.dumps({'message': 'password  not match !'})





@app.route('/signUp',methods=['POST','GET'])
def signUp():

		_name = request.form['inputName']
		_password = request.form['inputPassword']
		if _name and _password:
			_hashed_password=_password
			data = session.query(User).filter(User.name == _name).all()

			all_users=session.query(User).all()

			if len(data) is 0:
				user1 = User(len(all_users) + 1 ,_name,_hashed_password)
				session.add(user1)
				session.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'message':'User %s already exist !' % _name})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})




if __name__ == "__main__":
    app.run(port=5002)

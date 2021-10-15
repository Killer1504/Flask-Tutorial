from flaskr import db, User, Post
db.drop_all()
db.create_all()

user_1 = User(username="ThanhHung", email="thanhhung@gmail.com", password='password')
db.session.add(user_1)

user_2 = User(username="Kimduyen", email="Kimduyen@gmail.com", password='password')
db.session.add(user_2)

db.session.commit()

post_1 = Post(title='Blog 1', content='First post content', user_id=1)
post_2 = Post(title='Blog 2', content='Second post content', user_id=1)
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()

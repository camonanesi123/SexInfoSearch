# db_mysql.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Xjj(db.Model):
    __tablename__ = 'detail_info'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    url = db.Column(db.String(300), nullable=False, server_default=None)
    isGet = db.Column(db.Integer, nullable=False, server_default='0')
    title=db.Column(db.String(180), nullable=False, server_default=None)
    style=db.Column(db.String(30), nullable=False, server_default=None)
    district=db.Column(db.String(60), nullable=False, server_default=None)
    detailAddr=db.Column(db.String(360), nullable=False, server_default=None)
    source=db.Column(db.String(180), nullable=False, server_default=None)
    amount=db.Column(db.String(48), nullable=False, server_default=None)
    age=db.Column(db.String(48), nullable=False, server_default=None)
    leveldesc=db.Column(db.String(150), nullable=False, server_default=None)
    appear=db.Column(db.String(240), nullable=False, server_default=None)
    service=db.Column(db.String(240), nullable=False, server_default=None)
    price=db.Column(db.String(360), nullable=False, server_default=None)
    timeopen=db.Column(db.String(150), nullable=False, server_default=None)
    environ=db.Column(db.String(180), nullable=False, server_default=None)
    safe=db.Column(db.String(90), nullable=False, server_default=None)
    judge=db.Column(db.String(180), nullable=False, server_default=None)
    contact=db.Column(db.BLOB, nullable=False, server_default=None)
    detail=db.Column(db.TEXT)

    def __init__(self,id):
        self.id = id

    def __repr__(self):
        return '<User %r,Role id %r>' % (self.username, self.role_id)


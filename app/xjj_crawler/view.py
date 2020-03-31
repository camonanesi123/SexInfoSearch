from flask import request, render_template, Blueprint, flash, redirect, url_for
from app.controller import XjjDao


# 定义蓝图
notesbp = Blueprint('notesbp', __name__, template_folder='templates')

@notesbp.route('/')
def index():

    noteservice = XjjDao()

    # return book list to front end
    notes = noteservice.list_all()
    return render_template('index.html', notes=notes)

from flask import render_template, flash, redirect
from app import app

from app.form import LoginForm
from app import finalCode
import pickle

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
    form=LoginForm()
    content = {'title':'Restauranto'}
    if form.validate_on_submit():
        reviews,len1,len2 = finalCode.main(form.searchTerm.data)
        flash('Search results for: {}'.format(form.searchTerm.data))
        return render_template('index.html',content=content,reviews=reviews,len1=len1,len2=len2,form=form)
    return render_template('index.html', content=content,form=form)

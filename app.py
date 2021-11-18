from typing import Counter
from flask import Flask, render_template, session, redirect, url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from numpy.lib.polynomial import poly
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired
import galois
import numpy as np
import numba
import pickle
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

#################################Check#########################################
valid_character = ['0','1','2','3','4','5','6','7','8','9','^']
def check_str(GF):
	if GF[0] == '^' or GF[-1] == '^':
		return False
	for character in GF:
		if character not in valid_character:
			return False
	return True

def cal_order(GF):
	pos = GF.find("^");
	if pos == -1:
		#"^" not exists
		p = int(GF)
		if not galois.is_prime(p):
			return -1
		else:
			return p
	else:
		p = int(GF[:pos])
		if not galois.is_prime(p):
			return -1
		m = int(GF[pos+1:])
		if m == 0:
			return -2
	return p**m
##########################################################################


###########################Galois#########################################
def primitive_polys_str(order,degree,limit,method):
	counter = 0
	field = galois.GF(order)

	# Only search monic polynomials of degree m over GF(p)
	#min_ = order**degree
	file_start=open('./var/start.pkl','rb+')
	dic_start= pickle.load(file_start)
	file_start.close()
	min_=dic_start['min_']
	max_=dic_start['max_']
	#max_ = 2*order**degree

	polys_str = []

	if method == 'order' and limit == -1:
		for element in range(min_, max_):
			poly = galois.Poly.Integer(element, field=field)
			if galois.is_primitive(poly):
				polys_str.append(poly.string)
		return polys_str

	if method == 'reverse' and limit == -1:
		for element in range(max_-1, min_-1,-1):
			poly = galois.Poly.Integer(element, field=field)
			if galois.is_primitive(poly):
				polys_str.append(poly.string)
		return polys_str

	if method == 'random' and limit == -1:
		for element in range(min_, max_):
			poly = galois.Poly.Integer(element, field=field)
			if galois.is_primitive(poly):
				polys_str.append(poly.string)
		return polys_str
	
	if method == 'order' and limit != -1:
		for element in range(min_, max_):
			poly = galois.Poly.Integer(element, field=field)
			if galois.is_primitive(poly):
				polys_str.append(poly.string)
				counter += 1
				if counter == limit:
					dic_start['min_'] = element+1
					file_start=open('./var/start.pkl','wb+')
					pickle.dump(dic_start,file_start)
					file_start.close()
					break
		return polys_str

	if method == 'reverse' and limit != -1:
		for element in range(max_-1, min_-1,-1):
			poly = galois.Poly.Integer(element, field=field)
			if galois.is_primitive(poly):
				polys_str.append(poly.string)
				counter += 1
				if counter == limit:
					dic_start['max_'] = element
					file_start = open('./var/start.pkl','wb+')
					pickle.dump(dic_start,file_start)
					file_start.close()
					break
		return polys_str

	else:
		for element in range(max_-1, min_-1,-1):
			poly = galois.primitive_poly(order,degree,method='random')
			poly_str = poly.string
			if poly_str not in polys_str:
				polys_str.append(poly_str)
				counter += 1
				if counter == limit:
					break
		return polys_str

def num_term_primitive_polys_str(order,degree,num_term,limit,method):
	counter = 0

	#min_ = order**degree
	#max_ = 2*order**degree
	file_start=open('./var/start.pkl','rb+')
	dic_start= pickle.load(file_start)
	file_start.close()
	min_=dic_start['min_']
	max_=dic_start['max_']	
	field = galois.GF(order)
	polys_str = []
	
	if num_term <1 or num_term>degree+1:
		return polys_str

	if num_term == 1:
		poly = 	galois.Poly.Integer(min_,field=field)
		if galois.is_primitive(poly):
			polys_str.append(poly.string)
		return polys_str

	#for i in range(num_term-1):
	#	min_ += order**i
	#max_ -= order**(degree-num_term+1)
	#max_ += 1

	if method == 'order' and limit == -1:
		for element in range(min_, max_):
			poly = galois.Poly.Integer(element, field=field)
			poly_str = poly.string
			if poly_str.count('+') == num_term-1:
				if galois.is_primitive(poly):
					polys_str.append(poly_str)
		return polys_str
	
	if method == 'reverse' and limit == -1:
		for element in range(max_-1, min_-1,-1):
			poly = galois.Poly.Integer(element, field=field)
			poly_str = poly.string
			if poly_str.count('+') == num_term-1:
				if galois.is_primitive(poly):
					polys_str.append(poly_str)
		return polys_str

	if method == 'order' and limit != -1:
		for element in range(min_,max_):
			poly = galois.Poly.Integer(element,field=field)
			poly_str = poly.string
			if poly_str.count('+') == num_term-1:
				if galois.is_primitive(poly):
					polys_str.append(poly_str)
					counter += 1
					if counter == limit:
						dic_start['min_'] = element+1
						file_start=open('./var/start.pkl','wb+')
						pickle.dump(dic_start,file_start)
						file_start.close()
						break;
		return polys_str

	else:
		for element in range(max_-1,min_-1,-1):
			poly = galois.Poly.Integer(element,field=field)
			poly_str = poly.string
			if poly_str.count('+') == num_term-1:
				if galois.is_primitive(poly):
					polys_str.append(poly_str)
					counter += 1
					if counter == limit:
						dic_start['max_'] = element
						file_start = open('./var/start.pkl','wb+')
						pickle.dump(dic_start,file_start)
						file_start.close()
						break;
		return polys_str
#####################################################################

################################FlaskForm################################
class index_form(FlaskForm):
	GF = StringField('GF', validators=[DataRequired()])
	degree = IntegerField('Degree', validators=[DataRequired()])
	limit = IntegerField('Limit',validators=[DataRequired()])
	method = RadioField('Method',choices = ['order','reverse','random'])
	submit = SubmitField('Submit')

class find_one_form(FlaskForm):
	GF = StringField('GF',validators=[DataRequired()])
	degree = IntegerField('Degree',validators=[DataRequired()])
	method = RadioField('Method',choices = ['min','max','random'])
	submit = SubmitField('Submit')

class num_term_form(FlaskForm):
	GF = StringField('GF', validators=[DataRequired()])
	degree = IntegerField('Degree',validators=[DataRequired()])
	num_term = IntegerField('Number Of Term',validators=[DataRequired()])
	limit = IntegerField('Limit',validators=[DataRequired()])
	method = RadioField('Method',choices = ['order','reverse'])
	submit = SubmitField('Submit')

class conway_form(FlaskForm):
	characteristic = IntegerField('Characteristic',validators=[DataRequired()])
	degree = IntegerField('Degree',validators=[DataRequired()])
	Submit = SubmitField('Submit')

class judge_form(FlaskForm):
	GF = StringField('GF',validators=[DataRequired()])
	expression = StringField('Expression',validators=[DataRequired()])
	submit = SubmitField('Submit')
########################################################################


############################flask route##################################
@app.route('/', methods=['GET', 'POST'])
def index():
	form = index_form()
	GF = form.GF.data
	if form.validate_on_submit():
		if check_str(GF) == False:
			flash("'GF' is invalid")
			return render_template('index.html',form = form)
		order = cal_order(GF)
		if order == -1:
			flash("'characteristic' must be a prime")
			return render_template('index.html',form = form)
		if order == -2:
			flash("'dimension' can't be 0")
			return render_template('index.html',form = form)
		if form.degree.data < 0:
			flash("'degree' can't be a negtive number")
			return render_template('index.html',form = form)
		else:
			#初始化搜索起点
			min_ = order**(form.degree.data)
			max_ = 2*min_
			dic_start = {'min_':min_,'max_':max_}
			file_start=open('./var/start.pkl','wb+')
			pickle.dump(dic_start,file_start)
			file_start.close()
			
			session['primitive_polys_str'] = primitive_polys_str(order,form.degree.data,form.limit.data,form.method.data)
			dic_index = {'form_GF':form.GF.data,'form_degree':form.degree.data,'form_limit':form.limit.data,'form_method':form.method.data,'order':order}
			file_index = open('./var/index.pkl','wb+')
			pickle.dump(dic_index,file_index)
			file_index.close()
			return render_template('result_index.html',form=form,primitive_polys_str = session.get('primitive_polys_str'))	
	else:
		return render_template('index.html',form = form)

@app.route('/result_index',methods=['GET','POST'])
def result_index():
	form = index_form()
	file_index = open('./var/index.pkl','rb')
	dic_index = pickle.load(file_index)
	file_index.close()
	form.GF.data = dic_index['form_GF']
	form.degree.data = dic_index['form_degree']
	form.limit.data = dic_index['form_limit']
	form.method.data = dic_index['form_method']
	order = dic_index['order']
	session['primitive_polys_str'] = primitive_polys_str(order,form.degree.data,form.limit.data,form.method.data)
	return render_template('/result_index.html',form=form,primitive_polys_str=session.get('primitive_polys_str'))

@app.route('/find_one', methods=['GET', 'POST'])
def find_one():
	form = find_one_form()
	if form.validate_on_submit():
		GF = form.GF.data
		if check_str(GF) == False:
			flash("'GF' is invalid")
			render_template('find_one.html',form = form)
		order = cal_order(GF)
		if order == -1:
			flash("'characteristic' must be a prime")
			return render_template('find_one.html',form = form)
		if order == -2:
			flash("'dimension' can't be 0")
			return render_template('find_one.html',form = form)
		if form.degree.data < 0:
			flash("'degree' can't be a negtive number")
			return render_template('find_one.html',form = form)
		else:
			session['primitive_poly_str'] = [galois.primitive_poly(order,form.degree.data,form.method.data).string]
			dic_find_one = {'form_GF':form.GF.data,'form_degree':form.degree.data,'form_method':form.method.data,'order':order}
			file_find_one = open('./var/find_one.pkl','wb+')
			pickle.dump(dic_find_one,file_find_one)
			file_find_one.close()
			return render_template('result_find_one.html',form=form,primitive_polys_str = session.get('primitive_poly_str'))	
	else:
		return render_template('find_one.html',form=form)

@app.route('/result_find_one',methods=['GET','POST'])
def result_find_one():
	form = find_one_form()
	file_find_one = open('./var/find_one.pkl','rb')
	dic_find_one = pickle.load(file_find_one)
	file_find_one.close()
	form.GF.data = dic_find_one['form_GF']
	form.degree.data = dic_find_one['form_degree']
	form.method.data = dic_find_one['form_method']
	order = dic_find_one['order']
	session['primitive_poly_str'] = [galois.primitive_poly(order,form.degree.data,form.method.data).string]
	return render_template('result_find_one.html',form=form,primitive_polys_str = session.get('primitive_poly_str'))


@app.route('/num_term', methods=['GET', 'POST'])
def num_term():
	form = num_term_form()
	GF = form.GF.data
	if form.validate_on_submit():
		if check_str(GF) == False:
			flash("'GF' is invalid")
			return render_template('num_term.html',form = form)
		order = cal_order(GF)
		if order == -1:
			flash("'characteristic' must be a prime")
			return render_template('num_term.html',form = form)
		if order == -2:
			flash("'dimension' can't be 0")
			return render_template('num_term.html',form = form)
		if form.degree.data < 0:
			flash("'degree' can't be a negtive number")
			return render_template('num_term.html',form = form)
		if form.num_term.data <= 0:
			flash("'num_term' must be a positive number")
			return render_template('num_term.html',form = form)
		else:
			#初始化搜索起点
			min_ = order**(form.degree.data)
			max_ = 2*min_
			for i in range(form.num_term.data-1):
				min_ += order**i
			max_ -= order**(form.degree.data-form.num_term.data+1)
			max_ += 1
			dic_start = {'min_':min_,'max_':max_}
			file_start=open('./var/start.pkl','wb+')
			pickle.dump(dic_start,file_start)
			file_start.close()

			session['num_term_primitive_polys_str'] = num_term_primitive_polys_str(order,form.degree.data,form.num_term.data,form.limit.data,form.method.data)#Pistache
			dic_num_term = {'form_GF':form.GF.data,'form_degree':form.degree.data,'form_num_term':form.num_term.data,'form_limit':form.limit.data,'form_method':form.method.data,'order':order}
			file_num_term = open('./var/num_term.pkl','wb+')
			pickle.dump(dic_num_term,file_num_term)
			file_num_term.close()
			return render_template('result_num_term.html',form = form,num_term_primitive_polys_str = session.get('num_term_primitive_polys_str'))	
	else:
		return render_template('num_term.html',form = form)


@app.route('/result_num_term',methods=['GET','POST'])
def result_num_term():
	form = num_term_form()
	file_num_term = open('./var/num_term.pkl','rb')
	dic_num_term = pickle.load(file_num_term)
	file_num_term.close()
	
	form.GF.data = dic_num_term['form_GF']
	form.degree.data = dic_num_term['form_degree']
	form.num_term.data = dic_num_term['form_num_term']
	form.limit.data = dic_num_term['form_limit']
	form.method.data = dic_num_term['form_method']
	order = dic_num_term['order']
	session['num_term_primitive_polys_str'] = num_term_primitive_polys_str(order,form.degree.data,form.num_term.data,form.limit.data,form.method.data)
	return render_template('result_num_term.html',form=form,num_term_primitive_polys_str=session.get('num_term_primitive_polys_str'))

@app.route('/conway', methods=['GET', 'POST'])
def conway():
	form = conway_form()
	session['show'] = False
	if form.validate_on_submit():
		if not galois.is_prime(form.characteristic.data):
			flash("'characteristic' must be a prime")
			return render_template('conway.html',form = form,show = session.get('show'))
		if form.degree.data <=0:
			flash("'degree' must be a positive number")
			return render_template('conway.html',form = form,show = session.get('show'))
		session['show'] = True
		session['primitive_poly_str'] = (galois.conway_poly(form.characteristic.data,form.degree.data)).string
	return render_template('conway.html',form = form, primitive_poly_str = session.get('primitive_poly_str') ,show = session.get('show'))	


@app.route('/judge',methods=['GET','POST'])
def judge():
	form = judge_form()
	GF = form.GF.data
	session['show'] = False
	if form.validate_on_submit():
		if check_str(GF) == False:
			flash("'GF' is invalid")
			render_template('judge.html',form = form,show = session.get('show'))
		order = cal_order(GF)
		if order == -1:
			flash("'characteristic' must be a prime")
			return render_template('judge.html',form = form,show = session.get('show'))
		if order == -2:
			flash("'dimension' can't be 0")
			return render_template('judge.html',form = form,show = session.get('show'))
		session['show'] = True
		session['is_primitive'] = galois.is_primitive(galois.Poly.String(form.expression.data,field=galois.GF(order)))#Pistache
	return render_template('judge.html',form=form,is_primitive = session.get('is_primitive'),show = session.get('show'))

@app.route('/polynomial',methods=['GET','POST'])
def polynomial():
	return render_template('polynomial.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500
###########################################################################################

if __name__ == '__main__':
	app.run("0.0.0.0",5050,debug=True)

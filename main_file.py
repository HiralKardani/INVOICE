from flask import *
import os
import io
import sys
import psycopg2
import logging
from xhtml2pdf import pisa
from flask_mail import Mail, Message, email_dispatched
from datetime import date, timedelta, datetime


app = Flask(__name__, template_folder='D:/code/invoice/templates',static_url_path='/static')
app.secret_key = "Hiral"
# log = logging.getLogger('werkzeug')
# log.disabled = True

user=''
database_name='invoice'
now = datetime.now()
product_data=['','','']
customer_data=['','','','']


formatted_date = now.strftime("%B %d, %Y")
print(formatted_date)

due_date = now + timedelta(days=10)
formatted_due_date = due_date.strftime("%B %d, %Y")
print(formatted_due_date)


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'firstusertest42@gmail.com'
app.config['MAIL_PASSWORD'] = 'obfs gnrf gvvf tmfe'
app.config['MAIL_DEFAULT_SENDER'] = 'firstusertest42@gmail.com'

mail = Mail(app)

logging.basicConfig(level=logging.DEBUG)

def log_mail_message(message, app):
	app.logger.debug(f'Sending email to {message.recipients}')

email_dispatched.connect(log_mail_message, app)


########################## This Function will be called when to insert data into the Database ###########################
def WriteToDatabase(sql1,*args):
	counter = 0 # for trying atleast five times in case of failure.
	while True:
		try:
			conn = psycopg2.connect(database=database_name, user="postgres", password="postgres", host="localhost", port="5432")  # This will connect to the database.
			cur = conn.cursor()
			cur.execute(sql1,args) # Execute the querry.
			conn.commit()          # Insert data into database.
			conn.close()
			# print("Inserted in Database....")
			break
		except Exception as e:
			print("Error in Database writing-------::::",e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print("error in WriteToDatabase(): ",exc_type, fname, exc_tb.tb_lineno)
			try:
				conn.close()
				counter += 1
				if(counter > 5):
					result = []
					break
			except Exception as e:
				print("WriteToDatabase error",e)
				break
	counter = 0


########################## This Function will be called when to fetch the data from the Database #################################
def ReadDatabase(querry):
	
	counter = 0 # for trying atleast five times in case of failure.

	while True:
		try:
			conn = psycopg2.connect(database=database_name, user="postgres", password="postgres", host="localhost", port="5432")  # This will connect to the database.
			cur = conn.cursor()
			cur.execute(querry)  # Execute the querry.
			result = cur.fetchall() # read data from database.
			conn.close()
			break
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print("error in ReadDatabase() :",exc_type, fname, exc_tb.tb_lineno)
			try:
				conn.close()
				counter += 1 # increase the counter value
				if(counter > 5): # If counter value is greater then five then break the loop
					result = []
					break
			except:
				result = []
				break
	counter = 0
	return result


#######################
@app.route('/')
def login():
	return render_template('login.html')


@app.route('/logout')
def logout():
	return render_template('login.html')

@app.route('/home')
def home():
	global user
	query = "select * from invoice.invoice_details"
	result=ReadDatabase(query)
	# print("all details------------------",result)

	return render_template('index.html',name=user,result=result)


@app.route('/invoice_details/<int:invoice_id>')
def invoice_details(invoice_id):
	global invoice
	global prodect_list
	global formatted_date
	global formatted_due_date

	prodect_list=[]

	
	formatted_date = now.strftime("%B %d, %Y")
	print(formatted_date)

	due_date = now + timedelta(days=10)
	formatted_due_date = due_date.strftime("%B %d, %Y")
	print(formatted_due_date)
		
	# Find the invoice details by ID

	query = "select * from invoice.invoice_details"
	result=ReadDatabase(query)
	# print("all details------------------",result)

	invoice = next((item for item in result if item[0] == invoice_id), None)
	print("invoice==+++++++++++",invoice)


	# Split the strings into lists
	products = invoice[6].split(',')
	quantities = invoice[7].split(',')
	prices = invoice[8].split(',')

	# Combine the lists into the desired format
	prodect_list = [[products[i], quantities[i], prices[i]] for i in range(len(products))]

	# Print the result
	print("prodect_list---",prodect_list)


	if invoice:
		return render_template('invoice_test.html', invoice=invoice, prodect_list=prodect_list, formatted_date=formatted_date, formatted_due_date=formatted_due_date)
	else:
		return "Invoice not found", 404



@app.route('/invoice_remove/<int:invoice_id>')
def invoice_remove(invoice_id):


	print("invoice_id++++++++++++++++",invoice_id)
	delete_query = "DELETE FROM invoice.invoice_details WHERE id = {}".format(invoice_id)
	try:
		WriteToDatabase(delete_query)
		print("data deleted successfully....")
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})

	return redirect(url_for('home'))



@app.route('/product')
def product():
	global product_data
	return render_template('product.html', data=product_data)



@app.route('/add_product', methods=['POST'])  
def add_product():
	global product_data
	if request.method == 'POST':
		# product_name=request.form['product-name'] 
		product_name=request.form.get('product-name') 
		product_description=request.form['product-description']  
		product_price=request.form['product-price'] 
		print("-----",product_name,product_description,product_price) 
		print("-----",type(product_name),product_description,type(product_price))


		if product_name!='':
		
			qur='''INSERT INTO invoice.products(sync_time, product_name, "description", price)
				VALUES (now(), '{}', '{}', '{}');'''.format(product_name, product_description, str(product_price))
			print(qur)
			WriteToDatabase(qur)
			print("product data store successfully--------")


		product_data = [product_name, product_description, product_price]
		print(product_data)

	else:
		print("choose correct method..")

	return render_template('product.html', data=product_data)


@app.route('/product_remove/<product_name>')
def product_remove(product_name):
	global product_data
	print("invoice_id----+++++++",product_name)
	print("invoice_id----+++++++",product_data)
	product_data=['','','']


	delete_query = "DELETE FROM invoice.products WHERE product_name = '{}'".format(product_name)
	print(delete_query)
	try:
		WriteToDatabase(delete_query)
		print("data deleted successfully....")
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})

	# return render_template('product.html', data=product_data)
	return redirect(url_for('home'))





@app.route('/customer')
def customer():
	global customer_data
	return render_template('customer.html',data=customer_data)


@app.route('/add_customer', methods=['POST'])
def add_customer():
	global customer_data
		
	if request.method == 'POST':
		customer_name=request.form['customer-name']   
		customer_address=request.form['customer-address']  
		customer_phone=request.form['customer-phone'] 
		customer_email=request.form['customer-email'] 

		print("customer_data-----",customer_name,customer_address,customer_phone,customer_email)
		customer_data = [customer_name, customer_address, customer_phone, customer_email]
		print(customer_data)


		if customer_name!='':
		
			qur='''INSERT INTO invoice.customer(sync_time, customer_name, "address", phone, emai)
				VALUES (now(), '{}', '{}', '{}','{}');'''.format(customer_name, customer_address, customer_phone,customer_email)

			print(qur)
			WriteToDatabase(qur)
			print("customer data store successfully--------")

	return render_template('customer.html',data=customer_data)

	
@app.route('/customer_remove/<customer_name>')
def customer_remove(customer_name):
	global product_data
	print("customer_name----+++++++",customer_name)
	print("invoice_id----+++++++",product_data)
	product_data=['','','']


	delete_query = "DELETE FROM invoice.customer WHERE customer_name = '{}'".format(customer_name)
	print(delete_query)
	try:
		WriteToDatabase(delete_query)
		print("data deleted successfully....")
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)})

	return redirect(url_for('home'))


@app.route('/new_invoice')
def new_invoice():
	global invoice_result
	qry="select * from invoice.products"
	invoice_result=ReadDatabase(qry)
	# print("product result--------",result)

	qry="select * from invoice.customer"
	customer_result=ReadDatabase(qry)
	# print("customer_result--------",customer_result)

	return render_template('new_invoice.html', result=invoice_result,customer_result=customer_result)


@app.route('/get_invoice', methods=['POST'])
def get_invoice():
	print("*****************")
	invoice_result=request.form
	print("result--------",invoice_result)

	customer_name = request.form['customer-select']
	# print("Selected Customer:", customer_name)
	customer_address = request.form['customer-address']
	customer_phone = request.form['customer-phone']
	customer_email = request.form['customer-email']
	invoice_status = request.form['status']


	print("Customer Information:")
	print(f"Name: {customer_name}")
	print(f"Address: {customer_address}")
	print(f"Phone: {customer_phone}")
	print(f"Email: {customer_email}")
	print(f"invoice_status: {invoice_status}")


	items = request.form.getlist('item')
	item_quantities = request.form.getlist('item-quantity')
	item_prices = request.form.getlist('item-price')
	
	new_items=",".join(items)
	print("new_items:", new_items)
	new_item_quantities = ",".join(item_quantities)
	print("new_item_quantities:", new_item_quantities)
	new_item_prices = ",".join(item_prices)
	print("new_item_prices:", new_item_prices)


	products = []
	subtotal = 0
	for item, quantity, price in zip(items, item_quantities, item_prices):
		quantity = int(quantity)
		price = float(price)
		total_price = quantity * price
		subtotal += total_price
		product = {
			'item': item,
			'quantity': quantity,
			'price': price,
			'total_price': total_price
		}
		products.append(product)

		print("Product:", product)

	print("Productssss:", products)
	products.append(customer_name)
	products.append(customer_address)
	products.append(customer_phone)
	products.append(customer_email)
	print("Productsssssss:", products)


	# Calculate tax and total
	tax = subtotal * 0.10
	final_total = subtotal + tax
	print("subtotal--",subtotal)
	print("final_total--",final_total)


	query = '''INSERT INTO invoice.invoice_details(
	sync_time, customer_name, customer_address, customer_phone, customer_email, product_name, quantity, price, tax, total_price,sub_total,status)
	VALUES (now(), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}');'''.format(customer_name, customer_address, customer_phone, customer_email, new_items, new_item_quantities, new_item_prices, tax, final_total, subtotal,invoice_status)
	WriteToDatabase(query)
	print("Data of new invoice inserted successfully.......")

	return redirect(url_for('home'))



# @app.route('/download-pdf')
# def download_pdf():
# 	global invoice
# 	global prodect_list
# 	global formatted_date
# 	global formatted_due_date

# 	# Render the HTML template
# 	rendered_html = render_template('invoice_test.html', invoice=invoice, prodect_list=prodect_list,formatted_date=formatted_date, formatted_due_date=formatted_due_date)
	
# 	# Create a PDF
# 	pdf = convert_html_to_pdf(rendered_html)
	
# 	# Create a response object and set the appropriate headers
# 	response = make_response(pdf)
# 	response.headers['Content-Type'] = 'application/pdf'
# 	response.headers['Content-Disposition'] = 'attachment; filename=invoice_{}.pdf'.format(invoice[2])
	
# 	return response

def convert_html_to_pdf(source_html):
	# Convert HTML to PDF
	result = io.BytesIO()
	pdf = pisa.pisaDocument(io.BytesIO(source_html.encode("UTF-8")), result)
	
	if not pdf.err:
		return result.getvalue()
	return None
	

@app.route('/send-pdf-email', methods=['POST'])
def send_pdf_email_route():
	global invoice
	global prodect_list
	global formatted_date
	global formatted_due_date

	recipient = request.json.get('recipient')
	print("recipient-",recipient)
	rendered_html = render_template('invoice_test.html', invoice=invoice, prodect_list=prodect_list,formatted_date=formatted_date, formatted_due_date=formatted_due_date)


	pdf = convert_html_to_pdf(rendered_html)
	if pdf:
		send_pdf_email(recipient, pdf)
		return jsonify({'message': 'Email sent successfully'})
	return jsonify({'message': 'Failed to generate PDF'}), 500



def send_pdf_email(recipient, pdf):
	print("recipient-------",recipient)
	msg = Message("Your PDF", recipients=[recipient])
	msg.body = "Please find the attached PDF."
	msg.attach("output.pdf", "application/pdf", pdf)
	with app.app_context():
		mail.send(msg)



@app.route('/login_verify',methods = ['POST', 'GET'])
def login_verification():
	global user
	error=None
	if request.method == 'POST':
		user = request.form['username']
		print("user==",user)
		if user=="admin":
			flash('You are successfully logged in..')
			return redirect(url_for('home',name = user))
		else:
			error = 'Invalid username or password. Please try again!'
			return render_template('login.html',error=error)

	# else:
	#     user = request.args.get('username')
	#     print("user==",user)
	#     return redirect(url_for('index',name = user))
	else:
		flash('please login with admin')
		return redirect(url_for('index'))




if __name__ == '__main__':
	try:
		app.run(host = 'localhost', port = 5000, debug = True, use_reloader=False)
		raise KeyboardInterrupt

	except KeyboardInterrupt:
		print('Keyboard Interrupted')
		os._exit(130)

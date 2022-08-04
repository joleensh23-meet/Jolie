from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyCSZSFdFervvj_0T0J-y4unCkSWC34kZrk",

  "authDomain": "jolie-c43f5.firebaseapp.com",

  "projectId": "jolie-c43f5",

  "storageBucket": "jolie-c43f5.appspot.com",

  "messagingSenderId": "13231725292",

  "appId": "1:13231725292:web:05fd5f6dead9cd1faa23c9",

  "measurementId": "G-1FCVFLT685" , 
  "databaseURL":"https://jolie-c43f5-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':

        return render_template("home.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('products')) 

        except:
            error = "Authentication failed"
            return render_template("signin.html")

    else:
        return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        address = request.form['address']
        cardnum = request.form['cardnum']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user={"email": email , "password": password , "fullname": fullname , "address": address , "cardnum": cardnum}
            user = db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('products'))

        except:
            error = "Authentication failed"
            return render_template("signup.html", error=error)
    else:
        return render_template("signup.html")


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return render_template("products.html")
    else:
        cart = db.child("Cart").child(login_session['user']['localId']).get().val()
        if cart:
            if request.form['Add to Cart'] in cart:
                cart[request.form['Add to Cart']] += 1
            else:
                cart[request.form['Add to Cart']] = 1
                
            db.child("Cart").child(login_session['user']['localId']).update(cart)
        else:
            cart = {request.form['Add to Cart'] : 1}
            db.child("Cart").child(login_session['user']['localId']).set(cart)

        return render_template('products.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    products=db.child("Cart").child(login_session['user']['localId']).get().val()
    return render_template("cart.html" ,products=products)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':

        return render_template("checkout.html")
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
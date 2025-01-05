from flask import Flask, render_template,request,session,redirect,url_for

products = [
    {'id': 1, 'name': 'red skirt', 'image': 'static/images/ladies-skirts.jpg',"price":600,'style':"width: 100%; height: auto;",'text':'This stunning red skirt is perfect for any occasion! Crafted from high-quality fabric, it features a flattering fit and a vibrant color'},
    {'id': 2, 'name': 'black short top', 'image': "static/images/top.jpg","price":500,'style':"width: 70%; height: auto;",'text':'A versatile black short top that blends elegance with comfort. Perfect for casual outings or layered with a jacket for a chic evening look. A wardrobe essential for every fashionista!'},
    {'id': 3,'name':'blazer set','image':"static/images/blazer.jpg",'price':7000,'style':"width: 130%; height: auto;",'text':'This stunning blue blazer set redefines sophistication. Whether for office wear or formal events, it adds a sleek and polished touch to your style, keeping you effortlessly classy.'},
    {'id': 4,'name':'white pant','image':'static/images/pant1.jpg','price':1000,'style':"width: 90%; height: auto;",'text':'These white pants are the epitome of modern minimalism. With a tailored fit and clean design, they pair beautifully with tops or shirts for a fresh and stylish look.'},
    {'id': 5,'name':'Grey top','image':'static/images/top1.jpg','price':600,'style':"width: 100%; height: auto;",'text':"A classic grey top that's as versatile as it is comfortable. Ideal for casual days or styled with statement accessories for a trendy upgrade."},
    {'id': 6,'name':'Shirt','image':'static/images/shirt1.jpg','price':800,'style':"width: 80%; height: auto;",'text':'Embrace warm tones with this coffee-colored shirt. Perfect for both workwear and casual occasions, it adds a cozy yet polished feel to your wardrobe.'},
    {'id': 7,'name':'white tshirt','image':'static/images/tshirt.jpg','price':500,'style':"width: 100%; height: auto;","text":"A timeless white t-shirt that's a staple for every closet. Soft, comfortable, and easy to pair with anything, it’s perfect for casual outings or layering"},
    {'id': 8,'name':'jeans','image':'static/images/jeans.jpg','price':1200,'style':"width: 100%; height: auto;","text":"Durable and stylish, these jeans are designed for everyday wear. With a flattering fit and classic design, they effortlessly match any top for a complete look."}
]


app = Flask(__name__)
app.secret_key = "pooja"

@app.route("/")
def home():
    
    return render_template("index.html",products = products)

@app.route("/cart",methods = ["GET","POST"])
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html",cart_items = cart_items)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    size = request.form.get('size')  # Get the selected size from the form
    product_id = int(request.args.get('product_id'))
    product = next((prod for prod in products if prod["id"] == product_id), None)

    if request.method == "POST":

        # If the product exists and size is selected, create or update a cart item
        if product and size:
            # Initialize session cart if it doesn't exist
            if "cart" not in session:
                session["cart"] = []
            
            # Check if the item already exists in the cart
            cart = session["cart"]
            existing_item = next(
                (item for item in cart if item["id"] == product_id and item["size"] == size),
                None
            )

            if existing_item:
                # If the item exists, increase its quantity
                existing_item["quantity"] += 1
            else:
                # Otherwise, create a new cart item
                cart_item = {
                    "id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "size": size,
                    "quantity": 1  # Start with a quantity of 1
                }
                cart.append(cart_item)

            session.modified = True  # Mark the session as modified to ensure the change is saved
            action = request.form.get('action')
            if action == "buy":
                return redirect(url_for("buy")) 
            # Optionally, you can redirect to the cart page or show a success message
            return render_template('checkout.html',product = product)  # Redirect to a cart page after adding item

    return render_template("checkout.html", product=product)

    
@app.route('/remove_from_cart/<int:item_id>/<size>')
def remove_from_cart(item_id, size):
    # Retrieve cart from session
    cart = session.get('cart', [])
    
    # Remove the item with the given ID and size
    session['cart'] = [
        item for item in cart 
        if not (item['id'] == item_id and item['size'] == size)
    ]
    
    # Save changes to session and redirect to the cart page
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/buy', methods=["GET", "POST"])
def buy():
    # Retrieve cart from session
    cart = session.get('cart', [])
    
    if not cart:
        # Handle the case where the cart is empty
        return render_template('cart.html', message="Your cart is empty.")

    # Calculate the total amount
    total_amount = sum(item['price'] * item['quantity'] for item in cart)

    # Optionally, clear the cart after the purchase
    if request.method == "POST":

        return redirect(url_for("payment_option"))  # Redirect to a success page

    return render_template('cart.html', cart_items=cart, total=total_amount)


@app.route('/payment-options',methods = ["GET","POST"])
def payment_option():
    cart = session.get('cart', [])
    total_amount = sum(item['price'] * item['quantity'] for item in cart)
    if request.method == 'POST':
        # Get the selected payment method from the form
        selected_option = request.form.get('paymentMethod')
        
        if selected_option:
            session["cart"] = []
            session.modified = True
            home_link = f'<a href="{url_for("home")}">Back to Home</a>'

            # Save or process the selected option as needed
            return f"You selected {selected_option} as your payment method.{home_link}"
        else:
            return "No payment method selected. Please try again."

    return render_template('payment_options.html',total = total_amount)

if __name__ == '__main__':
    app.run(debug=True)

  

    

if __name__ == "__main__":
    app.run(debug=True)

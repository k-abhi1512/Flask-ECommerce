import os
from flask import render_template, redirect, url_for, flash, request, session
from .forms import ProductForm
from .models import Product
from . import products_bp
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


# Define the upload folder and allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'app/static/uploads'

# Route to add a new product
@products_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        # Handle image upload
        import pdb
        pdb.set_trace()
        image_file = request.files.get('image')  # Use request.files for file upload
        
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
            
            # Save product to the database
            new_product = Product(
                name=form.name.data,
                price=float(form.price.data), 
                description=form.description.data,
                quantity = float(form.quantity.data),
                image=filename  # Store only the filename, not full path
            )
            new_product.save_to_db()
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('products.list_products'))
        
        flash('Invalid image file or no file uploaded.', 'danger')
    else:
        print(form.errors)  # Debug validation errors
    
    return render_template('products/add_product.html', form=form)


# Route to list all products
@products_bp.route('/list_products')
def list_products():
    if '_user_id' not in session:
        flash('Please log in to access the Products.', 'warning')
        return redirect(url_for('auth.login'))
    products = Product.get_all()
    return render_template('products/list_products.html', products=products)

# Route to view product details
@products_bp.route('/product_detail/<product_id>')
def product_detail(product_id):
    if '_user_id' not in session:
        flash('Please log in to access the Products.', 'warning')
        return redirect(url_for('auth.login'))
    product = Product.get_by_id(product_id)
    if product:
        return render_template('products/product_detail.html', product=product)
    else:
        flash('Product not found', 'danger')
        return redirect(url_for('products.list_products'))

# Route to edit a product
@products_bp.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if '_user_id' not in session:
        flash('Please log in to access the Products.', 'warning')
        return redirect(url_for('auth.login'))
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('products.list_products'))
    print(product)
    form = ProductForm(
        name=product['name'],
        description=product['description'],
        price=product['price'],
        quantity=product['quantity'],
        image=product['image_path']
    )
    
    if form.validate_on_submit():
        import pdb
        pdb.set_trace()
        updated_data = {
            'name': form.name.data,
            'description': form.description.data,
            'price': float(form.price.data), 
            'quantity': float(form.quantity.data),
            'image_path': product['image_path']
        }
        Product.update_product(product_id, updated_data)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.product_detail', product_id=product_id))
    
    return render_template('products/edit_product.html', form=form, product=product)

# Route to delete a product
@products_bp.route('/delete_product/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if '_user_id' not in session:
        flash('Please log in to access the Products.', 'warning')
        return redirect(url_for('auth.login'))
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
    else:
        Product.delete_product(product_id)
        flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.list_products'))

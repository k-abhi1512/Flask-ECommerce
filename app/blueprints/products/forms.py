from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, FloatField
from wtforms.validators import DataRequired, NumberRange, DataRequired, Length
from flask_wtf.file import FileRequired, FileAllowed

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()]) 
    quantity = FloatField('Quantity', validators=[DataRequired()])
    # Image upload field
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')  # Allow only images
    ])
    submit = SubmitField('Add Product')

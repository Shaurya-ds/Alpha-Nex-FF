from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class SignupForm(FlaskForm):
    """User registration form with validation"""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    """User authentication form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class UploadForm(FlaskForm):
    """File upload form"""
    file = FileField('Select File', validators=[
        FileRequired(),
        FileAllowed(['mp3', 'wav', 'mp4', 'avi', 'pdf', 'doc', 'docx', 'txt', 'py', 'js', 'html', 'css', 'jpg', 'png', 'gif', 'zip'], 
                   'File type not allowed!')
    ])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    category = SelectField('Category', choices=[
        ('audio', 'Audio'),
        ('document', 'Document'), 
        ('code', 'Code'),
        ('text', 'Text'),
        ('image', 'Image'),
        ('archive', 'Archive')
    ], validators=[DataRequired()])
    ai_consent = BooleanField('I consent to AI analysis of this content', validators=[DataRequired()])


class RatingForm(FlaskForm):
    """Website rating form"""
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('overall', 'Overall Experience'),
        ('upload', 'Upload System'),
        ('review', 'Review System'),
        ('ui', 'User Interface')
    ], validators=[DataRequired()])
    description = TextAreaField('Feedback', validators=[Length(max=1000)])
    contact_email = StringField('Email (optional)', validators=[Email()])

class UploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1000)])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('audio', 'Audio'), 
        ('document', 'Document/PDF'),
        ('code', 'Code'),
        ('text', 'Text'),
        ('image', 'Image'),
        ('archive', 'Archive')
    ])
    ai_consent = BooleanField(
        'I agree that this content belongs to me, does not violate any rules, and can be used by AI companies for training',
        validators=[DataRequired()]
    )

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', validators=[DataRequired()], choices=[
        ('good', 'Good - High quality content'),
        ('bad', 'Bad - Poor quality or inappropriate')
    ])
    description = TextAreaField('Review Description', 
                              validators=[Length(min=10, max=500)],
                              render_kw={"placeholder": "Explain your rating in detail (required for bad ratings)..."})

class WithdrawalForm(FlaskForm):
    amount_xp = IntegerField('XP Amount', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', validators=[DataRequired()], choices=[
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency')
    ])
    payment_details = TextAreaField('Payment Details', validators=[DataRequired()])

class RatingForm(FlaskForm):
    # Disable CSRF for better compatibility - backend/frontend communication fixed
    
    rating = IntegerField('Overall Rating', validators=[DataRequired()])
    category = SelectField('Feedback Category', validators=[DataRequired()], choices=[
        ('general', 'General Feedback'),
        ('bug_report', 'Bug Report'),
        ('feature_request', 'Feature Request'),
        ('ui_ux', 'User Interface/Experience'),
        ('performance', 'Performance Issues'),
        ('suggestion', 'Improvement Suggestion')
    ])
    description = TextAreaField('Detailed Feedback', 
                              validators=[DataRequired(), Length(min=10, max=2000)],
                              render_kw={"placeholder": "Please share your detailed feedback..."})
    contact_email = StringField('Your Email (Optional)', validators=[Email()])

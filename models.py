from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    xp_points = db.Column(db.Integer, default=0)
    uploader_strikes = db.Column(db.Integer, default=0)
    reviewer_strikes = db.Column(db.Integer, default=0)
    is_banned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # KYC fields
    kyc_verified = db.Column(db.Boolean, default=False)
    document_path = db.Column(db.String(255))
    selfie_path = db.Column(db.String(255))
    
    # Daily upload tracking
    daily_upload_bytes = db.Column(db.Integer, default=0)
    daily_upload_count = db.Column(db.Integer, default=0)
    daily_upload_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Daily review tracking
    daily_review_count = db.Column(db.Integer, default=0)
    daily_review_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    uploads = db.relationship('Upload', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    strikes = db.relationship('Strike', backref='user', lazy=True)

    
    def reset_daily_counters_if_needed(self):
        """Reset daily counters if it's a new day"""
        try:
            current_date = datetime.utcnow().date()
            
            # Reset upload counters if new day
            if self.daily_upload_reset and current_date > self.daily_upload_reset.date():
                self.daily_upload_bytes = 0
                self.daily_upload_count = 0
                self.daily_upload_reset = datetime.utcnow()
            elif not self.daily_upload_reset:
                self.daily_upload_reset = datetime.utcnow()
            
            # Reset review counters if new day
            if self.daily_review_reset and current_date > self.daily_review_reset.date():
                self.daily_review_count = 0
                self.daily_review_reset = datetime.utcnow()
            elif not self.daily_review_reset:
                self.daily_review_reset = datetime.utcnow()
                
            db.session.commit()
        except Exception as e:
            pass  # Fail silently
    
    def get_daily_upload_remaining(self):
        """Calculate remaining daily upload capacity in bytes"""
        try:
            self.reset_daily_counters_if_needed()
            max_daily = 500 * 1024 * 1024  # 500MB in bytes
            current_usage = self.daily_upload_bytes or 0
            return max_daily - current_usage
        except Exception as e:
            return 500 * 1024 * 1024
    
    def can_upload_today(self):
        """Check if user can upload more files today (max 3 per day)"""
        try:
            self.reset_daily_counters_if_needed()
            return (self.daily_upload_count or 0) < 3
        except Exception as e:
            return True
    
    def can_review_today(self):
        """Check if user can review more content today (max 5 per day)"""
        try:
            self.reset_daily_counters_if_needed()
            return (self.daily_review_count or 0) < 5
        except Exception as e:
            return True
    
    def get_remaining_uploads_today(self):
        """Get remaining upload count for today"""
        try:
            self.reset_daily_counters_if_needed()
            return 3 - (self.daily_upload_count or 0)
        except Exception as e:
            return 3
    
    def get_remaining_reviews_today(self):
        """Get remaining review count for today"""
        try:
            self.reset_daily_counters_if_needed()
            return 5 - (self.daily_review_count or 0)
        except Exception as e:
            return 5
    
    def can_upload(self, file_size):
        """Check if user can upload a file of given size"""
        return (self.get_daily_upload_remaining() >= file_size and 
                self.can_upload_today() and 
                not self.is_banned and 
                file_size <= 100 * 1024 * 1024)  # 100MB limit per file
    
    def add_strike(self, strike_type, reason):
        strike = Strike()
        strike.user_id = self.id
        strike.strike_type = strike_type
        strike.reason = reason
        db.session.add(strike)
        
        if strike_type == 'uploader':
            self.uploader_strikes += 1
        elif strike_type == 'reviewer':
            self.reviewer_strikes += 1
            
        # Ban user if they reach 3 strikes in either category
        if self.uploader_strikes >= 3 or self.reviewer_strikes >= 3:
            self.is_banned = True
            
        db.session.commit()

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    ai_consent = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    deletion_deadline = db.Column(db.DateTime)
    
    # AI analysis results
    duplicate_score = db.Column(db.Float, default=0.0)
    spam_score = db.Column(db.Float, default=0.0)
    
    # Review tracking
    reviews = db.relationship('Review', backref='upload', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Upload, self).__init__(**kwargs)
        # Set deletion deadline to 48 hours from upload
        self.deletion_deadline = datetime.utcnow() + timedelta(hours=48)
    
    def get_average_rating(self):
        try:
            # Query reviews directly to avoid relationship property issues
            from app import db
            reviews_query = db.session.query(Review).filter_by(upload_id=self.id).all()
            if not reviews_query:
                return None
            good_reviews = sum(1 for r in reviews_query if r.rating == 'good')
            return good_reviews / len(reviews_query)
        except Exception as e:
            return None
    
    def can_delete_free(self):
        return datetime.utcnow() < self.deletion_deadline
    
    def get_deletion_penalty(self):
        if self.can_delete_free():
            return 0
        # Penalty increases based on how long after deadline
        hours_late = (datetime.utcnow() - self.deletion_deadline).total_seconds() / 3600
        return min(int(hours_late * 5), 100)  # Max 100 XP penalty

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.String(10), nullable=False)  # 'good' or 'bad'
    description = db.Column(db.Text, nullable=False)
    xp_earned = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quality tracking for reviewer strikes
    is_flagged = db.Column(db.Boolean, default=False)
    quality_score = db.Column(db.Float, default=1.0)

class Strike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    strike_type = db.Column(db.String(20), nullable=False)  # 'uploader' or 'reviewer'
    reason = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WithdrawalRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_xp = db.Column(db.Integer, nullable=False)
    amount_usd = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    payment_method = db.Column(db.String(100))
    payment_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    admin_notes = db.Column(db.Text)

class AdminAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)  # ID of affected user/upload/etc
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='ratings')

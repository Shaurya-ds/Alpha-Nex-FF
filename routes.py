"""
Simplified Alpha Nex Routes - Direct Access Without Demo User System
"""
import os
import uuid
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Upload, Review, Strike, WithdrawalRequest, AdminAction, Rating
from forms import UploadForm, ReviewForm, RatingForm
# from openai_service import analyze_content_quality  # Not needed for simplified version

def get_or_create_user_for_session():
    """Get or create a unique user for this session"""
    # Get user name from session
    user_name = session.get('user_name', 'Anonymous')
    
    # Create a unique username based on session name and timestamp
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())[:8]
        session['session_id'] = session_id
    
    username = f"user_{session_id}"
    
    # Try to find existing user for this session
    user = User.query.filter_by(username=username).first()
    
    if not user:
        # Create new user for this session
        user = User()
        user.username = username
        user.name = user_name
        user.email = f"{username}@alphanex.com"
        user.password_hash = generate_password_hash('alphanex123')
        user.xp_points = 500
        user.daily_upload_count = 0
        user.daily_upload_bytes = 0
        user.daily_review_count = 0
        user.daily_upload_reset = datetime.utcnow()
        user.daily_review_reset = datetime.utcnow()
        user.uploader_strikes = 0
        user.reviewer_strikes = 0
        user.is_banned = False
        
        db.session.add(user)
        db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
    else:
        # Update name if it changed
        if user.name != user_name:
            user.name = user_name
            db.session.add(user)
            db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
    
    return user

def create_demo_content_for_reviews():
    """Create demo content from a test user for reviews"""
    # Create a demo content user if doesn't exist
    demo_user = User.query.filter_by(username='demo_content_creator').first()
    if not demo_user:
        demo_user = User()
        demo_user.username = 'demo_content_creator'
        demo_user.name = 'Demo Content Creator'
        demo_user.email = 'demo@alphanex.com'
        demo_user.password_hash = generate_password_hash('demo123')
        demo_user.xp_points = 300
        db.session.add(demo_user)
        db.session.flush()
        
        # Create demo files
        demo_files = [
            {
                'filename': 'demo_audio.mp3',
                'original_filename': 'DEMO - Tech Podcast Episode',
                'file_size': 8388608,
                'description': 'DEMO FILE - Technology podcast about AI trends',
                'category': 'audio'
            },
            {
                'filename': 'demo_document.pdf',
                'original_filename': 'DEMO - Research Paper',
                'file_size': 2097152,
                'description': 'DEMO FILE - Academic research on machine learning',
                'category': 'document'
            },
            {
                'filename': 'demo_code.py',
                'original_filename': 'DEMO - Python Script',
                'file_size': 524288,
                'description': 'DEMO FILE - Data analysis script using pandas',
                'category': 'code'
            }
        ]
        
        for demo_file in demo_files:
            upload = Upload()
            upload.user_id = demo_user.id
            upload.filename = demo_file['filename']
            upload.original_filename = demo_file['original_filename']
            upload.file_path = f"uploads/{demo_file['filename']}"
            upload.file_size = demo_file['file_size']
            upload.description = demo_file['description']
            upload.category = demo_file['category']
            upload.status = 'pending'
            upload.ai_consent = True
            db.session.add(upload)
        
        db.session.commit()

def create_test_content_old():
    """Create sample content for review system"""
    test_files = [
        {
            'filename': 'sample_audio_podcast.mp3',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Tech Podcast Episode',
            'file_size': 8388608,  # 8MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Technology podcast discussion about AI trends and future innovations',
            'category': 'audio'
        },
        {
            'filename': 'sample_music.mp3',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Background Music Track',
            'file_size': 5242880,  # 5MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Instrumental background music for content creation',
            'category': 'audio'
        },
        {
            'filename': 'research_paper.pdf',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - AI Research Paper',
            'file_size': 2097152,  # 2MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Academic research paper on machine learning applications in healthcare',
            'category': 'document'
        },
        {
            'filename': 'tutorial_guide.pdf',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Programming Tutorial',
            'file_size': 3145728,  # 3MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Comprehensive programming tutorial for Python beginners',
            'category': 'document'
        },
        {
            'filename': 'data_analysis.py',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Python Data Analysis Script',
            'file_size': 524288,  # 512KB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Python script for data analysis and visualization using pandas',
            'category': 'code'
        },
        {
            'filename': 'web_scraper.js',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - JavaScript Web Scraper',
            'file_size': 262144,  # 256KB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - JavaScript web scraping tool for data collection',
            'category': 'code'
        },
        {
            'filename': 'project_notes.txt',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Project Documentation',
            'file_size': 131072,  # 128KB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Detailed project notes and development documentation',
            'category': 'text'
        },
        {
            'filename': 'meeting_minutes.txt',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Team Meeting Notes',
            'file_size': 65536,  # 64KB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Minutes from team meetings and project discussions',
            'category': 'text'
        },
        {
            'filename': 'logo_design.png',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Company Logo Design',
            'file_size': 1048576,  # 1MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Professional logo design for branding purposes',
            'category': 'image'
        },
        {
            'filename': 'infographic.jpg',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Data Infographic',
            'file_size': 2097152,  # 2MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Visual data representation and statistics infographic',
            'category': 'image'
        },
        {
            'filename': 'website_mockup.png',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Website Mockup',
            'file_size': 1572864,  # 1.5MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - UI/UX design mockup for web application',
            'category': 'image'
        },
        {
            'filename': 'source_code.zip',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Source Code Archive',
            'file_size': 4194304,  # 4MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Complete source code archive for web application project',
            'category': 'archive'
        },
        {
            'filename': 'assets_pack.zip',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Design Assets Pack',
            'file_size': 6291456,  # 6MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Collection of design assets including icons, fonts, and graphics',
            'category': 'archive'
        },
        {
            'filename': 'backup_files.tar.gz',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Project Backup',
            'file_size': 5242880,  # 5MB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Compressed backup of project files and database',
            'category': 'archive'
        },
        {
            'filename': 'documentation.md',
            'original_filename': '**DEMO FILE FOR TESTING PURPOSES ONLY** - API Documentation',
            'file_size': 327680,  # 320KB
            'description': '**DEMO FILE FOR TESTING PURPOSES ONLY** - Comprehensive API documentation with examples and usage guidelines',
            'category': 'text'
        }
    ]
    
    # Create a separate test user for these uploads
    test_user = User.query.get(2)
    if not test_user:
        test_user = User()
        test_user.id = 2
        test_user.username = 'test_content_user'
        test_user.name = 'Test Content User'
        test_user.email = 'testcontent@alphanex.com'
        test_user.password_hash = generate_password_hash('test123')
        test_user.xp_points = 300
        db.session.add(test_user)
        db.session.flush()
        
        for test_file in test_files:
            upload = Upload()
            upload.user_id = test_user.id
            upload.filename = test_file['filename']
            upload.original_filename = test_file['original_filename']
            upload.file_path = f"uploads/demo_{test_file['filename']}"
            upload.file_size = test_file['file_size']
            upload.description = test_file['description']
            upload.category = test_file['category']
            upload.status = 'pending'
            upload.ai_consent = True
            db.session.add(upload)

@app.route('/')
def index():
    """Landing page redirects to name entry"""
    return redirect(url_for('name_entry'))

@app.route('/name_entry', methods=['GET', 'POST'])
def name_entry():
    """Name entry page before dashboard"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name and len(name) >= 2 and len(name) <= 50 and name.replace(' ', '').isalpha():
            session['user_name'] = name
            
            # Create demo content for reviews if needed
            create_demo_content_for_reviews()
            
            return redirect(url_for('dashboard'))
        else:
            flash('Please enter a valid name (2-50 characters, letters and spaces only)', 'error')
    
    return render_template('name_entry.html')

@app.route('/health')
def health():
    """Health check endpoint for uptime monitoring"""
    try:
        # Test database connection
        from app import db
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return "OK", 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return "Database Error", 503

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    # Check if user has entered name
    if 'user_name' not in session:
        return redirect(url_for('name_entry'))
    
    try:
        user = get_or_create_user_for_session()
        user_name = session['user_name']
        
        # Get user stats
        upload_count = Upload.query.filter_by(user_id=user.id).count()
        review_count = Review.query.filter_by(reviewer_id=user.id).count()
        
        # Get recent uploads
        recent_uploads = Upload.query.filter_by(user_id=user.id)\
                                    .order_by(Upload.uploaded_at.desc()).limit(5).all()
        
        # Calculate daily remaining
        daily_remaining = user.get_daily_upload_remaining()
        daily_remaining_mb = daily_remaining / (1024 * 1024)
        
        # Generate motivational messages based on user progress
        import random
        
        # Welcome messages with motivation
        welcome_messages = [
            f"🌟 Welcome back! Ready to earn more XP?",
            f"🚀 Hey there! Time to create amazing content!",
            f"⭐ Great to see you! Let's make today productive!",
            f"💪 You're doing fantastic! Keep it up!",
            f"🔥 Welcome! Your contributions make a difference!",
            f"✨ Hello! Ready to level up today?",
            f"🎯 You're on the right path to success!"
        ]
        
        # Milestone celebration messages
        milestone_messages = []
        if user.xp_points >= 100:
            milestone_messages.append("🎉 Amazing! You've reached 100+ XP points!")
        if user.xp_points >= 500:
            milestone_messages.append("🏆 Incredible! 500+ XP points achieved!")
        if upload_count >= 5:
            milestone_messages.append("📁 Fantastic! You've uploaded 5+ files!")
        if review_count >= 10:
            milestone_messages.append("👀 Outstanding! 10+ reviews completed!")
        
        # Progress motivation without limits
        daily_motivation = [
            f"💡 Keep uploading amazing content!",
            f"🔍 More reviews help the community grow!"
        ]
        
        return render_template('dashboard.html', 
                             upload_count=upload_count,
                             review_count=review_count,
                             recent_uploads=recent_uploads,
                             daily_remaining_mb=daily_remaining_mb,
                             demo_user=user,
                             current_user=user,
                             user_name=user_name,
                             xp_threshold_reached=False,
                             welcome_message=random.choice(welcome_messages),
                             milestone_message=" ".join(milestone_messages),
                             daily_limit_message=" ".join(daily_motivation))
                             
    except Exception as e:
        app.logger.error(f"Dashboard error: {e}")
        return render_template('error.html', error=f"Dashboard error: {str(e)}")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """File upload endpoint"""
    try:
        user = get_or_create_user_for_session()
        form = UploadForm()
        
        if form.validate_on_submit():
            file = form.file.data
            if file and file.filename:

                
                # Process file upload
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                upload_folder = 'uploads'
                file_path = os.path.join(upload_folder, unique_filename)
                
                # Ensure upload directory exists
                os.makedirs(upload_folder, exist_ok=True)
                
                # Save file
                file.save(file_path)
                file_size = os.path.getsize(file_path)
                
                # Check file size limit (100MB)
                if file_size > 100 * 1024 * 1024:
                    os.remove(file_path)
                    flash('File too large! Maximum size is 100MB.', 'error')
                    return redirect(url_for('upload_file'))
                
                # Create upload record
                upload = Upload()
                upload.user_id = user.id
                upload.filename = unique_filename
                upload.original_filename = filename
                upload.file_path = file_path
                upload.file_size = file_size
                upload.description = form.description.data
                upload.category = form.category.data
                upload.status = 'pending'
                upload.ai_consent = form.ai_consent.data
                
                # Update user stats - give XP for upload
                user.xp_points += 20
                
                db.session.add(upload)
                db.session.add(user)  # Make sure user changes are saved
                db.session.commit()
                
                motivational_messages = [
                    "🎉 Awesome upload! You're contributing amazing content!",
                    "⭐ Fantastic! Your upload earned you 20 XP points!",
                    "🚀 Great job! Keep sharing quality content!",
                    "💪 Excellent upload! You're making the platform better!",
                    "🌟 Outstanding work! 20 XP points added to your account!",
                    "🔥 Amazing content! You're a content creation superstar!",
                    "✨ Perfect upload! Your contribution is valuable!"
                ]
                import random
                flash(random.choice(motivational_messages), 'success')
                return redirect(url_for('dashboard'))
        
        # Calculate remaining daily upload capacity
        daily_remaining = user.get_daily_upload_remaining()
        daily_remaining_mb = daily_remaining / (1024 * 1024)
        
        return render_template('uploader/upload.html', 
                             form=form, 
                             daily_remaining_mb=daily_remaining_mb, 
                             demo_user=user,
                             current_user=user)
                             
    except Exception as e:
        app.logger.error(f"Upload error: {e}")
        return render_template('error.html', error=f"Upload error: {str(e)}")

@app.route('/review')
def review_content():
    """Content review page"""
    try:
        user = get_or_create_user_for_session()
        
        # Get uploads that need review (not from current user and not already reviewed)
        reviewed_upload_ids = [r.upload_id for r in Review.query.filter_by(reviewer_id=user.id).all()]
        
        uploads = Upload.query.filter(
            Upload.user_id != user.id,  # Cannot review own uploads
            ~Upload.id.in_(reviewed_upload_ids)  # Haven't reviewed yet
        ).order_by(Upload.uploaded_at.desc()).all()
        
        # Filter out uploads that already have 5 reviews
        available_uploads = []
        for upload in uploads:
            review_count = Review.query.filter_by(upload_id=upload.id).count()
            if review_count < 5:  # Max 5 reviews per upload
                available_uploads.append(upload)
        
        return render_template('reviewer/review.html', 
                             uploads=available_uploads, 
                             demo_user=user,
                             current_user=user)
                             
    except Exception as e:
        app.logger.error(f"Review error: {e}")
        return render_template('error.html', error=f"Review error: {str(e)}")

@app.route('/review/<int:upload_id>', methods=['GET', 'POST'])
def review_upload(upload_id):
    """Review a specific upload"""
    try:
        user = get_or_create_user_for_session()
        upload = Upload.query.get_or_404(upload_id)
        form = ReviewForm()
        
        if form.validate_on_submit():
            # Check if user already reviewed this upload
            existing_review = Review.query.filter_by(upload_id=upload_id, reviewer_id=user.id).first()
            if existing_review:
                flash('You have already reviewed this upload.', 'warning')
                return redirect(url_for('review_content'))
            
            # Create review
            review = Review()
            review.upload_id = upload_id
            review.reviewer_id = user.id
            review.rating = form.rating.data
            review.description = form.description.data
            review.xp_earned = 15  # Review XP
            
            # Update user stats - give XP for review
            user.xp_points += 15
            
            db.session.add(review)
            db.session.add(user)  # Make sure user changes are saved
            db.session.commit()
            db.session.commit()
            
            motivational_messages = [
                "🎉 Amazing review! You're helping make the platform better!",
                "⭐ Great job! Your insights are valuable to our community!",
                "🚀 Fantastic review! You're on fire today!",
                "💪 Excellent work! Keep up the great reviewing!",
                "🌟 Outstanding review! You earned 15 XP points!",
                "🔥 Brilliant analysis! You're a reviewing superstar!",
                "✨ Perfect review! Your feedback makes a difference!"
            ]
            import random
            flash(random.choice(motivational_messages), 'success')
            return redirect(url_for('review_content'))
        
        # Get existing reviews for this upload
        existing_reviews = Review.query.filter_by(upload_id=upload_id).all()
        
        return render_template('reviewer/review_upload.html', 
                             upload=upload, 
                             form=form,
                             existing_reviews=existing_reviews, 
                             review_count=len(existing_reviews), 
                             demo_user=user,
                             current_user=user)
                             
    except Exception as e:
        app.logger.error(f"Review upload error: {e}")
        return render_template('error.html', error=f"Review upload error: {str(e)}")

@app.route('/profile')
def profile():
    """User profile page"""
    try:
        user = get_or_create_user_for_session()
        
        # Get user's strikes and violation history
        strikes = Strike.query.filter_by(user_id=user.id)\
                             .order_by(Strike.created_at.desc()).all()
        
        return render_template('profile.html', 
                             current_user=user,
                             demo_user=user,
                             strikes=strikes)
                             
    except Exception as e:
        app.logger.error(f"Profile error: {e}")
        return render_template('error.html', error=f"Profile error: {str(e)}")


@app.route('/rating', methods=['GET', 'POST'])
def rate_website():
    """Website rating and feedback page"""
    try:
        user = get_or_create_user_for_session()
        form = RatingForm()
        
        if request.method == 'POST':
            # Debug form data
            app.logger.info(f"Form data received: {request.form}")
            app.logger.info(f"Form validation errors: {form.errors}")
            
            if form.validate_on_submit():
                # Create rating record
                rating = Rating()
                rating.user_id = user.id
                rating.rating = form.rating.data
                rating.category = form.category.data
                rating.description = form.description.data
                rating.contact_email = form.contact_email.data if form.contact_email.data else None
                
                db.session.add(rating)
                db.session.commit()
                
                flash('Thank you for your feedback! Your rating has been submitted.', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Show validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'{field}: {error}', 'error')
        
        return render_template('rating.html', 
                             form=form,
                             demo_user=user,
                             current_user=user)
                             
    except Exception as e:
        app.logger.error(f"Rating error: {e}")
        return render_template('error.html', error=f"Rating error: {str(e)}")

@app.route('/delete_upload/<int:upload_id>')
def delete_upload(upload_id):
    """Delete an upload"""
    try:
        user = get_or_create_user_for_session()
        upload = Upload.query.get_or_404(upload_id)
        
        # Check if user owns this upload
        if upload.user_id != user.id:
            flash('You can only delete your own uploads.', 'error')
            return redirect(url_for('dashboard'))
        
        # Delete file from filesystem
        if os.path.exists(upload.file_path):
            os.remove(upload.file_path)
        
        # Delete reviews for this upload
        Review.query.filter_by(upload_id=upload_id).delete()
        
        # Delete upload record
        db.session.delete(upload)
        db.session.commit()
        
        flash('Upload deleted successfully.', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        app.logger.error(f"Delete upload error: {e}")
        flash('Error deleting upload.', 'error')
        return redirect(url_for('dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500
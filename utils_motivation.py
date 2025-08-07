"""
Motivational messages and user engagement utilities for Alpha Nex
"""
import random

def get_upload_success_message(user_name, xp_earned, upload_count):
    """Get a motivational message for successful uploads"""
    messages = [
        # Data Hero Style
        f"🧠 Brilliant upload! You're helping build the smartest content library on the internet — and we notice your quality.",
        f"🧠 Another smart contribution! You're making the platform smarter with each upload — {xp_earned} XP earned!",
        f"🧠 Data hero in action! Your {upload_count} uploads are building something amazing. Keep the quality coming!",
        
        # Future Elite Style
        f"🚀 You're on the path to becoming one of our elite content creators. Keep it up — big rewards ahead!",
        f"🚀 Future elite alert! Uploads like this will put you in our top contributor hall of fame. +{xp_earned} XP!",
        f"🚀 You're building your legacy one upload at a time. Elite status is within reach!",
        
        # Founder Speaks Style
        f"🫱 As the founder, I personally thank you. Contributors like you will shape the future of Alpha Nex.",
        f"🫱 From the founding team: This is exactly the quality content we envisioned. Thank you for believing in our mission!",
        f"🫱 Founder's note: Your {upload_count} contributions prove you understand our vision. We're grateful!",
        
        # Competitive Style
        f"🏆 You're already ahead of 90% of users in quality. That's exactly what we want for our top team!",
        f"🏆 Competition alert! Uploads like this put you in the top tier. You're outperforming most users!",
        f"🏆 Your quality score is impressive. You're competing with the best — and winning!",
        
        # Impact Style
        f"🎯 You didn't just upload a file — you contributed data that might help train the next generation of AI!",
        f"🎯 Impact achieved! Your content will be reviewed by others, creating a ripple effect of quality.",
        f"🎯 This upload joins {upload_count-1} others in making Alpha Nex the premium content platform!"
    ]
    
    return random.choice(messages)

def get_review_success_message(user_name, xp_earned, review_count):
    """Get a motivational message for successful reviews"""
    messages = [
        # Data Hero Style
        f"🧠 Another smart review! You're helping make the internet smarter — and we notice your insight.",
        f"🧠 Brilliant analysis! Your {review_count} reviews are setting the quality standard. +{xp_earned} XP!",
        f"🧠 Data hero strikes again! Reviews like this separate good platforms from great ones.",
        
        # Future Elite Style
        f"🚀 You're on the path to becoming one of our elite trusted reviewers. Keep it up — big rewards ahead!",
        f"🚀 Future elite reviewer alert! Your judgment is becoming legendary on Alpha Nex.",
        f"🚀 Elite reviewers start exactly like this. You're on the fast track to recognition!",
        
        # Founder Speaks Style
        f"🫱 As the founder, I personally thank you. Reviewers like you will shape the future of this platform.",
        f"🫱 From the founding team: Your reviews maintain the quality we dreamed of. Thank you!",
        f"🫱 Founder's appreciation: Your {review_count} reviews prove you understand our quality mission.",
        
        # Competitive Style
        f"🏆 You're already ahead of 90% of users in review quality. That's what we want for our top team!",
        f"🏆 Quality champion! Your reviews consistently outshine others. You're in the elite tier!",
        f"🏆 Your review accuracy is impressive. You're competing with the best reviewers — and leading!",
        
        # Impact Style
        f"🎯 You didn't just review a file — you improved data that might train the next generation of AI!",
        f"🎯 Impact multiplied! Your review helps other users discover quality content. Chain reaction started!",
        f"🎯 This review joins {review_count-1} others in building the smartest content curation system!"
    ]
    
    return random.choice(messages)

def get_xp_milestone_message(user_name, current_xp):
    """Get milestone messages based on XP achievements"""
    messages = []
    
    if current_xp >= 1400:
        messages = [
            f"⚠️ You're at {current_xp} XP! Just {1500-current_xp} XP until account creation is required. You've almost unlocked everything!",
            f"🚨 Final stretch! {1500-current_xp} XP until you join our verified member community. Epic journey so far!",
            f"🔥 You're {1500-current_xp} XP away from the big leagues! Premium features await!"
        ]
    elif current_xp >= 1200:
        messages = [
            f"🌟 You've reached {current_xp} XP! You're in the top tier of users. Account creation coming soon!",
            f"⭐ Superstar level! {current_xp} XP proves you're serious about quality content.",
            f"🎖️ {current_xp} XP puts you ahead of most users. You're building something special!"
        ]
    elif current_xp >= 1000:
        messages = [
            f"🎯 1000+ XP achieved! You're officially a power user. The platform is better because of you!",
            f"💎 Diamond status! {current_xp} XP shows your commitment to excellence.",
            f"🏅 {current_xp} XP! You've joined the exclusive 1000+ club. Premium recognition unlocked!"
        ]
    elif current_xp >= 750:
        messages = [
            f"🚀 {current_xp} XP and climbing! You're becoming a platform veteran. Keep the momentum!",
            f"⚡ Energy level: Maximum! {current_xp} XP shows you're unstoppable.",
            f"📈 {current_xp} XP achieved! Your growth curve is impressive. Future elite material!"
        ]
    elif current_xp >= 500:
        messages = [
            f"✨ {current_xp} XP! You've proven you understand quality. The community notices contributors like you!",
            f"🌱 Growing strong! {current_xp} XP shows you're invested in building something great.",
            f"🎪 {current_xp} XP! You're no longer a beginner. Experienced contributor status achieved!"
        ]
    
    return random.choice(messages) if messages else None

def get_daily_limit_reminder(user_name, uploads_left, reviews_left):
    """Get motivational daily limit reminders"""
    if uploads_left == 0 and reviews_left == 0:
        return f"🎯 You've maximized today's impact! Both upload and review limits reached. Come back tomorrow to continue building!"
    elif uploads_left == 0:
        return f"📤 Upload limit reached for today! You can still review {reviews_left} more files to keep earning XP!"
    elif reviews_left == 0:
        return f"👁️ Review limit reached! You can still upload {uploads_left} more files today. Keep the momentum!"
    else:
        return f"💪 You have {uploads_left} uploads and {reviews_left} reviews remaining today. Make them count!"

def get_welcome_back_message(user_name):
    """Get welcome back messages for returning users"""
    messages = [
        f"🌟 Welcome back! Ready to continue building the future of content curation?",
        f"🚀 You're back! The platform missed your quality contributions. Let's make today even better!",
        f"⚡ Power user is back! Your expertise makes Alpha Nex stronger. What will you create today?",
        f"🎯 Welcome back to your content empire! Every upload and review builds your legacy.",
        f"🏆 The champion returns! Your consistent quality sets the standard for others."
    ]
    
    return random.choice(messages)
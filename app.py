from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Dummy data for demonstration
posts = {
    1: {'title': 'The Radiance of Sunny Holidays: Embracing the Best', 'content': '''
        In a world filled with diverse travel destinations, there's something undeniably captivating about the allure of sunny holidays. 
        Beyond the obvious joy of basking in warmth, these vacations have a unique charm that sets them apart.  Let's explore the reasons why sunny holidays are often considered the best and why they continue to be a favorite among travelers seeking rejuvenation and adventure.

Body:

Warm Embrace of Nature:

There's an intrinsic connection between sunshine and a sense of well-being. The warmth of the sun's rays has a profound impact on our mood and energy levels. Sunny holidays provide the perfect opportunity to immerse oneself in this natural embrace, fostering a feeling of relaxation and happiness. Whether it's lounging on a tropical beach or exploring vibrant landscapes, the sun adds an extra layer of positivity to the travel experience.

Endless Outdoor Adventures:

Sunlit destinations often offer a plethora of outdoor activities. From water sports along the crystalline shores to hiking through lush, sun-kissed trails, sunny holidays open the door to a world of adventure. The abundance of sunlight extends the hours available for exploration, allowing travelers to make the most of their days and create lasting memories.

Golden Hours and Stunning Sunsets:

One of the magical aspects of sunny holidays is the enchanting play of light during golden hours. Whether it's the sunrise casting a golden glow over the landscape or the breathtaking hues of a sunset, these moments become indelible imprints on the traveler's soul. The interplay of colors and shadows creates a visual symphony that elevates the entire vacation experience.

Mood Elevation and Vitamin D Boost:

Scientifically proven, exposure to sunlight triggers the release of serotonin, often referred to as the "happy hormone." Sunny holidays provide an ample supply of this natural mood enhancer, contributing to a sense of joy and relaxation. Additionally, the sun is a rich source of Vitamin D, essential for overall health. Soaking up the sun responsibly becomes a holistic approach to well-being during these vacations.

Culinary Delights and Fresh Fare:

Sunny destinations often boast vibrant culinary scenes. From fresh seafood to tropical fruits, the local cuisine reflects the richness of the region. Dining under the sun or by the beach adds an extra layer of enjoyment to every meal. The connection between food, sunlight, and the natural surroundings creates a sensory experience that lingers in the traveler's memory.

Conclusion:

In the grand tapestry of travel experiences, sunny holidays weave a narrative of warmth, adventure, and well-being. The allure of the sun extends beyond its physical presence, touching the very essence of why we seek to explore the world. Whether you find solace on a sandy shore, thrill in an outdoor escapade, or simply savor the golden moments, sunny holidays stand as a testament to the beauty and brilliance that travel can offer.
        
   ''' },

    2: {'title': 'Embracing the Magic: Why Winter Holidays Are the Best', 'content': '''
        As the days grow shorter and a crisp chill fills the air, winter unveils its enchanting charm, setting the stage for a season of joy and celebration. While each season holds its unique allure, there's something truly magical about winter holidays. Let's delve into the reasons why this frost-kissed period stands out as the best time for creating cherished memories and embracing the warmth within the cold.

Body:

Snow-Covered Landscapes and Winter Wonderland:

Winter blankets the world in a serene layer of snow, transforming landscapes into enchanting wonderlands. The glistening white scenery, adorned with icicles and frost, creates a picturesque backdrop for holiday festivities. Whether it's a walk through snow-laden forests or the joy of building snowmen, the winter landscape fosters a sense of wonder and delight.

Cozy Retreats and Fireside Bliss:

Winter holidays invite us to seek refuge in cozy retreats, nestled by the warmth of crackling fires. The allure of snuggling up with a blanket, sipping hot cocoa, and sharing stories with loved ones creates an intimate and comforting atmosphere. The glow of a fireplace becomes a beacon of solace, inviting us to unwind and connect with the spirit of the season.

Seasonal Delights and Culinary Traditions:

Winter holidays bring with them a delectable array of seasonal treats and culinary traditions. From the aroma of freshly baked gingerbread cookies to the richness of hearty stews, the winter menu is a celebration of comforting flavors. The act of sharing meals with family and friends becomes a cherished ritual, fostering a sense of togetherness and joy.

Festive Lights and Illuminated Spirit:

The sparkle of festive lights illuminates the winter nights, creating a magical ambiance that is synonymous with the holiday season. Streets adorned with twinkling decorations and homes aglow with colorful lights evoke a sense of wonder and anticipation. The act of decorating becomes a joyful expression of creativity and a collective celebration of the season.

Winter Sports and Outdoor Adventures:

For those seeking a dose of adrenaline, winter holidays offer a playground of outdoor adventures. From the thrill of skiing down snowy slopes to the tranquility of ice skating on frozen lakes, winter sports provide a unique way to embrace the season's energy. The crisp, cold air becomes invigorating, and the snowy landscapes become a canvas for exhilarating activities.

Conclusion:

In the tapestry of seasons, winter holidays emerge as a time of enchantment, warmth, and shared joy. The unique blend of snowy landscapes, cozy retreats, culinary delights, festive lights, and outdoor adventures creates an unparalleled experience. As winter wraps the world in its chilly embrace, it invites us to embrace the magic within, making it the best time to celebrate, connect, and create lasting memories with loved ones. Winter holidays, with their ethereal charm, beckon us to slow down, savor the moment, and revel in the beauty of the season.

    '''},
}

# Routes for different sections of the website

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process form data and log the user in
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required  # Ensure that only logged-in users can access this route
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists.')

        # Check if the password and confirm_password match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match.')

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = posts.get(post_id)
    if post:
        return render_template('post.html', post=post)
    else:
        return render_template('not_found.html')
    
@app.route('/full_post/<int:post_id>')
def full_post(post_id):
    post = posts.get(post_id)
    return render_template('full_post.html', post=post)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    # Handle form submission for creating a new post
    if request.method == 'POST':
        # Process form data and add the new post to the 'posts' data structure
        # Dummy implementation for demonstration
        title = request.form.get('title')
        content = request.form.get('content')
        new_post_id = max(posts.keys()) + 1
        posts[new_post_id] = {'title': title, 'content': content}
        return redirect(url_for('index'))

    return render_template('new_post.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

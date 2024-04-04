from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from rss_fetcher import fetch_rss_feed
from summarizer import generate_daily_summary
from datetime import date
from sqlalchemy.dialects.postgresql import JSONB
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can safely get the API key
database_url = os.getenv('DATABASE_URL')

app = Flask(__name__)
postgres_username = 'alexanderbricken'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class DailySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today, unique=True)
    summary = db.Column(db.Text, nullable=False)
    links = db.Column(JSONB, nullable=False)

    def __repr__(self):
        return f'<DailySummary {self.date}>'

# Create the tables in the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Daily Summary API!"

@app.route('/api/summaries')
def get_summaries():
    # Fetch RSS feed data
    articles, links = fetch_rss_feed()

    # Extract article titles
    titles = [article['title'] for article in articles]

    # Generate daily summary
    summary = generate_daily_summary(titles)

    # Store the daily summary in the database
    today = date.today()
    daily_summary = DailySummary(date=today, summary=summary, links=links)
    db.session.add(daily_summary)
    db.session.commit()

    return jsonify({'date': today.strftime('%Y-%m-%d'), 'summary': summary, 'links': links})

@app.route('/api/summaries/all')
def get_all_summaries():
    summaries = DailySummary.query.all()
    result = []
    for summary in summaries:
        result.append({
            'id': summary.id,
            'date': summary.date.strftime('%Y-%m-%d'),
            'summary': summary.summary,
            'links': summary.links
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
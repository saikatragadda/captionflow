CaptionFlow
CaptionFlow generates social media captions for Instagram, TikTok, and LinkedIn. You enter your niche and what the post is about, pick a platform, tone, and length, and it gives you two caption options with hashtags.
Live: https://captionflow.onrender.com (password protected)
How it works
Users log in with an access password. Login is stored in a Flask session.
The form sends niche, topic, platform, tone, and length to the /generate endpoint.
The backend builds the prompt from those inputs. Platform and length rules are kept in two dictionaries (PLATFORM_RULES and LENGTH_RULES), so adding a new platform is a one-line change.
The prompt is sent to Claude Haiku 4.5 through the Anthropic API, and the captions are returned to the page.
I went with Haiku because captions are a short task and it's fast and cheap. max_tokens is capped at 1200 to keep the cost per request predictable.
Stack
Python, Flask
Anthropic API (Claude Haiku 4.5)
Gunicorn
Render (redeploys automatically on push to main)
Gumroad for checkout

Files
app.py             routes, login, prompt building, API call
templates/         login.html and index.html
requirements.txt   dependencies
Procfile           start command for Render

Running it locally
git clone https://github.com/saikatragadda/captionflow.git
cd captionflow
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
export ACCESS_PASSWORD=any_password
export SECRET_KEY=any_random_string
python app.py

Then go to http://localhost:5000
On Render, the same three values are set as environment variables. Nothing secret is stored in the repo.
What I'd improve next
Everyone shares one password right now. I'd like to move to individual access per purchase.
There's no rate limiting, and since it's a one-time purchase, API cost per user isn't capped. A daily limit per user would fix that.
No tests yet. The prompt-building logic would be the first thing to test.

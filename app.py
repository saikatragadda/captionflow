from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import anthropic
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "captionflow-secret-2026")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

ACCESS_PASSWORD = os.environ.get("ACCESS_PASSWORD", "captionflow2026")

PLATFORM_RULES = {
    "Instagram":     "Use line breaks for readability. Add a call-to-action. Include 20-25 relevant hashtags at the end.",
    "TikTok":        "Hook in the very first line. Keep it punchy and energetic. Include 5-10 trending hashtags.",
    "LinkedIn":      "2-3 short paragraphs. End with a thought-provoking question to drive comments. Include 3-5 professional hashtags.",
    "All platforms": "Generate 3 separate captions labeled Instagram, TikTok, and LinkedIn. Each should follow platform best practices with appropriate hashtags."
}

LENGTH_RULES = {
    "short":  "Keep the caption very short — 1-3 sentences max. Punchy and to the point.",
    "medium": "Write a medium-length caption — 3-6 sentences. Balanced and engaging.",
    "long":   "Write a detailed long-form caption — 7-12 sentences. Tell a story, go deep."
}

@app.route("/")
def index():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if password == ACCESS_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("index"))
        else:
            error = "Incorrect password. Purchase access at captionflow.gumroad.com"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/generate", methods=["POST"])
def generate():
    if not session.get("authenticated"):
        return jsonify({"error": "Unauthorized"}), 401

    data     = request.json
    niche    = data.get("niche", "").strip()
    topic    = data.get("topic", "").strip()
    platform = data.get("platform", "Instagram")
    tone     = data.get("tone", "Casual & fun")
    length   = data.get("length", "medium")

    if not niche or not topic:
        return jsonify({"error": "Please fill in all fields."}), 400

    prompt = f"""You are an expert social media copywriter specializing in viral content.

Create captions for a content creator in the "{niche}" niche.

Post topic: {topic}
Tone: {tone}
Length rule: {LENGTH_RULES.get(length, LENGTH_RULES["medium"])}
Platform: {PLATFORM_RULES.get(platform, PLATFORM_RULES["Instagram"])}

Deliver exactly 2 caption variations labeled "Caption 1" and "Caption 2".
Each caption should have its hashtags listed directly below it.
No extra commentary, no explanations — just the captions, ready to copy and post."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"result": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

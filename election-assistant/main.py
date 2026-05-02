from flask import Flask, render_template, request, jsonify
from google.cloud import translate_v2 as translate
from flask_cors import CORS
from flask_compress import Compress
import functools
import time
import logging
import google.cloud.logging
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
Compress(app)
CORS(app)
translate_client = translate.Client()

client = google.cloud.logging.Client()
client.setup_logging()

if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
ELECTION_INFO = {
    "eligibility": "To vote in India, you must be an Indian citizen, at least 18 years of age on the qualifying date (usually Jan 1st), and registered as a voter in the constituency where you reside.",
    "registration": "You can register online via voterportal.eci.gov.in. Step 1: Create an account. Step 2: Fill out Form 6 for new voter registration. Step 3: Upload required documents (age and address proof). Step 4: Submit and track your application status.",
    "timeline": "Indian elections follow a typical timeline: 1) Announcement of dates and enforcement of the Model Code of Conduct (MCC). 2) Filing of nominations by candidates. 3) Scrutiny of nominations and withdrawal. 4) Campaigning period. 5) Voting day(s) in phases. 6) Counting of votes and declaration of results.",
    "voting_process": "On election day, go to your designated polling booth. Show your EPIC (Voter ID) or other valid ID. Your name will be checked on the electoral roll. An official will ink your finger, and you will proceed to the voting compartment to cast your vote using the EVM and verify via the VVPAT slip.",
    "candidates": "Candidates must be Indian citizens and at least 25 years old for Lok Sabha. They must file nomination papers with the Returning Officer along with an affidavit of assets, liabilities, and criminal background. A security deposit is required (e.g., Rs. 25,000 for Lok Sabha).",
    "results": "Votes are counted under the supervision of the Returning Officer after all phases of polling are complete. EVMs are brought from strong rooms, unsealed, and the votes recorded are tallied. The candidate with the highest number of votes in the constituency is declared the winner.",
    "evm": "An EVM (Electronic Voting Machine) consists of a Control Unit and a Balloting Unit. Instead of paper ballots, voters press a button next to the candidate's symbol. EVMs are standalone machines without internet connectivity, ensuring they cannot be hacked remotely.",
    "mcc": "The Model Code of Conduct (MCC) is a set of guidelines issued by the Election Commission to regulate political parties and candidates prior to elections. It ensures free and fair elections by preventing ruling parties from misusing official machinery and maintaining a level playing field."
}

@functools.lru_cache(maxsize=128)
def get_election_response(user_message):
    message = user_message.lower()
    
    if "eligibility" in message:
        return ELECTION_INFO["eligibility"]
    elif "register" in message or "registration" in message:
        return ELECTION_INFO["registration"]
    elif "timeline" in message:
        return ELECTION_INFO["timeline"]
    elif "vote" in message or "booth" in message or "voting" in message:
        return ELECTION_INFO["voting_process"]
    elif "candidate" in message:
        return ELECTION_INFO["candidates"]
    elif "result" in message:
        return ELECTION_INFO["results"]
    elif "evm" in message:
        return ELECTION_INFO["evm"]
    elif "mcc" in message or "code of conduct" in message:
        return ELECTION_INFO["mcc"]
    else:
        return "I am an election assistant. I can help you with topics like eligibility, registration, timeline, voting process, candidates, results, EVMs, and the MCC. Please ask me a specific question!"

@app.route("/")
def home():
    logging.info("Accessed home route")
    return render_template("index.html"), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        logging.error("Chat request failed: No message provided")
        return jsonify({"error": "No message provided"}), 400
    
    user_message = str(data["message"]).strip()[:500]
    if not user_message:
        logging.error("Chat request failed: Message is empty")
        return jsonify({"error": "Message cannot be empty"}), 400
        
    logging.info(f"Received chat message: {user_message}")
    reply = get_election_response(user_message)
    
    if "hindi" in user_message.lower() or "translate to hindi" in user_message.lower():
        logging.info("Translating response to Hindi")
        result = translate_client.translate(reply, target_language="hi")
        reply = result["translatedText"]
        
    logging.info(f"Sending reply: {reply[:100]}...")
    return jsonify({"reply": reply}), 200

@app.route("/timeline", methods=["GET"])
def timeline():
    logging.info("Accessed timeline route")
    phases = [
        {"phase": "Announcement & MCC", "duration": "Day 1", "description": "Election Commission announces dates; Model Code of Conduct comes into force.", "emoji": "📢"},
        {"phase": "Voter List Finalization", "duration": "Before Nominations", "description": "Final electoral rolls are published. Last chance for voter registration updates.", "emoji": "📝"},
        {"phase": "Nomination Filing", "duration": "Usually 7 Days", "description": "Candidates submit their nomination papers and affidavits to the Returning Officer.", "emoji": "✍️"},
        {"phase": "Scrutiny of Nominations", "duration": "1 Day", "description": "Returning Officer verifies the submitted documents for validity.", "emoji": "🔎"},
        {"phase": "Campaign Period", "duration": "Approx 14 Days", "description": "Candidates and parties campaign through rallies, manifestos, and outreach.", "emoji": "📣"},
        {"phase": "Silent Period", "duration": "48 Hours Before Polling", "description": "All public campaigning stops to allow voters a peaceful time to decide.", "emoji": "🤫"},
        {"phase": "Voting Day", "duration": "1 Day (Per Phase)", "description": "Voters cast their votes at designated polling booths using EVMs.", "emoji": "🗳️"},
        {"phase": "Vote Counting", "duration": "1 Day", "description": "EVMs are unsealed and votes are counted under strict supervision.", "emoji": "🧮"},
        {"phase": "Results Declaration", "duration": "Same Day as Counting", "description": "The candidate with the most votes wins. Winning party forms government.", "emoji": "🏆"}
    ]
    return jsonify(phases), 200

@app.route("/search", methods=["GET"])
def search():
    """Returns a Google Search URL for the given query."""
    query = request.args.get("q", "")
    logging.info(f"Accessed search route with query: {query}")
    import urllib.parse
    # URL encode the query to ensure special characters are handled
    encoded_query = urllib.parse.quote(query)
    # Construct the search URL with "India election" prefix
    search_url = f"https://www.google.com/search?q=India+election+{encoded_query}"
    knowledge_url = f"https://www.google.com/search?q={encoded_query}+Election+Commission+of+India"
    return jsonify({"search_url": search_url, "knowledge_url": knowledge_url}), 200

@app.route("/googlesearch", methods=["GET"])
def googlesearch():
    query = request.args.get("q", "")
    logging.info(f"Accessed googlesearch route with query: {query}")
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q=India+election+{encoded_query}"
    knowledge_url = f"https://www.google.com/search?q={encoded_query}+Election+Commission+of+India"
    return jsonify({"search_url": search_url, "knowledge_url": knowledge_url}), 200

@app.route("/nearbyoffice", methods=["GET"])
def nearbyoffice():
    city = request.args.get("city", "")
    logging.info(f"Accessed nearbyoffice route with city: {city}")
    import urllib.parse
    encoded_city = urllib.parse.quote(city)
    maps_url = f"https://www.google.com/maps/search/election+commission+office+in+{encoded_city}"
    message = f"Find election office in {city}"
    return jsonify({"maps_url": maps_url, "message": message}), 200

@app.route("/static_map", methods=["GET"])
def static_map():
    logging.info("Accessed static_map route")
    embed_url = "https://maps.google.com/maps?q=Election+Commission+of+India,+New+Delhi&t=&z=15&ie=UTF8&iwloc=&output=embed"
    return jsonify({"embed_url": embed_url}), 200

@app.route("/health", methods=["GET"])
def health():
    logging.info("Accessed health route")
    return jsonify({"status": "healthy", "timestamp": time.time()}), 200

@app.route("/save", methods=["POST"])
def save_chat():
    data = request.get_json()
    if not data or "user_message" not in data or "bot_reply" not in data:
        return jsonify({"error": "Missing user_message or bot_reply"}), 400
        
    try:
        doc_ref = db.collection('chat_history').document()
        doc_ref.set({
            'user_message': data['user_message'],
            'bot_reply': data['bot_reply'],
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        logging.info("Chat saved to Firestore")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error saving to Firestore: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
        
    text = data["text"]
    logging.info("Translating text to Hindi via /translate route")
    try:
        result = translate_client.translate(text, target_language="hi")
        return jsonify({"translated_text": result["translatedText"]}), 200
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history():
    try:
        chats_ref = db.collection('chat_history').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        docs = chats_ref.stream()
        
        history = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if 'timestamp' in doc_dict and doc_dict['timestamp']:
                try:
                    doc_dict['timestamp'] = doc_dict['timestamp'].isoformat()
                except AttributeError:
                    pass
            history.append(doc_dict)
            
        logging.info("Fetched chat history from Firestore")
        return jsonify({"history": history}), 200
    except Exception as e:
        logging.error(f"Error fetching from Firestore: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run on Antigravity default port 8080 and expose to all network interfaces
    app.run(host="0.0.0.0", port=8080, debug=True)

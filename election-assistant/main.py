from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data["message"]
    reply = get_election_response(user_message)
    return jsonify({"reply": reply})

@app.route("/timeline", methods=["GET"])
def timeline():
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
    return jsonify(phases)

@app.route("/search", methods=["GET"])
def search():
    """Returns a Google Search URL for the given query."""
    query = request.args.get("q", "")
    import urllib.parse
    # URL encode the query to ensure special characters are handled
    encoded_query = urllib.parse.quote(query)
    # Construct the search URL with "India election" prefix
    search_url = f"https://www.google.com/search?q=India+election+{encoded_query}"
    return jsonify({"search_url": search_url})

if __name__ == "__main__":
    # Run on Antigravity default port 8080 and expose to all network interfaces
    app.run(host="0.0.0.0", port=8080, debug=True)

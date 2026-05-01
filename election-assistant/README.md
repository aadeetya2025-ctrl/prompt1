# Election Process Assistant

## 1. Chosen Vertical
**Civic Education / Public Awareness**

## 2. Approach and Logic
This project is an interactive, keyword-matching chatbot built with Flask. Its primary goal is to help citizens understand the intricacies of the Indian election process. Through an intuitive chat interface and a visual timeline, users can ask questions and explore step-by-step information regarding how elections are conducted. The logic relies on matching user input against predefined keywords to return accurate, beginner-friendly explanations.

## 3. How the Solution Works
The application is composed of a lightweight backend and a responsive frontend:
*   **Flask Backend (`main.py`)**: Handles the core application logic and serves the web pages.
*   **Knowledge Base (`ELECTION_INFO`)**: A centralized Python dictionary containing detailed, curated information on topics such as voter eligibility, registration, candidates, EVMs, and the Model Code of Conduct.
*   **`/chat` Route**: A POST endpoint that receives the user's message, extracts relevant keywords using a custom matching function, and returns the appropriate educational response as JSON.
*   **`/timeline` Route**: A GET endpoint that returns a structured JSON list of all the major phases in the Indian general election timeline.
*   **Frontend Chat UI (`templates/index.html`)**: A clean, responsive HTML/CSS/JS interface that uses the `fetch()` API to communicate with the backend asynchronously, allowing users to chat seamlessly and view a dynamic vertical timeline without page reloads.

## 4. Assumptions Made
*   The application operates within the context of the **Indian General Election (Lok Sabha)**.
*   The primary language of interaction is **English**.
*   Users are accessing the application via a browser with standard JavaScript and CSS support.

## 5. Google Services Used
Deployed via **Google Antigravity** (Google Cloud).

## 6. Setup Instructions

To run this application locally on your machine, follow these steps:

1. Install the required dependencies:
   ```bash
   pip install flask
   ```

2. Start the application:
   ```bash
   python main.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000/
   ```

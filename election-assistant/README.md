# Election Process Assistant

## 1. Chosen Vertical
Civic Education and Public Awareness

## 2. Approach and Logic
AI-powered Flask chatbot with full Google Services integration.

## 3. How the Solution Works
The application uses a Flask backend with a responsive frontend, exposing the following routes:
- `/chat`: Core chatbot interface processing user queries and returning context-aware election info.
- `/timeline`: Provides structured phases of the Indian election timeline.
- `/translate`: Uses the official Google Cloud Translation API to translate text to Hindi.
- `/nearbyoffice`: Generates Google Maps Search URLs to locate election offices by city.
- `/save`: Securely logs user chat sessions and bot replies to Firebase Firestore.
- `/history`: Retrieves the most recent chat messages from Firestore history.
- `/health`: Health-check endpoint for server uptime monitoring.

## 4. Google Services Used
- **Google Cloud Run**: Serverless production deployment.
- **Google Cloud Logging**: Integrated structured logging for seamless observability.
- **Google Cloud Translation API**: Dynamic, accurate English to Hindi text translation.
- **Firebase Firestore**: Secure, scalable NoSQL database for saving chat history.
- **Google Maps Embed API**: Interactive frontend maps for pinpointing local election offices.

## 5. Testing
Comprehensive `pytest` suite featuring 12 tests covering all major routes, success/error states, and edge cases. Supported by `pytest-cov` for automated test coverage reporting.

## 6. Security
Secured using JWT token authentication (`flask-jwt-extended`) for sensitive routes, strict HTTP security headers (Helmet-style HSTS, CSP, X-Frame-Options), request size limiting, and rigorous XSS input sanitization via `bleach`.

## 7. Live URL
[https://election-assistant-526669661692.us-central1.run.app](https://election-assistant-526669661692.us-central1.run.app)

## 8. GitHub
[https://github.com/aadeetya2025-ctrl/prompt1](https://github.com/aadeetya2025-ctrl/prompt1)

---

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests with coverage:
   ```bash
   pytest test_app.py -v --cov=main
   ```

3. Start the application locally:
   ```bash
   python main.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8080/
   ```

# Election Process Assistant

## 1. Chosen Vertical
Civic Education and Public Awareness

## 2. Approach and Logic
Keyword-based Flask chatbot with Google Services integration.

## 3. How the Solution Works
Flask backend with `/chat`, `/timeline`, `/nearbyoffice`, `/googlesearch`, `/translate` routes and a responsive chat frontend.

## 4. Google Services Used
Google Translate API via `googletrans`, Google Maps Search URLs, Google Custom Search URLs, deployed on Google Cloud Run.

## 5. Testing
`pytest` test suite with 6 tests covering all major routes.

## 6. Assumptions
Indian election context, English and Hindi language support.

## 7. Live URL
[https://election-assistant-526669661692.us-central1.run.app](https://election-assistant-526669661692.us-central1.run.app)

## 8. GitHub
[https://github.com/aadeetya2025-ctrl/prompt1](https://github.com/aadeetya2025-ctrl/prompt1)

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest test_app.py
   ```

3. Start the application:
   ```bash
   python main.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8080/
   ```

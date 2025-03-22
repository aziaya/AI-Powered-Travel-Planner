```markdown
# AI Travel Planner

TravelPlannerAI is a FastAPI-based application that provides a travel planning assistant powered by LangChain and Ollama. It offers both RESTful and WebSocket APIs for generating detailed travel guides and real-time travel-related conversations. The application is designed to help users plan trips, get itinerary suggestions, and receive real-time travel advice in Markdown format.

## Features

- **RESTful API**: Generate detailed travel guides in JSON format.
- **WebSocket API**: Stream real-time travel advice in Markdown format.
- **Travel-Only Context**: Ensures all responses are related to travel planning.
- **Markdown Support**: Responses are formatted in Markdown for better readability.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TravelPlannerAI.git
   cd TravelPlannerAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### RESTful API

- **POST `/generate-travel-guide`**:
  - **Request Body**:
    ```json
    {
      "destinations": ["Serengeti", "Zanzibar"],
      "travel_dates": {
        "start_date": "2023-12-01",
        "end_date": "2023-12-10"
      },
      "interests": ["wildlife safaris", "beach holidays"],
      "user_budget": "luxury",
      "number_of_travellers": 4
    }
    ```
  - **Response**:
    ```json
    {
      "overview": "...",
      "itinerary_suggestions": {...},
      "tips_and_recommendations": {...},
      "must_visit_attractions": {...},
      "activities_and_experiences": {...},
      "itinerary_example": [...],
      "budget_breakdown": {...},
      "safety_tips": [...],
      "conclusion": "..."
    }
    ```

### WebSocket API

- **WebSocket `/ws/travel-chat`**:
  - **Client Request**:
    ```javascript
    const ws = new WebSocket("ws://localhost:8000/ws/travel-chat");
    ws.send("Plan a 7-day luxury trip to Serengeti and Zanzibar.");
    ```
  - **Server Response** (streamed in Markdown):
    ```markdown
    ### Day 1: Arrival in Serengeti
    - **Morning**: Arrive at Kilimanjaro International Airport.
    - **Afternoon**: Transfer to Serengeti National Park by private vehicle.
    - **Evening**: Check into the Four Seasons Safari Lodge.
    ```

## Example Usage

### RESTful API Example

```bash
curl -X POST "http://localhost:8000/generate-travel-guide" \
-H "Content-Type: application/json" \
-d '{
  "destinations": ["Serengeti", "Zanzibar"],
  "travel_dates": {
    "start_date": "2023-12-01",
    "end_date": "2023-12-10"
  },
  "interests": ["wildlife safaris", "beach holidays"],
  "user_budget": "luxury",
  "number_of_travellers": 4
}'
```

### WebSocket API Example (JavaScript)

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/travel-chat");

ws.onopen = () => {
    console.log("WebSocket connection established");
    ws.send("Plan a 7-day luxury trip to Serengeti and Zanzibar.");
};

ws.onmessage = (event) => {
    console.log("Received:", event.data);
};

ws.onclose = () => {
    console.log("WebSocket connection closed");
};
```

## Project Structure

```
TravelPlannerAI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   └── utils.py
├── .env
├── requirements.txt
└── README.md
```

### Key Files

- **`app/main.py`**: Contains the FastAPI app and API endpoints.
- **`app/services.py`**: Implements the logic for generating travel guides and streaming responses.
- **`app/models.py`**: Defines Pydantic models for input and output validation.
- **`.env`**: Stores environment variables like `OLLAMA_BASE_URL`.
- **`requirements.txt`**: Lists all Python dependencies.

## Commit Messages

1. **Initial commit**: Set up the FastAPI project structure.
2. **feat: Add RESTful API for travel guide generation**: Implemented the `/generate-travel-guide` endpoint.
3. **feat: Add WebSocket API for real-time travel advice**: Implemented the `/ws/travel-chat` endpoint.
4. **docs: Add README.md**: Added comprehensive documentation for the project.
5. **fix: Handle malformed JSON output**: Fixed JSON parsing issues in the RESTful API.
6. **chore: Update dependencies**: Added required dependencies to `requirements.txt`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

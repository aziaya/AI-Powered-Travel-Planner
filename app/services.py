import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


def generate_travel_guide(destinations: list, travel_dates: dict, interests: list, user_budget: str, number_of_travellers: int) -> dict:
    # Load environment variables
    base_url = os.getenv("OLLAMA_BASE_URL")

    # Define the model
    model = "llama3.2:1b"

    # Initialize the ChatOllama instance
    llm = ChatOllama(
        base_url=base_url,
        model=model,
        temperature=0.9,
    )

    # Define the HumanMessage prompt template for the question
    question = HumanMessagePromptTemplate.from_template(
        """
        Give me a travel guide for visiting the following destinations: {destinations}.
        Travel Dates: {start_date} to {end_date}.
        Interests: {interests}.
        User Budget: {user_budget}.
        Number of Travellers: {number_of_travellers}.
        """
    )

    # Define the SystemMessage prompt template with dynamic instructions
    system = SystemMessagePromptTemplate.from_template(
        """
        You are a travel agent. Answer only questions related to travel. 
        The response must be in JSON format. Return the results in the following JSON structure:

        {{
          "overview": "A brief overview of the travel guide",
          "itinerary_suggestions": {{
            "region_name": [
              {{
                "location": "Name of the location",
                "activity": "Description of the activity"
              }}
            ]
          }},
          "tips_and_recommendations": {{
            "key_tip": "Description of the tip"
          }},
          "must_visit_attractions": {{
            "region_name": [
              {{
                "location": "Name of the location",
                "activities": [
                  "Description of activity 1",
                  "Description of activity 2"
                ]
              }}
            ]
          }},
          "activities_and_experiences": {{
            "category": [
              "Description of activity or experience"
            ]
          }},
          "itinerary_example": [
            {{
              "day": "Day 1",
              "location": "Name of the location (e.g., Kenya)",
              "date_time": "Day of the week and date (e.g., Thursday, Mar 27)",
              "list_of_images": [
                {{
                  "image_title": "Title of the image (e.g., Lion Pride)",
                  "image_url": "URL of the image",
                  "image_description": "Description of the image (e.g., Majestic Lion Pride in the Savannah)"
                }}
              ],
              "activities": [
                "Activity 1 (e.g., Morning safari game drive)",
                "Activity 2 (e.g., Traditional lunch experience)",
                "Activity 3 (e.g., Evening cultural show)",
                "Activity 4 (e.g., Sunset photography session)"
              ],
              "accommodations": [
                "Name of the accommodation (e.g., Giraffe Manor)"
              ],
              "included_meals": [
                "Breakfast",
                "Lunch",
                "Dinner"
              ]
            }}
          ],
          "budget_breakdown": {{
            "category": {{
              "subcategory": "Description of the cost"
            }}
          }},
          "safety_tips": [
            "Description of safety tip"
          ],
          "conclusion": "A brief conclusion of the travel guide"
        }}

        Replace the placeholders (e.g., region_name, location, activity, etc.) with the actual data provided. Ensure the JSON structure remains consistent.
        """
    )

    # Define the messages for the ChatPromptTemplate
    messages = [system, question]

    # Create the ChatPromptTemplate
    template = ChatPromptTemplate(messages)

    # Define the chain for generating the travel guide
    chain = template | llm | StrOutputParser()

    # Invoke the chain with the input parameters
    output = chain.invoke({
        "destinations": ", ".join(destinations),
        "start_date": travel_dates["start_date"],
        "end_date": travel_dates["end_date"],
        "interests": ", ".join(interests),
        "user_budget": user_budget,
        "number_of_travellers": number_of_travellers
    })

    # Clean the output string
    output = output.strip()

    # Parse the JSON string into a Python dictionary
    try:
        # Remove the "output" key if present
        if output.startswith("{"):
            return json.loads(output)
        elif output.startswith('{"output":'):
            # Extract the inner JSON string
            output_dict = json.loads(output)
            return json.loads(output_dict["output"])
        else:
            raise ValueError("Invalid JSON format: Output does not start with '{'")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON output: {e}")





# Initialize the ChatOllama instance
def get_chat_ollama():
    base_url = os.getenv("OLLAMA_BASE_URL")
    model = "llama3.2:1b"
    return ChatOllama(
        base_url=base_url,
        model=model,
        temperature=0.9,
    )


# Function to handle WebSocket streaming
async def stream_travel_response(websocket, prompt: str):
    llm = get_chat_ollama()

    # Define the SystemMessage prompt template for travel-related questions
    system = SystemMessagePromptTemplate.from_template(
        """
        You are a travel agent. Answer only questions related to travel planning.
        The response must be in Markdown format.
        """
    )

    # Define the HumanMessage prompt template for the user's question
    question = HumanMessagePromptTemplate.from_template("{prompt}")

    # Define the messages for the ChatPromptTemplate
    messages = [system, question]

    # Create the ChatPromptTemplate
    template = ChatPromptTemplate(messages)

    # Define the chain for generating the response
    chain = template | llm | StrOutputParser()

    # Stream the response in real-time
    async for chunk in chain.astream({"prompt": prompt}):
        await websocket.send_text(chunk)
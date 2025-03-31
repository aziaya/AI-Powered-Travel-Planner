import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import date
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq


load_dotenv(".env")

# Load environment variables
base_url = os.getenv("OLLAMA_BASE_URL")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")
# print("GROQ_API_KEY:", GROQ_API_KEY)

if not base_url:
    raise ValueError("OLLAMA_BASE_URL not found in .env file")

# Define the model
model = "llama3.2:3b"

# Initialize the ChatOllama instance
# llm = ChatOllama(
#     base_url=base_url,
#     model=model,
#     temperature=0.7,
# )


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Input Model
class TravelQuery(BaseModel):
    destinations: str
    start_date: date
    end_date: date
    interests: str
    user_budget: float
    number_of_travellers: int

# Output Models (unchanged)
class ImageItem(BaseModel):
    image_title: str
    image_url: str
    image_description: str

# class ItinerarySuggestionItem(BaseModel):
#     location: str
#     activity: List[str]

class AccommodationItem(BaseModel):
    name: str
    location: str
    amenities: List[str]
    type: str
    description: str
    price_per_night: float

class MustVisitAttractionItem(BaseModel):
    location: str
    activities: List[str]

class ItineraryDay(BaseModel):
    day: str
    location: str
    date_time: str
    list_of_images: List[ImageItem]
    activities: List[str]
    activities_and_experiences: Dict[str, List[str]]
    accommodations: List[AccommodationItem]
    includes: List[str]
    excludes: List[str]

class TravelGuideResponse(BaseModel):
    overview: str
    # itinerary_suggestions: Dict[str, List[ItinerarySuggestionItem]]
    tips_and_recommendations: Dict[str, str]
    must_visit_attractions: Dict[str, List[MustVisitAttractionItem]]

    # itinerary_example: List[ItineraryDay]
    itinerary: List[ItineraryDay]
    budget_breakdown: Dict[str, Dict[str, str]]
    safety_tips: List[str]
    conclusion: str

# Budget tier logic
def get_budget_tier(user_budget: float) -> str:
    if 1000 <= user_budget <= 2000:
        return "Budget"
    elif 2000 < user_budget <= 4000:
        return "Comfort"
    elif user_budget > 4000:
        return "Luxury"
    else:
        raise ValueError("Budget must be at least $1000")

budget_tiers = {
    "Budget": {
        "range": "$500 - $2000",
        "accommodations": "3-star accommodations",
        "tours": "Group tours",
        "transportation": "Local transportation",
        "meals": "Basic meals included",
        "extras": "Guided city tours"
    },
    "Comfort": {
        "range": "$2000 - $4000",
        "accommodations": "4-star accommodations",
        "tours": "Private tours",
        "transportation": "Private transportation",
        "meals": "Premium meals included",
        "extras": "Professional photography session"
    },
    "Luxury": {
        "range": "$4000+",
        "accommodations": "5-star luxury resorts",
        "tours": "VIP experiences",
        "transportation": "Luxury vehicle transfers",
        "meals": "Gourmet dining",
        "extras": "Personal concierge service"
    }
}

output_parser = JsonOutputParser(pydantic_object=TravelGuideResponse)

# Updated prompt
prompt = PromptTemplate(
    template="""
    You are a travel agent tasked with creating a detailed travel guide. Based on the following details:
    - Destinations: {destinations}
    - Travel Dates: {start_date} to {end_date}
    - Interests: {interests}
    - Budget: {user_budget} (Tier: {budget_tier}, {budget_description})
    - Travelers: {number_of_travellers}

    Generate a comprehensive travel guide focusing on national parks, wildlife tours, safaris, and city tours. Tailor the guide to the budget tier:
    - Budget ($1000-$2000): 3-star accommodations, group tours, local transportation, basic meals, guided city tours
    - Comfort ($2000-$4000): 4-star accommodations, private tours, private transportation, premium meals, photography session
    - Luxury ($4000+): 5-star resorts, VIP experiences, luxury transfers, gourmet dining, concierge service

    Return a valid JSON object with actual travel guide content (e.g., specific activities, locations, and budget breakdowns), not the schema. Use this structure as a guide:

    {format_instructions}

    Rules:
    1. Fill in the JSON with relevant data based on the query and budget tier.
    2. Ensure dates in the itinerary match the travel period ({start_date} to {end_date}).
    3. Keep budget recommendations within the user's budget tier.
    4. Provide a detailed itinerary with activities, accommodations, and meals.
    5. Include safety tips and a conclusion summarizing the travel experience.
    6. Use the budget tier to guide the level of detail and luxury in the recommendations.
    7. Ensure the JSON is valid and well-structured.
    8. Make sure to include list of activities, accommodations, and meals in the in each itinerary.
    9. Include a budget breakdown with specific costs for each category.    
    10. Do not repeat the schema; provide only the populated JSON output.
    """,
    input_variables=["destinations", "start_date", "end_date", "interests", "user_budget", "number_of_travellers", "budget_tier", "budget_description"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

# Example query
query = TravelQuery(
    destinations="Serengeti, Ngorongoro",
    start_date=date(2024, 6, 1),
    end_date=date(2024, 6, 7),
    interests="wildlife photography, cultural experiences",
    user_budget=5000.00,  # Luxury tier
    number_of_travellers=2
)

# Determine budget tier
budget_tier = get_budget_tier(query.user_budget)
budget_description = ", ".join([f"{k}: {v}" for k, v in budget_tiers[budget_tier].items()])

chain = prompt | llm | output_parser

output = chain.invoke({
    "destinations": query.destinations,
    "start_date": query.start_date.isoformat(),
    "end_date": query.end_date.isoformat(),
    "interests": query.interests,
    "user_budget": query.user_budget,
    "number_of_travellers": query.number_of_travellers,
    "budget_tier": budget_tier,
    "budget_description": budget_description
})

print(output)
# try:
#     parsed_output = output_parser.parse(output.content)
#     print("Parsed output:", parsed_output)
# except Exception as e:
#     print("Parsing error:", e)

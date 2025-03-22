from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ImageSchema(BaseModel):
    image_title: str
    image_url: Optional[str] = ""
    image_description: str

class DayItinerarySchema(BaseModel):
    day: str
    location: str
    date_time: str
    list_of_images: List[ImageSchema]
    activities: List[str]
    accommodations: List[str]
    included_meals: List[str]

class TravelGuideOutput(BaseModel):
    overview: str
    itinerary_suggestions: dict
    tips_and_recommendations: dict
    must_visit_attractions: dict
    activities_and_experiences: dict
    itinerary_example: List[DayItinerarySchema]
    budget_breakdown: dict
    safety_tips: List[str]
    conclusion: str

class TravelGuideInput(BaseModel):
    destinations: List[str]
    travel_dates: dict  # {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}
    interests: List[str]
    user_budget: str  # "comfort", "luxury", or "budget"
    number_of_travellers: int
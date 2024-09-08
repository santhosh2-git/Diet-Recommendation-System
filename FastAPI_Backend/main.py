from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
import pandas as pd
from model import recommend, output_recommended_recipes

# Load dataset
dataset = pd.read_csv('../Data/dataset.csv', compression='gzip')

app = FastAPI()

class Params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class PredictionIn(BaseModel):
    nutrition_input: List[float] = Field(..., min_items=9, max_items=9)
    ingredients: Optional[List[str]] = []
    params: Optional[Params]

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: List[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: List[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None

@app.get("/")
async def home():
    return {"health_check": "OK"}

@app.post("/predict/", response_model=PredictionOut)
async def update_item(prediction_input: PredictionIn):
    recommendation_dataframe = recommend(dataset, prediction_input.nutrition_input, prediction_input.ingredients, prediction_input.params.dict())
    output = output_recommended_recipes(recommendation_dataframe)
    
    # Convert numeric values to strings in output
    for recipe in output or []:
        recipe['CookTime'] = str(recipe['CookTime'])
        recipe['PrepTime'] = str(recipe['PrepTime'])
        recipe['TotalTime'] = str(recipe['TotalTime'])
    
    if output is None:
        raise HTTPException(status_code=404, detail="No recipes found with the specified criteria")
    
    return {"output": output}

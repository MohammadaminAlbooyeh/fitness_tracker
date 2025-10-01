from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class FoodBase(BaseModel):
    name: str
    brand: Optional[str] = None
    serving_size: float
    serving_unit: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    sodium: Optional[float] = None

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int
    user_created: bool
    user_id: Optional[int]

    class Config:
        orm_mode = True

class MealItemBase(BaseModel):
    food_id: int
    servings: float

class MealItemCreate(MealItemBase):
    pass

class MealItem(MealItemBase):
    id: int
    meal_id: int
    food: Food

    class Config:
        orm_mode = True

class MealBase(BaseModel):
    name: str
    notes: Optional[str] = None

class MealCreate(MealBase):
    items: List[MealItemCreate]

class Meal(MealBase):
    id: int
    user_id: int
    date: datetime
    items: List[MealItem]

    class Config:
        orm_mode = True

class PlannedMealBase(BaseModel):
    day_of_week: int
    meal_type: str
    foods: List[dict]
    notes: Optional[str] = None

class PlannedMealCreate(PlannedMealBase):
    pass

class PlannedMeal(PlannedMealBase):
    id: int
    meal_plan_id: int

    class Config:
        orm_mode = True

class MealPlanBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    daily_calories: int
    macros: dict
    notes: Optional[str] = None

class MealPlanCreate(MealPlanBase):
    planned_meals: List[PlannedMealCreate]

class MealPlan(MealPlanBase):
    id: int
    user_id: int
    planned_meals: List[PlannedMeal]

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    description: str
    ingredients: List[dict]
    instructions: List[str]
    prep_time: int
    cook_time: int
    servings: int
    image_url: Optional[str] = None
    tags: List[str]
    nutrition: dict

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
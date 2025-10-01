from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, nullable=True)
    serving_size = Column(Float)
    serving_unit = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)
    sodium = Column(Float)
    user_created = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    user = relationship("User", back_populates="created_foods")
    meal_items = relationship("MealItem", back_populates="food")

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)  # breakfast, lunch, dinner, snack
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    user = relationship("User", back_populates="meals")
    items = relationship("MealItem", back_populates="meal")

class MealItem(Base):
    __tablename__ = "meal_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    servings = Column(Float)
    
    meal = relationship("Meal", back_populates="items")
    food = relationship("Food", back_populates="meal_items")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    daily_calories = Column(Integer)
    macros = Column(JSON)  # {"protein": 30, "carbs": 40, "fat": 30}
    notes = Column(String, nullable=True)
    
    user = relationship("User", back_populates="meal_plans")
    planned_meals = relationship("PlannedMeal", back_populates="meal_plan")

class PlannedMeal(Base):
    __tablename__ = "planned_meals"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"))
    day_of_week = Column(Integer)  # 0-6 for Monday-Sunday
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    foods = Column(JSON)  # [{"food_id": 1, "servings": 2}, ...]
    notes = Column(String, nullable=True)
    
    meal_plan = relationship("MealPlan", back_populates="planned_meals")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(String)
    ingredients = Column(JSON)  # [{"food_id": 1, "amount": 100, "unit": "g"}, ...]
    instructions = Column(JSON)  # ["Step 1...", "Step 2...", ...]
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    servings = Column(Integer)
    image_url = Column(String, nullable=True)
    tags = Column(JSON)  # ["healthy", "quick", "vegetarian", ...]
    nutrition = Column(JSON)  # Calculated nutrition facts per serving
    
    user = relationship("User", back_populates="recipes")
from fastapi import FastAPI

app = FastAPI(title="My Backend API")

# 1. Root Endpoint
@app.get("/")
def root():
    return {"message": "Hello from CIT Backend Course!"}

# 2. Path Parameter Endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}

# 3. Query Parameter Endpoint
@app.get("/items")
def list_items(limit: int = 10, category: str = "all"):
    return {"limit": limit, "category": category, "items": []}

# --- Exercise 1: Welcome Endpoint ---
@app.get("/welcome/{name}")  # Specifies the GET endpoint path with a string variable [cite: 103]
def welcome(name: str):
    return {"message": f"Welcome, {name}!"}  # Returns the formatted greeting [cite: 104]
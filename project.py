from typing import Optional, List, Literal
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# ⚠️ TODO: Change this to your actual Student Admission Number!
STUDENT_ID = "C027-01-2213/2023"

# Initialize FastAPI with your project information and student ID for grading
app = FastAPI(
    title=f"GigHub Nairobi Freelance Gigs API - {STUDENT_ID}",
    description="A local platform matching Nairobi's top tech talent with clients.",
    version="1.0.0"
)

# In-memory database tracking active freelance gigs
gigs_db = [
    {
        "id": 1,
        "title": "React Native Mobile App",
        "description": "Build a prototype cross-platform delivery app for a local business.",
        "category": "Development",
        "budget": 45000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Kamau Njoroge"
    },
    {
        "id": 2,
        "title": "Fintech UI/UX Design",
        "description": "Design a high-fidelity dashboard for a SACCO automation system.",
        "category": "Design",
        "budget": 25000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Fatuma Ali"
    },
    {
        "id": 3,
        "title": "SEO Blog Writer",
        "description": "Write 5 high-quality tech articles regarding AI adoption in Africa.",
        "category": "Writing",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Smith"
    }
]

@app.get("/")
def root():
    return {"message": "Welcome to GigHub Nairobi Freelance Gigs API", "student_id": STUDENT_ID}

# --- Step 2: Pydantic Models for Data Validation ---
# --- Part 4: Pydantic Models with Explicit Constraints ---

class GigCreate(BaseModel):
    # Required fields with custom constraints
    title: str = Field(..., min_length=5, max_length=100, description="Title of the freelance gig")
    description: str = Field(..., min_length=15, max_length=1000, description="Detailed requirements")
    category: str = Field(..., min_length=3, max_length=30, description="e.g., Development, Design, Writing")
    budget: float = Field(..., gt=0, description="Budget must be a strictly positive number")
    client_name: str = Field(..., min_length=2, max_length=50, description="Client's full name")

class GigUpdate(BaseModel):
    # Optional budget field (must be positive if provided)
    budget: Optional[float] = Field(None, gt=0, description="Updated positive budget amount")
    
    # Strictest constraint: Must ONLY be one of these three exact strings
    status: Optional[Literal["Open", "In Progress", "Closed"]] = Field(
        None, 
        description="Current workflow state. Allowed values: Open, In Progress, Closed"
    )

# 1. Retrieve all freelance gigs with skip and limit pagination
@app.get("/gigs")
def get_gigs(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0, le=100)):
    return gigs_db[skip : skip + limit]

# 2. Search for gigs by title/description with optional category filtering (MUST BE ABOVE ID ROUTE!)
@app.get("/gigs/search")
def search_gigs(q: str, category: Optional[str] = None):
    results = []
    for gig in gigs_db:
        # Check if query matches title or description
        if q.lower() in gig["title"].lower() or q.lower() in gig["description"].lower():
            # Apply an additional filter if a category filter is selected
            if category:
                if category.lower() in gig["category"].lower():
                    results.append(gig)
            else:
                results.append(gig)
    return results

# 3. Retrieve a single gig by its unique ID path parameter
@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    raise HTTPException(status_code=404, detail="Freelance gig not found")

# --- Step 5: API Endpoints (Data Creation) ---

# 4. Add a new freelance gig to the platform with validation
@app.post("/gigs")
def create_gig(gig: GigCreate):
    # Check if a gig with the exact same title already exists (case-insensitive)
    for existing_gig in gigs_db:
        if existing_gig["title"].lower() == gig.title.lower():
            raise HTTPException(status_code=400, detail="A gig with this title already exists")
            
    # Generate a unique auto-incremented ID
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1
    
    # Create the dictionary entry matching our DB structural pattern
    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": gig.currency,
        "status": gig.status,
        "client_name": gig.client_name
    }
    
    # Append to our database list
    gigs_db.append(new_gig)
    return {"message": "Freelance gig posted successfully", "gig": new_gig}

# --- Step 6: API Endpoints (Data Modification) ---
# --- Updated Step 6: PUT Endpoint matching Part 4 Schemas ---

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            # Update budget if provided
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget
            # Update status if provided (validated automatically by Literal choices)
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status
                
            return {"message": "Freelance gig updated successfully", "gig": gigs_db[index]}
            
    raise HTTPException(status_code=404, detail="Freelance gig not found")


# 6. Delete a freelance gig from the system entirely
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    # Enumerate through the database list to monitor the positional index
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            # Pop the item out of the list at the current index position
            deleted_gig = gigs_db.pop(index)
            return {"message": "Freelance gig deleted successfully", "gig": deleted_gig}
            
    # Raise a 404 error if the gig ID is missing from the list
    raise HTTPException(status_code=404, detail="Freelance gig not found")
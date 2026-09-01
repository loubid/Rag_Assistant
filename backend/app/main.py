from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   
from app.api.routes.query import router as query_router


app = FastAPI(
    title="Harry Potter RAG API",
    description="RAG API for querying the Harry Potter books",
    version="1.0.0"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # لو عايز تحصر الأوريجينز، حط الدومين بتاع الفرونت اند هنا بدل *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Harry Potter RAG API is running"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Query
# --------------------------------------------------

app.include_router(
    query_router,
    prefix="/query",
    tags=["Query"]
)


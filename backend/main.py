from fastapi import FastAPI

app = FastAPI(title="Resume Scanner API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Scanner API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Resume Scanner"}
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, Chatbot Backend is running!"}

@app.post("/chat/")
async def chat_response(message: str):
    # Hier kannst du die Logik für den Chatbot einfügen
    response = f"Du hast gesagt: {message}"
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
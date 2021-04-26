import uvicorn

if __name__ == "__main__":
    test = 5
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
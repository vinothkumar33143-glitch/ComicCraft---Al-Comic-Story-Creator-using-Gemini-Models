"""Easy launcher for ComicCraft on Android/Pydroid/Termux."""
import os
import uvicorn

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    print("\nComicCraft is starting...")
    print(f"Open this on the same phone: http://127.0.0.1:{port}")
    print(f"If using another device on the same Wi-Fi, use your phone IP with :{port}.\n")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from sdk.codon_sdk import CodonSdk
from handlers.codon_handler import handle_codon
from utils.nlp_parser import parse_command
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
    }.get(user_id)

class CommandRequest(BaseModel):
    command: str
    user_id: str = "owner123"  # Default user ID

@app.post("/execute-command")
async def execute_command(request: CommandRequest):
    try:
        sdk = CodonSdk(get_user_secret)

        codon_data = parse_command(request.command)

        if codon_data["intent"] == "unknown":
            raise HTTPException(status_code=400, detail="Sorry, I didn't understand that command.")

        codon = sdk.create_codon(
            intent=codon_data["intent"],
            payload=codon_data["payload"],
            meta={},
            user_id=request.user_id
        )

        # Handle the codon asynchronously
        asyncio.create_task(handle_codon(codon, get_user_secret))

        return {
            "status": "success",
            "codon": codon,
            "message": "Command processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For testing purposes
@app.get("/")
async def read_root():
    return {"message": "Codon Command Processor is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
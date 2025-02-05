import os
import logging
import string
import subprocess
import signal
import atexit
from typing import Dict
import json
from http import HTTPStatus
import argparse

import uvicorn
from openai import OpenAI
from fastapi import FastAPI, Response

from agentorg.orchestrator.orchestrator import AgentOrg
from agentorg.orchestrator.NLU.api import nlu_openai, slotfilling_openai
from create import API_PORT
from agentorg.utils.model_config import MODEL

logger = logging.getLogger(__name__)
app = FastAPI()

process = None  # Global reference for the FastAPI subprocess

def terminate_subprocess():
    """Terminate the FastAPI subprocess."""
    global process
    if process and process.poll() is None:  # Check if process is running
        logger.info(f"Terminating FastAPI process with PID: {process.pid}")
        process.terminate()  # Send SIGTERM
        process.wait()  # Ensure it stops
        logger.info("FastAPI process terminated.")

# Register cleanup function to run on program exit
atexit.register(terminate_subprocess)

# Handle signals (e.g., Ctrl+C)
signal.signal(signal.SIGINT, lambda signum, frame: exit(0))
signal.signal(signal.SIGTERM, lambda signum, frame: exit(0))


def get_api_bot_response(args, history, user_text, parameters):
    data = {"text": user_text, 'chat_history': history, 'parameters': parameters}
    orchestrator = AgentOrg(config=os.path.join(args.input_dir, "taskgraph.json"))
    result = orchestrator.get_response(data)
    return result['answer'], result['parameters']


# NLU endpoints
@app.post("/nlu/predict")
def predict_nlu(data: dict, res: Response):
    logger.info(f"Received data: {data}")
    pred_intent = nlu_openai.predict(**data)
    logger.info(f"pred_intent: {pred_intent}")
    return {"intent": pred_intent}

@app.post("/slotfill/predict")
def predict_slot(data: dict, res: Response):
    logger.info(f"Received data: {data}")
    results = slotfilling_openai.predict(**data)
    logger.info(f"pred_slots: {results.slots}")
    return results.slots

# Evaluation endpoint
@app.post("/eval/chat")
def predict(data: Dict):
    history = data['history']
    params = data['parameters']
    user_text = history[-1]['content']
    answer, params = get_api_bot_response(args, history[:-1], user_text, params)
    return {"answer": answer, "parameters": params}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start FastAPI with custom config.")
    parser.add_argument('--input-dir', type=str, default="./examples/test")
    parser.add_argument('--model', type=str, default=MODEL["model_type_or_path"])
    parser.add_argument('--port', type=int, default=int(API_PORT), help="Port to run the FastAPI app")
    
    args = parser.parse_args()
    os.environ["DATA_DIR"] = args.input_dir
    MODEL["model_type_or_path"] = args.model

    #run server
    uvicorn.run(app, host="0.0.0.0", port=int(API_PORT))
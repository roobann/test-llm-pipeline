import json
import logging
import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

def init():
    global model, tokenizer
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model')
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)
        input_text = data['input_data']['input_string']
        
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {"response": response}
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"error": str(e)} 
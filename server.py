import os
from flask import Flask, request, jsonify
from token_usage_tracking.llm_functions import generate_summary
from token_usage_tracking.log_tokens_to_hana import init_db, log_tokens

app = Flask(__name__)

port = int(os.getenv("PORT", 5000))

@app.route('/generate', methods=['POST'])
def generate():
    """flask endpoint to generate summary of prompt"""
    body = request.get_json()
    prompt = body.get("prompt", "")
    
    model_name = "gpt-4o"

    summary, propmt_tokens, completion_tokens = generate_summary(prompt, model_name)

    log_tokens('generate_summarization_1', '/generate', model_name, propmt_tokens, completion_tokens)

    return jsonify({"generated_text": summary})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=port) 
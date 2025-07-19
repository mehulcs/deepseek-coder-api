from transformers import AutoTokenizer, AutoModelForCausalLM, snapshot_download
import runpod
import torch
import os

MODEL_ID = "deepseek-ai/deepseek-coder-6.7b-instruct"
LOCAL_MODEL_DIR = "/models/deepseek-coder-6.7b-instruct"

print("Starting model download...")
if not os.path.exists(LOCAL_MODEL_DIR):
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=LOCAL_MODEL_DIR,
        local_dir_use_symlinks=False,
        trust_remote_code=True
    )
print("Model downloaded")

tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_DIR, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    LOCAL_MODEL_DIR,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16
).cuda()

def generate_code(prompt: str) -> str:
    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**input_ids, max_length=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]

def handler(event):
    # Extract input data from the request
    input_data = event["input"]
    
    return {"result": generate_code(input_data['prompt'])}

runpod.serverless.start({"handler": handler})
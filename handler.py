from transformers import AutoTokenizer, AutoModelForCausalLM
import runpod
import torch

def generate_code(prompt: str) -> str:
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
    
    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**input_ids, max_length=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]

def handler(event):
    # Extract input data from the request
    input_data = event["input"]
    
    return {"result": generate_code(input_data['prompt'])}

runpod.serverless.start({"handler": handler})
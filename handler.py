from transformers import AutoTokenizer, AutoModelForCausalLM
import runpod
import torch
import os


def generate_code(prompt: str) -> str:
    cache_dir = "/runpod-volume/cache"
    os.makedirs(cache_dir, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(
        "deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True, torch_dtype=torch.bfloat16, cache_dir=cache_dir).cuda()

    input_ids = tokenizer(prompt, return_tensors="pt",
                          truncation=True, max_length=15000).to(model.device)
    output = model.generate(**input_ids, max_new_tokens=1024)
    return tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]


def handler(event):
    # Extract input data from the request
    input_data = event["input"]

    return {"result": generate_code(input_data['prompt'])}


runpod.serverless.start({"handler": handler})

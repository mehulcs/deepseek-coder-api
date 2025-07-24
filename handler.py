from transformers import AutoTokenizer, AutoModelForCausalLM
import runpod
import os


def generate_code(prompt: str) -> str:
    cache_dir = "/runpod-volume/cache"
    os.makedirs(cache_dir, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(
        "TheBloke/deepseek-coder-33B-instruct-GPTQ", cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/deepseek-coder-33B-instruct-GPTQ", device_map="auto", trust_remote_code=False, revision="main", cache_dir=cache_dir)

    input_ids = tokenizer(prompt, return_tensors='pt',
                          truncation=True, max_length=15000).input_ids.cuda()

    output = model.generate(inputs=input_ids, temperature=0.7,
                            do_sample=True, top_p=0.95, top_k=40, max_new_tokens=1024)

    return tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]


def handler(event):
    # Extract input data from the request
    input_data = event["input"]

    return {"result": generate_code(input_data['prompt'])}


runpod.serverless.start({"handler": handler})

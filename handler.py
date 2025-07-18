import runpod  # Required

def handler(event):
    # Extract input data from the request
    input_data = event["input"]
    
    # Process the input (replace this with your own code)
    # result = process_data(input_data)
    
    # Return the result in the expected format
    return {"result": input_data}

if __name__ == '__main__':
  runpod.serverless.start({"handler": handler})  # Required
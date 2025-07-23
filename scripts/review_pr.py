import os
import requests

# Get inputs
diff = os.environ.get("DIFF", "")
if not diff.strip():
    print("❌ No diff content provided.")
    exit(1)

# Build prompt
prompt = f"You are a senior software engineer reviewing a pull request. Below is the diff of the PR. Your task is to provide clear, constructive, and specific code review comments that could help the author improve the code. \n\n{diff}"

# Prepare API call
url = "https://api.runpod.ai/v2/x3oz7vmgh6c1k3/runsync"
headers = {
    "Authorization": f"Bearer {os.environ.get('RUNPOD_TOKEN')}",
    "Content-Type": "application/json"
}
payload = {"input": {"prompt": prompt}}

# Make request
try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print(data)
    comment = data.get("output", {}).get("result", "")

    if not comment:
        print("⚠️ No result found in response.")
        comment = "No meaningful review generated."

except Exception as e:
    print(f"❌ Error calling RunPod API: {e}")
    comment = f"Error generating review: {str(e)}"

# Output comment for next GitHub step
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"comment={comment}\n")

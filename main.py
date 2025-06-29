import requests
import time
import json

# Configuration
BASE_URL = "https://chat.qwen.ai"
CHAT_ID = "c2f7efe1-8c15-4537-b13b-fd021b94ed11"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjliY2VhNTAwLWY1Y2ItNDIxNi04NWIzLWY5OGNkNTgyZDc4ZSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzUwNjYwODczLCJleHAiOjE3NTM2OTgxMDF9.x8r_jKZBzayyqeY1RRvnRo1KUWBNmZB099Vg26_uvBk"

# Headers setup
headers = {
    "authorization": AUTH_TOKEN,
    "content-type": "application/json",
    "origin": BASE_URL,
    "referer": f"{BASE_URL}/c/{CHAT_ID}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-request-id": "c584f184-026c-4094-ab24-3b47debe3f7f"
}

# Request payload for video generation
payload = {
    "stream": False,
    "incremental_output": True,
    "chat_id": CHAT_ID,
    "chat_mode": "normal",
    "model": "qwen3-235b-a22b",
    "parent_id": None,
    "messages": [{
        "fid": "717a9e7d-dc23-431e-8723-7cc87ec60f86",
        "parentId": None,
        "childrenIds": ["f3da5f2c-51af-4f80-a3b9-efcce26e8f52"],
        "role": "user",
        "content": "A cat is batting a ball of yarn with its paws, and the ball is rolling on the ground.",
        "user_action": "recommendation",
        "files": [],
        "timestamp": 1751110272,
        "models": ["qwen3-235b-a22b"],
        "chat_type": "t2v",
        "feature_config": {
            "thinking_enabled": False,
            "output_schema": "phase"
        },
        "extra": {
            "meta": {
                "subChatType": "t2v"
            }
        },
        "sub_chat_type": "t2v",
        "parent_id": None
    }],
    "timestamp": 1751110275,
    "size": "16:9"
}

def log_debug(message):
    """Helper function for debug logging"""
    print(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def make_video_generation_request():
    """Make the initial video generation request"""
    url = f"{BASE_URL}/api/v2/chat/completions?chat_id={CHAT_ID}"
    
    log_debug(f"Making video generation request to: {url}")
    log_debug(f"Request payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_debug(f"Request failed: {str(e)}")
        return None

def poll_task_status(task_id, max_attempts=500, interval=5):
    """Poll the task status until completion or max attempts reached"""
    status_url = f"{BASE_URL}/api/v1/tasks/status/{task_id}"
    
    for attempt in range(1, max_attempts + 1):
        log_debug(f"Polling attempt {attempt}/{max_attempts} - Task ID: {task_id}")
        
        try:
            response = requests.get(status_url, headers=headers)
            response.raise_for_status()
            status_data = response.json()
            
            log_debug(f"Status response: {json.dumps(status_data, indent=2)}")
            
            # Check for completion
            if status_data.get('success') or status_data.get('task_status') in ['completed', 'success']:
                log_debug("Video generation completed successfully!")
                return status_data
            elif status_data.get('task_status') in ['failed', 'error']:
                log_debug(f"Video generation failed: {status_data.get('message', 'Unknown error')}")
                return None
            
            log_debug(f"Video generation in progress... (Status: {status_data.get('task_status')})")
            if attempt < max_attempts:
                time.sleep(interval)
                
        except requests.exceptions.RequestException as e:
            log_debug(f"Polling request failed: {str(e)}")
            time.sleep(interval)
    
    log_debug(f"Max polling attempts ({max_attempts}) reached without completion")
    return None

def main():
    # Step 1: Initiate video generation
    log_debug("Starting Qwen video generation process")
    init_response = make_video_generation_request()
    
    if not init_response:
        log_debug("Failed to initiate video generation")
        return
    
    log_debug(f"Initial response: {json.dumps(init_response, indent=2)}")
    
    # Step 2: Extract task ID
    try:
        task_id = init_response['data']['messages'][0]['extra']['wanx']['task_id']
        log_debug(f"Extracted task ID: {task_id}")
    except KeyError as e:
        log_debug(f"Failed to extract task ID: {str(e)}")
        return
    
    # Step 3: Poll for completion
    final_result = poll_task_status(task_id)
    
    if final_result:
        log_debug("Video generation result:")
        print(json.dumps(final_result, indent=2))
        
        # You can add video download logic here if there's a video_url in the response
        if 'video_url' in final_result.get('data', {}):
            video_url = final_result['data']['video_url']
            log_debug(f"Video available at: {video_url}")
    else:
        log_debug("Video generation did not complete successfully")

if __name__ == "__main__":
    main()

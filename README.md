# Qwen Video Generation API Client v1.0.0

A Python client for interacting with Qwen AI's video generation API. This tool allows you to generate videos from text descriptions using Qwen's powerful AI model.

## ⚠️ Disclaimer

This project is for **EDUCATIONAL PURPOSES ONLY**. By using this code, you agree to the following:

- This code is intended for learning and understanding API interactions with Qwen AI
- You will not use this code for any illegal activities
- You are responsible for following Qwen AI's terms of service and usage policies
- The author is not responsible for any misuse of this code

For any questions, concerns, or if you've found this project helpful, please contact me at: hello.kaiiddo@gmail.com

## 🚀 Features

- Text-to-video generation using Qwen AI's API
- Automatic task status polling
- Detailed debug logging
- Error handling and retry mechanisms

## 📋 Prerequisites

- Python 3.x
- `requests` library
- Valid Qwen AI authentication token

## 🔧 Configuration

Before using the script, you need to set up your configuration in `main.py`:

```python
BASE_URL = "https://chat.qwen.ai"
CHAT_ID = "your-chat-id"
AUTH_TOKEN = "your-auth-token"
```

## 🎯 How It Works

1. **Authentication**: The script uses a Bearer token for API authentication
2. **Video Generation Request**: 
   - Sends a POST request to Qwen AI with your text description
   - Supports customizable video parameters (e.g., aspect ratio)
3. **Task Monitoring**:
   - Automatically polls for task status
   - Provides real-time status updates
   - Handles completion and error states
4. **Result Handling**:
   - Returns video URL upon successful generation
   - Provides detailed error information if generation fails

## 📝 Usage Example

```python
# Example text prompt
payload = {
    "messages": [{
        "role": "user",
        "content": "A cat is batting a ball of yarn with its paws",
        "chat_type": "t2v",
    }],
    "size": "16:9"
}

# Run the video generation
main()
```

## 🔍 API Response Structure

Successful response example:
```json
{
    "success": true,
    "task_status": "completed",
    "data": {
        "video_url": "https://example.com/video.mp4"
    }
}
```

## ⚙️ Functions

### make_video_generation_request()
Initiates the video generation process by sending the request to Qwen AI.

### poll_task_status(task_id, max_attempts=500, interval=5)
Monitors the generation task status:
- `task_id`: The ID of the generation task
- `max_attempts`: Maximum number of polling attempts
- `interval`: Time between polling attempts in seconds

### log_debug(message)
Helper function for debug logging with timestamps.

## 🛠️ Error Handling

The script includes comprehensive error handling for:
- Network issues
- API errors
- Invalid responses
- Task failures

## 📈 Future Improvements

- Add async support for better performance
- Implement automatic token refresh
- Add support for batch processing
- Include video download functionality

## 📄 License

This project is for educational purposes. Please contact hello.kaiiddo@gmail.com for any questions about usage or licensing.

---

Remember: This is v1.0.0 of the project and is intended for educational purposes only. For any questions or concerns, please reach out to hello.kaiiddo@gmail.com

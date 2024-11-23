# Auto YouTube Poster Bot 🎥🤖
A Python-based bot that automates the process of generating and uploading videos to YouTube. This project uses Selenium for browser automation and various APIs for generating images, audio, and assembling them into videos.

## Features 🚀
Downloads images based on keywords using the Pixabay API.
Generates audio from text using the ElevenLabs Text-to-Speech API.
Combines images and audio into a video using moviepy.
Automates YouTube Studio video uploads with Selenium.

```diff 
- <h1>Important </h1>
Youtube has rate limits, so you have to add time.sleep() and set intervals between each loop or else add it as a cronjob.
```
### Installation 📦
Prerequisites
Python 3.10+
Google Chrome (latest version)
ChromeDriver (matching your Chrome version)
Download it here and ensure the path is correct in your project.
Steps to Install
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/auto-yt-poster.git
cd auto-yt-poster
Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows

pip install -r requirements.txt
```

Add your API keys in a .env file: Create a .env file in the project root directory with the following content:

.emv file
```
PIXABAY_API_KEY=KEY
TTS_API_KEY=KEY
```

Download ChromeDriver and configure the path:

Place the chromedriver file in your project folder (e.g., /path/to/auto-yt-poster/chromedriver).
Ensure it is executable:
bash

Usage 🛠️
First add cookies to config/cookies.json

Running the Bot
Update the configuration files (e.g., config/constants.py) with appropriate paths for saving images, audio, and videos.

Run the bot:
python main.py

### Websites used
https://pixabay.com/
https://elevenlabs.io/

### Contributing 🤝
Feel free to fork this repository and make improvements. Contributions are welcome!
Create a pull request or report issues under the Issues tab.

### License 📜
This project is licensed under the Apache License. See the LICENSE file for details.

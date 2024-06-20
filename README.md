# ⭐ DropCloud ⭐

DropCloud is a fast and efficient text pasting/uploading site that prioritizes user privacy. With no login requirements, DropCloud ensures that your personal information is never collected. Simply paste your text, upload it, and get a unique URL to access your content anytime.

## Features
- **Privacy-Focused**: No logins required, ensuring complete anonymity.
- **Permanent Storage**: Your pasted text is stored forever and accessible via a unique URL.
- **User-Friendly**: Intuitive interface for easy text pasting and retrieval.

## Detailed Instructions for Using the Website
Using DropCloud is straightforward. Follow these simple steps:

### Submitting Plain Text
1. Enter your text and click "Submit".
2. You will be redirected to a unique file ID associated with your text. Save this file ID to avoid losing your text.
3. To access your text again, visit the site and append `/{YOUR_ID}` to the URL.

### Password-Protected Submission
1. Enter your text and set a password of your choice.
2. Click "Submit".
3. You will be redirected to a unique file ID. Access to the text requires entering the password you set.
4. To retrieve the text later, visit the site and append `/{YOUR_ID}` to the URL. You will be prompted to enter the password.

### Accessing Raw Text
1. For raw text files, use `/{YOUR_ID}/raw`.
2. If the file is password protected and you need raw access, use `/{YOUR_ID}/raw?password={YOUR_PASSWORD}`.

### Submitting Plain Text
1. Paste your text into the provided text area.
2. Click the "Upload" button.
3. You will be redirected to a unique URL containing your pasted text. Save this URL to access your text later.

### Accessing Your Text
1. Visit the unique URL provided after submission.
2. Your text will be displayed on this page.

## Self-Hosting
DropCloud is open-source, allowing you to host it yourself.

### Requirements
- Python
- Flask (install using `pip install flask`)

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dropcloud.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dropcloud
    ```
3. Install the required dependencies:
    ```bash
    pip install flask
    ```
4. Run the application:
    ```bash
    python app.py
    ```
5. Open your browser and go to the URL provided in the terminal to access your local DropCloud instance.

### Important Note
We do not recommend making your self-hosted DropCloud instance public as it could be a target for hacking, DDoS attacks, or information theft.

### API

The API is also very easy to use.

#### Get Raw Text From ID (No Password)
```python
import requests

# URL of the website displaying raw text
url = 'https://direct-jania-dropcloud-aaabff56.koyeb.app/{YOUR_ID}/raw'  # Replace with the actual URL of your paste file

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the text content of the response
    print(response.text)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
```
This example will go to your paste and take the raw text if you need to get text from a paste then you will have to use raw unless you want to use a web scraper which is just unnecessary.

## Disclaimer
-We are not responsible for any data loss resulting from guessed passwords, losing your text file ID, or any other circumstances. We will neither view, steal, nor delete your files. They are permanent unless removal is necessary, such as in the case of a malicious file link.
- **Privacy**: We do not collect or view your pastes. However, these pastes can be viewed by anyone with the unique URL. Do not paste private information unless you use a strong password.
- **Credit**: If you host DropCloud publicly, you must credit the original GitHub repository. You don't need to keep the GitHub button, but a link to the GitHub profile is required somewhere on your site.

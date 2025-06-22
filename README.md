# EH_Downloader
This is a web-based application that lets you automatically download all images from an E-Hentai gallery using Streamlit as the UI and Selenium for browser automation.
---
## 🧰 Features
🔍 Automatically detects page count from the gallery.

📥 Download all gallery images with a single click.

📁 Images are saved to a local folder with a custom name.

✅ Robust download with retry logic for failed attempts.
---

## 🚀 How to Run
### 1. Requirements
Install the necessary packages:

```
pip install streamlit selenium requests
```
⚠️ You also need ChromeDriver installed and matching your local Google Chrome version.

### 2. Launch the app
```
streamlit run app.py
```
### 3. Use it in your browser
- Enter the E-Hentai gallery URL.

- (Optional) Click Check Page to preview the number of pages.

- Click Download and the app will automatically extract page count and begin downloading.

## 📂 Folder Structure
Downloaded images will be saved into:

```
downloads/<your_custom_folder_name>
```
## 🛠 Additional Notes
- The app runs in headless mode (no browser window).

- If page extraction fails, make sure the gallery URL is valid and accessible.


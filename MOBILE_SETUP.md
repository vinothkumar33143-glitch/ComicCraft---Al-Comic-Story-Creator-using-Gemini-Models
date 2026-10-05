# ComicCraft — Mobile Setup

This version is prepared for running on an Android phone with **Termux** or **Pydroid 3**.

## 1. Extract the ZIP

Extract `ComicCraft-FINAL-MOBILE.zip` and open the `ComicCraft` folder.

## 2. Install Python

Use Termux or Pydroid 3. Make sure Python 3.11+ is available.

## 3. Open the project folder

In Termux, change directory into the extracted `ComicCraft` folder.

## 4. Install packages

```bash
python -m pip install -r requirements.txt
```

## 5. Start ComicCraft

```bash
python run_mobile.py
```

Or, in Termux:

```bash
bash run_mobile.sh
```

## 6. Open it on the phone

Open Chrome and visit:

```text
http://127.0.0.1:8000
```

The app starts in **mock + placeholder mode**, so you can test the complete project without a Gemini API key or a large Stable Diffusion download.

## 7. Test the project

Enter a story, character, setting, tone and art style, then tap **Create My Comic**.

You should get five panels and a PDF export button.

## Optional: real Gemini AI

Create a `.env` file from `.env.example` and set:

```env
AI_MODE=gemini
GEMINI_API_KEY=YOUR_KEY_HERE
```

Keep the key private. Do not upload `.env` publicly.

## Important for phones

Do **not** install `requirements-ai-images.txt` unless you specifically want to experiment with local Stable Diffusion. It is very large and normally unsuitable for a phone. Keep:

```env
IMAGE_PROVIDER=placeholder
```

for the mobile demo.

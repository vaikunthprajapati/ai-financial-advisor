<img src="banner.png" width="100%">

# 💰 AI Financial Advisor

An intelligent financial planning system powered by Google Gemini 2.0 Flash.

## Features
- Personalized advice for Students, Professionals & Retirees
- Expense breakdown with visual charts
- Goal tracking and timeline estimation
- Interactive AI chat for financial questions

## Tech Stack
- Python, Streamlit, Google Gemini 2.0 Flash, Plotly, Pandas

## How to Run
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Gemini API key to `.env` file
4. Run: `streamlit run app.py`
```
3. Save it

---

## 🧪 PHASE 5: Test Your App

---

### Step 15 — Run the App
In the VS Code terminal (make sure `(venv)` is showing), type:
```
streamlit run app.py
```
Your browser will automatically open with the app running at `http://localhost:8501`

---

### Step 16 — Test Everything
Go through this checklist:

| Test | What to do |
|---|---|
| ✅ Fill in your profile | Enter name, income, expenses in the sidebar |
| ✅ Check the dashboard | See your metrics and pie chart update |
| ✅ Click "Get My Personalized Advice" | AI should respond with advice |
| ✅ Set a goal amount | Check the progress bar |
| ✅ Ask a question in the chat | AI should answer |

If everything works — **your app is ready!** 🎉

---

## 📤 PHASE 6: Upload to GitHub

---

### Step 17 — Create a .gitignore File
1. Create a new file called `.gitignore`
2. Paste this inside:
```
venv/
.env
__pycache__/
*.pyc
```
3. Save it — this prevents your secret API key from being uploaded

---

### Step 18 — Create GitHub Repository
1. Go to **https://github.com** and log in
2. Click the **+** icon (top right) → **New Repository**
3. Name it: `ai-financial-advisor`
4. Set it to **Public**
5. Do NOT check any checkboxes
6. Click **Create Repository**
7. **Copy the repository URL** shown on the page (looks like `https://github.com/yourusername/ai-financial-advisor.git`)

---

### Step 19 — Upload Your Code to GitHub
In your VS Code terminal, run these commands **one by one**:
```
git init
```
```
git add .
```
```
git commit -m "Initial commit - AI Financial Advisor"
```
```
git branch -M main
```
```
git remote add origin https://github.com/YOUR_USERNAME/ai-financial-advisor.git
```
*(Replace YOUR_USERNAME with your actual GitHub username)*
```
git push -u origin main

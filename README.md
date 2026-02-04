# VTU Internship Diary Automation

This project automates the process of filling the **VTU Internship Diary** for the **current day** using browser automation and an LLM to generate learning outcomes.

Instead of manually logging into the VTU portal every day and writing repetitive entries, this script lets you:
- Write what you did at work
- Automatically generate learning outcomes using an LLM
- Auto-fill all required fields on the VTU Internship Diary page

---
## Prerequisite
- You must have an account on the vtu portal.
- Your company must be registered on the VTU portal.
- You must either have a Gemini API key (It is Free on Google AI Studio) or OpenAI API key (Paid)
- python version 3.10 or above
- Use uv or pip package manager
- You must not be a snitch

## Important Notes
- **The diary is only filled for the current day**
- The date picker always selects **Today**
- Past or future dates are not supported by design
- Company name must be exactly the same as on the vtu portal
- The List of skills must also be present on the portal. Don't make up your own skills.
- If you are using OpenAI API Key then run the test.py file after filling in the env variables.
- If you are using Gemini API Key then run the test2.py file after filling in the env variables.
- Use the command `pip install -r requirements.txt` to install all the packages
- You must enter all your details in the `.env` file whose format is given below.

## How the Diary Is Filled (Step-by-Step)

### 1) User writes daily work in Notepad  
- When the script starts, **Notepad opens automatically**.
- You write what you worked on for the day in plain text.
- Example:
```
Worked on debugging a data preprocessing pipeline, optimized SQL queries,
and experimented with a basic machine learning model for predictions.
```
- Once you close Notepad, the script reads this text and treats it as the **work description**.

---

### 2) Learning outcomes are generated using an LLM  
- The written work description is sent to an LLM using **DSPy**.
- Supported models:
- **Gemini Flash** (`gemini-2.5-flash`) – free API key
- **GPT-4o-mini** – paid API key (can be swapped in DSPy config to any other model)
- The model converts your work into a **first-person learning outcome** starting with: 'I Learned...'
- Example generated output:
```
I learned how to debug data pipelines more effectively, optimize database
queries for performance, and apply basic machine learning concepts to real
datasets.
```

---

### 3) VTU Internship Diary is auto-filled  
Using **Playwright**, the script:

- Logs into the VTU portal
- Navigates to **Internship Diary**
- Selects your internship company
- Automatically picks **today’s date**
- Fills the following fields:
- **Work Description** → Text you wrote in Notepad
- **Learning Outcomes** → LLM-generated reflection
- **Hours Worked** → From `.env`
- **Skills** → From `.env`

Finally, the diary entry is saved.

---

## Environment Setup

Create a `.env` file and fill in the following values:

```env
VTU_WEBSITE=https://vtu.internyet.in/sign-in
VTU_EMAIL=justinbeiber@gmail.com
VTU_PASSWORD=
INTERNSHIP_COMPANY="Diddy's Software Technologies"
HOURS_WORKED=10
SKILLS='["Python", "Intelligent Machines", "Data modeling", "Database design", "Machine learning"]'
OPENAI_API_KEY=
GEMINI_API_KEY=
```

---

## Tech Stack Used

- **Python**
- **Playwright** – browser automation
- **DSPy** – LLM orchestration
- **Gemini / OpenAI APIs** – learning outcome generation
- **dotenv** – environment variable management

import re
from playwright.sync_api import Playwright, sync_playwright, expect
import dspy
from dotenv import load_dotenv
import re
import os
from datetime import date
import tempfile
import os
import subprocess

# User input will be taken from notepad
def read_from_editor():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        path = f.name

    subprocess.run(["notepad.exe", path])
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    os.remove(path)
    return text

load_dotenv()

dspy.configure(
    lm=dspy.LM(
        model="openai/gpt-4o-mini",
        temperature=0.0,
        cache=False
    )
)

class LearningOutcomesSignature(dspy.Signature):
    """
    Role: Workplace Learning Reflection Agent

    Task: Given a paragraph that describes work activities, infer and summarize
    the learning outcomes in first-person point of view. The Paragraph must start with
    'I learned'
    """

    work_activities: str = dspy.InputField(
        desc="Things I did during work"
    )

    reflection: str = dspy.OutputField(
        desc="Short first-person paragraph describing what I learned on the job"
    )

class LearningOutcomesAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot = dspy.Predict(LearningOutcomesSignature)

    def forward(self, work_activities: list[str]):
        result = self.cot(work_activities=work_activities)

        # Only return the final reflection, not the reasoning
        return {
            "reflection": result.reflection
        }

def run(playwright: Playwright, learning_outcome: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://vtu.internyet.in/sign-in")
    page.get_by_role("textbox", name="Enter your email address").click()
    page.get_by_role("textbox", name="Enter your email address").fill(os.environ["VTU_EMAIL"])
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(os.environ['VTU_PASSWORD'])
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("button", name="I Understand").click()
    page.get_by_role("link", name="Internship Diary", exact=True).click()
    page.get_by_role("combobox", name="Select Internship *").click()
    page.get_by_label("Virtual Origami Technologies").get_by_text("Virtual Origami Technologies").click()
    page.get_by_role("button", name="Pick a Date").click()
    page.get_by_role("button", name="Today").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="Briefly describe the work you").click()
    page.get_by_role("textbox", name="Briefly describe the work you").fill(work_description)
    page.get_by_placeholder("e.g.").click()
    page.get_by_placeholder("e.g.").fill("10")
    page.get_by_role("textbox", name="What did you learn or ship").click()
    page.get_by_role("textbox", name="What did you learn or ship").fill(learning_outcome)
    page.locator(".react-select__input-container").click()
    page.locator("#react-select-2-input").fill("pyth")
    page.get_by_role("option", name="Python").click()
    page.locator("#react-select-2-input").fill("intell")
    page.get_by_role("option", name="Intelligent Machines").click()
    page.locator("#react-select-2-input").fill("data")
    page.get_by_role("option", name="Data modeling").click()
    page.locator("#react-select-2-input").fill("data")
    page.get_by_role("option", name="Database design").click()
    page.locator("#react-select-2-input").fill("machine")
    page.get_by_role("option", name="Machine learning").click()
    page.get_by_role("button", name="Save").click()

    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    agent = LearningOutcomesAgent()

    try:
        work_description = read_from_editor()
        agent_output: dspy.Prediction = agent(work_activities=work_description)
        print("Agent Output:")
        print(agent_output['reflection'])

        with sync_playwright() as playwright:
            run(playwright=playwright, learning_outcome=agent_output['reflection'])

        print("Successfully filled the internship diary...")

    except Exception as e:
        print(e)
        print(f"Failed to fill the internship diary for {date.today()}...")


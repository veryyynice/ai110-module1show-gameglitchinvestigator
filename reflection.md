# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Looked fine, very simple number guessing game.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
Hints were backwords, wrong. My score ended up being negative. It let me guess 111, out of bounds. New game button didn't work. Secret keeps changing. Diffulties don't make any sense. 
---
FIX: Refactored logic into logic_utils.py using Copilot Agent mode
## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Code, Copilot 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Verified the diffulty swaps by testing it manually and finding it in code. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). AI didn't improve the difficulties that well. It didn't change the amount of tries. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

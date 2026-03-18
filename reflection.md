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

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). 
AI didn't improve the difficulties that well. It didn't change the amount of tries. 
COnfused itself saying the wrong hints were cause by str int missmatch. 


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Searched the repository for other instances of that bug or variables. checked the code logic manually. 
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
had pytest tests running through GitHub Actions.
 One test checked that when your guess is too high, the hint says "LOWER" — it failed because the messages were literally swapped in the code. That was actually useful because I could see exactly what string came back vs what was expected. Another test caught that even-numbered guesses were giving the player +5 points instead of deducting, which I wouldn't have caught just by playing the game casually.

- Did AI help you design or understand any tests? How?
Claude helped write the initial test file and explained why each test was structured the way it was. 
t understood what edge cases to hit like boundary guesses (one above/below the secret) and the string vs int comparison bug. 
I verified they made sense by reading through them and cross-referencing with the actual bugs in the code.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Streamlit reruns the entire Python file every  time you interact with anything — clicking a button, kind of like React. The original code had random.randint() being called without checking if a secret already existed, so a new number got picked every rerun. 
Also the New Game button was hardcoded to use random.randint(1, 100)regardless of difficulty.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Think of it like refreshing a webpage every time you click something. Kind of like updates in React Session state is basically a backpack that persists between those refreshes. 
If you put your secret number in the backpack, it survives reruns. If you leave it as a regular variable, it gets recreated every time.

- What change did you make that finally gave the game a stable secret number?
The fix was wrapping the secret generation in a check: if "secret" not in st.session_state. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

the whole process- gathering a list of bugs, trying to fix with inline code changes. making tests. veryfying against tests. Or the same but making the tests before fixing. 

- What is one thing you would do differently next time you work with AI on a coding task?
I'd push back on AI explanations more and not just accept the first answer. Claude initially blamed the backwards hints on the int vs string comparison bug, which was a separate issue 
— the hints were wrong just because someone wrote the wrong string. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI generated code looks totally fine on the surface but can have some pretty dumb logical bugs baked in — things that a human would probably catch just from reading it once. You really do have to treat it like code review, not just assume it works because it ran without errors.
# Wordle Nodal Solver

This repository contains a **Python implementation of a Wordle solver** that uses *nodal analysis* of letter frequencies and co-occurrence to optimize guesses. Developed using ChatGPT, in order to explore its code creation and debugging capabilities.

Unlike brute-force or purely frequency-based solvers, this approach:
- Models how letters are likely to appear together  
- Balances **information gain** (broad coverage early) with **solution targeting** (narrowing once constraints are known)  
- Supports testing different **starting words** to measure their impact on solving efficiency  

---

## Features
- **Nodal Analysis Scoring**  
  Words are scored using:  
  - Letter frequency by position  
  - Co-occurrence of letters in valid solutions  
  - Penalties for repeated letters to encourage diversity early on  

- **Customizable Strategy**  
  - Optional exploratory probe words when too few letters are known  
  - Easy to extend with entropy-style scoring  

---

## Example Results
On the official Wordle solution set (~2,143 words):

- Starting with **SAUCE**:  
  - Average guesses: ~3.7  
  - Worst-case: 8 guesses  

- Starting with **CRANE** or **SOARE** improves the average to ~3.4–3.5 and avoids worst-case >6.  

---

## How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/wordle-nodal-solver.git
   cd wordle-nodal-solver
   ```

2. Ensure you have Python 3.8+ installed.

3. Run the solver on the full Wordle solution list:
   ```bash
   python wordle_solver.py
   ```

4. (Optional) To test different opening words:
   ```bash
   python wordle_solver.py --opening crane
   ```

## Files

- [**wordle_solver.py**](https://github.com/PCexec25/Wordle-Nodal-Solver/blob/main/wordle_solver.py) – Main solver implementation  
- [**wordle_solutions_cached.txt**](https://github.com/PCexec25/Wordle-Nodal-Solver/blob/main/wordle_solutions_cached.txt) – Canonical list of Wordle solutions (must be provided separately)  
- [**README.md**](https://github.com/PCexec25/Wordle-Nodal-Solver/blob/main/README.md) – This file  

---

## Why This Project?
This project demonstrates:
- **Algorithm design**: combining statistical analysis with constraint satisfaction
- **Software engineering**: clean, modular Python code suitable for reuse and extension
- **Data analysis**: measuring performance across large simulation sets to guide improvements

I use this project on my résumé as an example of applying analytical and coding skills to a playful but non-trivial problem.  

---

## License
MIT License. Free to use, modify, and share.  

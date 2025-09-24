#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wordle Nodal Analyzer
--------------------
Interactive solver and nodal analysis tool for Wordle.
Uses official Wordle solution list cached in 'wordle_solutions_cached.txt'
"""

import sys
import os
import datetime
import textwrap
from collections import Counter, defaultdict

# --------------------------------------------------------------------
# Load and filter solutions
# --------------------------------------------------------------------
def load_solutions(filename="wordle_solutions_cached.txt"):
    if not os.path.exists(filename):
        print(f"[fatal] solution file '{filename}' not found.")
        sys.exit(1)

    all_solutions = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            all_solutions.append(line)
    today = datetime.date.today()
    solutions = []
    for line in all_solutions:
        try:
            d_str, w = line.split(" ", 1)
            d = datetime.date.fromisoformat(d_str)
            if d >= today:
                solutions.append(w.lower())
        except ValueError:
            print(f"[warn] skipping malformed line: {line}")
    return solutions

# --------------------------------------------------------------------
# Candidate filtering
# --------------------------------------------------------------------
def filter_candidates(solutions, history):
    candidates = solutions.copy()
    for guess, fb in history:
        new_candidates = []
        for w in candidates:
            match = True
            for i, ch in enumerate(fb):
                if ch == "G" and w[i] != guess[i]:
                    match = False
                    break
                elif ch == "Y":
                    if guess[i] not in w or w[i] == guess[i]:
                        match = False
                        break
                elif ch == "B" and guess[i] in w:
                    match = False
                    break
            if match:
                new_candidates.append(w)
        candidates = new_candidates
    return candidates

# --------------------------------------------------------------------
# Pretty-print helper
# --------------------------------------------------------------------
def pretty_print_candidates(candidates, limit=30):
    for i, w in enumerate(candidates[:limit], 1):
        print(f"{i}. {w}")
    if len(candidates) > limit:
        print(f"...and {len(candidates)-limit} more")

# --------------------------------------------------------------------
# Nodal analysis helpers
# --------------------------------------------------------------------
def recommend_next(candidates, history, all_solutions, top_n=10):
    # Simple frequency scoring
    letter_counts = Counter()
    cooccurrence = defaultdict(Counter)
    for w in candidates:
        for i, ch in enumerate(w):
            letter_counts[ch] += 1
            for j, ch2 in enumerate(w):
                if i != j:
                    cooccurrence[ch][ch2] += 1

    # score all possible guesses
    scored = []
    for w in all_solutions:
        score = sum(letter_counts[ch] for ch in set(w))
        scored.append((score, w))
    scored.sort(reverse=True)
    recs = [w for score, w in scored[:top_n]]
    return recs, letter_counts, cooccurrence

def nodal_report(letter, cooc, top_k=6):
    if letter not in cooc:
        return []
    return cooc[letter].most_common(top_k)

# --------------------------------------------------------------------
# Interactive loop
# --------------------------------------------------------------------
def interactive_solver(solutions):
    print("=== Wordle nodal-analyzer (interactive) ===")
    print("Feedback: 5 chars: G=green, Y=yellow, B=gray (or .). Example: BYGBB")
    print("Type 'quit' to exit.")

    history = []
    current_candidates = solutions.copy()
    step = 0
    next_guess = "sauce"

    while True:
        step += 1
        print(f"\nStep {step}: I recommend you guess -> {next_guess.upper()}")
        fb = input(f"Enter feedback for {next_guess.upper()} (G/Y/B): ").strip()
        if not fb:
            print("[info] empty input; please enter feedback like 'BYGBB'")
            step -= 1
            continue
        if fb.lower() in ('quit','q','exit'):
            print("Quitting.")
            return
        fb = fb.upper().replace(' ', '')
        if len(fb) != 5 or any(ch not in ('G','Y','B','.') for ch in fb):
            print("[error] invalid feedback. Use G/Y/B (or .). Try again.")
            step -= 1
            continue

        history.append((next_guess, fb))
        if fb == "GGGGG":
            print(f"\nSolved! Word is: {next_guess.upper()}")
            return

        current_candidates = filter_candidates(solutions, history)
        print(f"[info] {len(current_candidates)} candidate(s) remain.")
        pretty_print_candidates(current_candidates, limit=30)

        known_letters = set()
        for g, f in history:
            for ch, fc in zip(g, f):
                if fc in ('G','Y'):
                    known_letters.add(ch.lower())

        if len(known_letters) < 2:
            if "broil" in solutions:
                print("[strategy] Not enough confirmed letters yet — recommending exploratory probe: BROIL")
                next_guess = "broil"
                continue
            else:
                print("[strategy] Not enough confirmed letters yet — recommending high-info guess.")

        recs, letter_freq, cooc = recommend_next(current_candidates, history, solutions, top_n=10)
        if not recs:
            print("[error] No recommendations found — double-check feedback")
            pretty_print_candidates(current_candidates, limit=200)
            return

        print("\nTop recommendations (by nodal score):")
        for i,w in enumerate(recs,1):
            print(f"  {i}. {w}")

        if known_letters:
            print("\nNodal neighbors for known letters (top co-occurring letters):")
            for k in sorted(known_letters):
                neighbors = nodal_report(k, cooc, top_k=6)
                neigh_str = ", ".join(f"{a}({cnt})" for a,cnt in neighbors) if neighbors else "(no data)"
                print(f"  {k}: {neigh_str}")

        next_guess = recs[0]

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main():
    print(textwrap.dedent("""\
        Wordle Nodal Analyzer
        --------------------
        This tool uses the OFFICIAL Wordle solution list (downloaded first-run then cached).
        Source: cfreshman gist (canonical extraction of original Wordle answers).
    """))

    solutions = load_solutions()
    # sanity check
    solutions = [w for w in solutions if len(w)==5 and w.isalpha()]
    if not solutions:
        print("[fatal] no solutions available.")
        sys.exit(1)
    print(f"[info] using {len(solutions)} solution words for analysis.")

    try:
        interactive_solver(solutions)
    except KeyboardInterrupt:
        print("\nInterrupted. Bye.")
        sys.exit(0)

if __name__ == '__main__':
    main()

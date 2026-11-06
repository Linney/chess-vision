# Chess Vision — Project Roadmap

## Purpose and audience

This project is a portfolio piece to show a cortAIx UK hiring manager (Thales, Glasgow) that I can independently take a real-world sensor problem through to a working, trustworthy AI system. Every phase should be judged against what that audience values:

- **Trusted AI:** the system knows when it is uncertain, fails safely, and keeps a human in the loop rather than guessing.
- **Measurable success criteria**, defined before building and reported honestly afterwards, including shortfalls.
- **Evidence-based ML:** a classical baseline, a trained model, a held-out evaluation, and a justified choice between them.
- **Robustness** under real conditions (lighting, shadows, camera position, hands in frame).
- **Explainability:** outputs a reviewer can verify, not a black box.
- **Edge-friendly:** light enough to run in real time on an ordinary CPU.
- **Engineering discipline:** tests, CI, pinned dependencies, clear modules, readable commits, eventually Docker.
- **My differentiator:** 14 years in precision optics. Camera calibration, distortion, parallax and lighting should be handled visibly and expertly.

Rules that apply throughout:

- I design and test; AI implements to my spec; I review and can explain every line.
- Nothing from work (data, images, processes) ever goes in this repo.
- Prioritise evaluation and trustworthiness over UI polish or feature creep.

## Final deliverable (MVP)

A Python command-line tool: recorded video in, PGN out, plus a report of uncertain or flagged moves and optional debug visualisations. For example:

```
python -m chess_vision game.mp4 --white "Linney" --black "Opponent" -o game.pgn
```

Live processing, a phone app, a GUI and clock reading are out of scope and belong in a "future work" section of the README.

## Architecture principle

The chess logic, vision (geometry and occupancy), temporal processing and output are **separate modules**. None of them depends on where frames come from (a file today, a live stream or phone later). This keeps each part testable and makes later extensions possible.

## Core design decision

Don't classify piece types. The game starts from a known position, so for each square decide only **empty / white / black**. Compare settled positions to find which squares changed, then use python-chess to find the **single legal move** that explains the change. Legality handles captures, castling and en passant. Promotion defaults to a queen and is flagged. If zero moves or more than one move match, **flag it and ask; never guess.**

## Success criteria (set now, report against at the end)

Draft targets, to be refined once real footage exists:

- ≥ 95% of moves recorded correctly across at least 5 held-out test games in normal indoor lighting.
- 100% of moves the system can't match are flagged (no silent wrong moves).
- Processes 1080p/30 fps video faster than real time on a standard laptop CPU.
- Works from any camera recording 1080p video, mounted overhead; nothing is specific to my phone.

---

## Phase 0 — Project setup ✅ COMPLETE

Done: Windows, VS Code, Python 3.13 in `.venv`, Git with a noreply email, GitHub repo `Linney/chess-vision`, README and `.gitignore`, folders `src/`, `tests/`, `data/`. The edit → commit → push loop is practised.

Hardware decided: a desk-clamp vertical pole with a horizontal arm, and a Galaxy S25 on the 1× main lens at about 60–80 cm above the board. Record 16:9 1080p video with stabilisation off, exposure and focus locked in Pro Video mode, and shutter at 1/50 or 1/100 s to avoid mains flicker. Use ordinary room lighting with no fill light, and orient the phone so the short side of the frame faces the pole.

## Phase 1 — Chess logic, no camera ✅ COMPLETE

Done: `models.py` (Occupancy, Result, Outcome and Reason, with validation) and `matcher.py` (`move_finder`). 17 tests cover normal moves, captures, en passant, both castles, promotion, illegal moves and an unchanged board. Dependencies are pinned, and GitHub Actions runs pytest on every push. Design decisions 004–009 are in `docs/decisions.md`.

Showcase value: clean structured Python, a test suite, CI, and "fails safely" built in from the first line.

## Phase 2 — Board geometry (about 1–2 weeks)

Turn a still frame into a clean, top-down, square board image cut into 64 cells.

- **Camera calibration** using a printed checkerboard, to correct lens distortion. Document the method properly; this is my home ground.
- Pick corners manually first, then detect them automatically, then apply a homography (`getPerspectiveTransform` / `warpPerspective`).
- **Analyse parallax:** tall pieces lean radially outward from the image centre. Quantify it for my setup and plan to handle it in software (for example, sampling the part of each cell nearest the image centre).
- Produce debug output: the original frame with the detected grid overlaid, and the warped board.

Showcase value: sensor understanding that most AI candidates lack, and the most visual early result for the README.

## Phase 3 — Square occupancy: baseline vs ML (about 2–3 weeks)

The ML centre of the project. Decide empty / white / black for each cell, **two ways, and compare them**.

- **Build a dataset** from my own footage: labelled cell images, with a record of which videos and conditions they came from (data versioning).
- **Split properly:** hold out whole games for testing, never just random cells from the same games.
- **Classical baseline:** brightness, variance and edge measures against an empty-board reference.
- **Trained classifier:** a small model (scikit-learn first, possibly a small CNN in PyTorch), with data augmentation for lighting and shadow.
- **Track experiments with MLflow:** every run's settings and results.
- **Evaluate** each approach: accuracy, confusion matrix, per-condition breakdown, and processing time per frame on CPU.
- Every prediction outputs a **confidence score**.
- **Choose on evidence** and write up why.

Showcase value: the full ML workflow of baseline, dataset, training, honest evaluation and a justified decision. This is exactly what the AI Engineer adverts describe.

## Phase 4 — Video to moves (about 2 weeks)

Process the video over time.

- Detect motion (hands over the board), wait until the board has been **stable**, then capture that frame as the new position.
- Run each settled position through geometry, then occupancy, then move matching.
- Carry confidence through the whole pipeline: if the changed squares or the occupancy readings are uncertain, flag the move rather than commit it.
- Handle the real-world mess: hovering hands, knocked pieces, shadows, and the stand being bumped.

Showcase value: robustness and uncertainty handling in a real temporal system.

## Phase 5 — PGN output, recovery and explainability (about a week)

- Write the PGN with headers: players, event, date, result.
- **Human-in-the-loop recovery:** flagged moves are listed with a timestamp and reason (for example, "move 23: no legal match at 14:32"), and the user can confirm or correct them.
- **An explainability report per move:** which squares changed, their confidence scores, which legal moves were considered, and why one was chosen. Optionally, an annotated debug video.

Showcase value: "decision support for a human operator", the trusted-AI message in miniature.

## Phase 6 — Robustness testing, packaging and showcase

- Record test games under **deliberately varied conditions**: daytime and evening light, different heights, at least one session at the club, a different board or set if possible.
- **Measure against the success criteria**, with a per-condition breakdown. Report the shortfalls honestly.
- **Handle drift:** show what happens with an unseen board or unseen lighting, how confidence scores reveal it, and how new data plus retraining fixes it.
- Measure timing on CPU and state the edge-deployment implications.
- Add a **Dockerfile** so anyone can run the tool identically.
- **Write the README:** problem, approach, architecture diagram, demo GIF, results table, limitations, hardware requirements ("any camera recording 1080p video, mounted overhead"), and future work (live streaming to a laptop, a phone app, clock reading as a move-complete signal, multi-board club recording, live broadcast).
- Make the repo **public** when it is ready to share.

## Interview readiness (ongoing)

For every phase, be able to explain in plain language what I built, why I chose that approach, what alternatives I rejected, how I know it works, and where it fails. Keep a short running decisions log in the repo (`docs/decisions.md`) as I go.

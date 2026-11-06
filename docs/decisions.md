# Decisions log

## 001 — Creating Separate Dev and Runtime Requirements
**Date:**       2026-09-28
**Status:**     Accepted

**Context:**    Deciding which requirement should be pinned from pip freeze output

**Decision:**   To provide separate dev and runtime requirements using only direct dependencies

**Alternatives considered:**   
* **Option 1: Unified requirements.txt**
    * Simpler, but would force users to needlessly install pytest

* **Option 2: Pin full freeze output**
    * More precise but less portable as it includes OS specific dependencies - eg. colorama

**Consequences:** 
* Since pytest is only required for dev and not for runtime it can be omitted from runtime requirements.txt. 
* By including the entire runtime requirements in the dev requirements, each dependency name and version number is only listed once and can be more easily updated if necessary. 
* Versions may drift over time. If things start to break we could revisit requirements with pip-tools to provide full and direct requirements lists.


## 002 — Forward Matching Algorithm Design
**Date:**       2026-09-28
**Status:**     Accepted

**Context:**    Constrained by the fact we're only observing square occupancy rather than specific piece type.

**Decision:**   To calculate potential board occupancy after each legal move and compare against observed position.

**Alternatives considered:**   
* **Option 1: Identify what squares changed and look backwards at what move could have caused it**
    * Effectively reinventing the wheel when python-chess can already understand the rules of chess and list all legal moves.

**Consequences:** 
* By better utilising python-chess' built-in features we don't have to write special logic for edge-cases, eg, castling, en-passant etc.
* Exhaustively searching all legal moves sounds potentially wasteful but most positions are limited to a few dozen moves so the cost is negligible.
* All legal moves must be explored, not stopping at first match.
* Promotion moves will have to be flattened to assume queen promotion, and flagged as needing human review.
* With perfect data, promotion is the only move with ambiguity. With noisy data this will change and each move will have a confidence score.


## 003 — Custom dataclass for recording square occupancy
**Date:**       2026-09-28
**Status:**     Accepted

**Context:**    Trying to choose a data type that can effectively reflect what the camera observes and be compared against a predicted board

**Decision:**   Create a custom dataclass that holds one SquareSet of squares occupied by white pieces, and another SquareSet of squares occupied by black pieces. It will follow python-chess numbering (a1=0). Confidence levels will be held separately.

**Alternatives considered:**   
* **Option 1: 64 char string representing black pieces (B) / white pieces (W) / empty squares (.)**
    * + More human-readable in testing
    * + Cannot have an overlap, ie, one square occupied by both colours
    * - Ambiguous square order- does it start at a1, or a8 like in FEN?
    * - Has no protection against invalid values (anything that isn't B/W/.) or wrong length (anything that isn't exactly 64 chars) unlike SquareSet
    * - More work involved in converting an occupied board into this format

**Consequences:** 
* Custom dataclass of SquareSets is much easier to convert a board into, and for finding changed squares. We are at risk of white/black overlap but this can be validated in `__post_init__` before building a board.
* Postponed: aligning confidence with occupancy


## 004 — Expanded AI usage to reflect real-world development environments
**Date:**       2026-10-16
**Status:**     Accepted

**Context:**    AI coding tools are being rolled out to staff at my workplace; weighing the value of proving I can hand-write every line against shipping a working, well-understood product sooner.

**Decision:**   Expand AI usage to generating code adhering strictly to my specification. I retain all design decisions; implementation is delegated to AI. I write all of the tests myself to make sure any AI-generated code remains well understood and fit for purpose.

**Alternatives considered:**   
* **Option 1:** Continue writing code myself with the AI as a tutor.
    * + More impressive as a software developer
    * - Much slower development pace.
    * - Willfully ignoring a powerful tool that is widely available in real-world environments.

* **Option 2:** Allowing AI to generate all implementation and testing
    * + Much, much faster development
    * - Same source writing tests and code could fail to uncover misunderstandings
    * - Python fluency undeveloped
    * - Much less likely to understand the end result on a meaningful level

**Consequences:** 
* Coding/implementation is drastically accelerated as I will only be writing pseudocode and making decisions.
* Generated code will be reviewed line by line, and results will be predicted before running code.
* Increased risk of subtle bugs/edge cases causing problems so comprehensive code review will be required.
* Only code that is understood will be committed.
* Tests will still be written by me.
* Limited room for improving Python fluency.


## 005 — Occupancy uses plain square names
**Date:**       2026-10-30
**Status:**     Accepted (supersedes the earlier plan to use `chess.SquareSet`)

**Context:**    `Occupancy` is the hand-off between Phase 3 (vision) and Phase 1 (matching). It needs to say which squares hold a white piece and which hold a black piece.

**Decision:**   `Occupancy` holds two frozensets of square names such as `'e4'`. `__post_init__` converts any collection of names into frozensets, then raises `ValueError` for an invalid square name or a square listed in both colours. Plausibility checks (more than 16 pieces, a captured piece reappearing) are deliberately not made here.

**Alternatives considered:**
* **Option 1:** `chess.SquareSet`
    * + Compares directly with python-chess boards
    * - Phase 3's vision code would depend on a chess library just to report colours
    * - Harder to read in tests and debug output
* **Option 2:** Validate plausibility (at most 16 pieces per colour) in `__post_init__`
    * + Catches impossible boards early
    * - A camera misread would crash the pipeline instead of producing a flagged move
    * - Unnecessary: no legal move explains an impossible board, so the matcher already returns NO_MATCH

**Consequences:**
* Conversion between square names and python-chess squares happens in one place, inside the matcher.
* Errors that can only come from bugs raise immediately; errors that can come from the camera flow through to a flagged move for a human.
* `models.py` still imports python-chess, because `Result` holds `chess.Move`. The separation is in what the vision code has to reason about, not in the imports.


## 006 — Matcher interface: Board in, Result out
**Date:**       2026-10-30
**Status:**     Accepted

**Context:**    Every test uses the matcher's inputs and outputs now, and Phases 4 and 5 will build on them later.

**Decision:**   `move_finder(board: chess.Board, occupancy: Occupancy) -> Result`. `Result` is a frozen dataclass with `outcome` (an `Outcome` enum), `moves` (always a tuple of `chess.Move`: empty, one, or several), `reason` (a `Reason` enum code, `NONE` when there is nothing to explain) and `confidence` (a float from 0.0 to 1.0). `__post_init__` enforces that the number of moves matches the outcome. Tests describe positions as FENs and build the `Board` themselves.

**Alternatives considered:**
* **Option 1:** Take a FEN string instead of a `Board`
    * + Tests slightly shorter
    * - Phase 4's game loop already holds a `Board`, forcing a Board → FEN → Board round trip on every move
* **Option 2:** Return moves as SAN or UCI strings
    * - SAN depends on the position (check marks, disambiguation), so comparisons are fragile
    * - Strings can't be pushed straight onto a board
* **Option 3:** Free-text reasons
    * + Quick to write
    * - Wording drifts, typos go unnoticed, and Phase 5 can't act on them reliably

**Consequences:**
* Phase 4 can push the returned move straight onto its board.
* Phase 5 turns reason codes into human-readable report lines, adding context the matcher doesn't have (move number, timestamp).
* Every field has one type whatever the outcome, so code reading a `Result` never has to check which form it got.


## 007 — The matcher is stateless; WAIT versus NO_MATCH
**Date:**       2026-10-30
**Status:**     Accepted

**Context:**    In real games, a settled frame can show an unchanged board, a capture in progress, a knocked-over piece or a misread square.

**Decision:**   The matcher only ever compares two settled states and knows nothing about time or motion. An unchanged board returns WAIT (`NO_CHANGE`). Anything not explained by exactly one legal move, including missing pieces, returns NO_MATCH (`NO_LEGAL_MATCH`). Motion detection, deciding when a board has settled, and timeouts all belong to Phase 4.

**Alternatives considered:**
* **Option 1:** Treat missing pieces as WAIT, since a capture may be in progress
    * + Fewer flagged moves in normal play
    * - The matcher can't tell a capture in progress from a knocked piece or a missed detection
    * - A persistent misread would stall the game silently, breaking the "no silent failures" criterion

**Consequences:**
* Failures are loud: a mid-capture frame becomes a flagged move for a human, never a silent stall or a wrong move.
* Phase 4 can later reduce these flags (for example, by waiting longer) without the matcher changing.


## 008 — Promotions are assumed to be queens
**Date:**       2026-10-30
**Status:**     Accepted

**Context:**    Occupancy can't distinguish piece types, so all four promotions produce identical occupancy. With perfect readings, this is the only way two legal moves can produce the same after-state.

**Decision:**   The matcher only considers queen promotions. A matched promotion returns reason `PROMOTION_ASSUMED_QUEEN`. Confidence is not reduced.

**Alternatives considered:**
* **Option 1:** Return AMBIGUOUS for every promotion
    * - Flags every promotion, even though queen promotions are the overwhelming majority
* **Option 2:** Lower the confidence (for example, to 25%)
    * - Mixes up two different things: uncertainty about the evidence, and information the sensor can never see
    * - A cleanly observed promotion would look less trustworthy than a shaky occupancy reading
* **Option 3:** Work out the promoted piece later from how it moves
    * Parked as future work. Often impossible: a queen moving along a file looks exactly like a rook.

**Consequences:**
* An under-promotion is recorded wrongly, but always visibly marked for human review.
* AMBIGUOUS can't occur in Phase 1. It is kept for Phase 3, when uncertain readings may fit several moves.


## 009 — Phase 1 implementation choices
**Date:**       2026-10-30
**Status:**     Accepted

**Decisions:**
* **Each candidate move is tried on a fresh `board.copy()`**, so the caller's board is never modified. Push/pop on the caller's board was rejected: anything exiting between a push and its pop would leave a phantom move behind. The cost of copying is negligible, because the matcher runs once per settled position, not once per frame.
* **Confidence is always 1.0 and isn't asserted in tests.** With perfect inputs it carries no information. Its meaning will be defined once Phase 3 produces real readings.
* **Tests assert individual `Result` fields** rather than comparing whole objects, so giving confidence a real value in Phase 3 won't break every test.
* **Tests write every after-occupancy by hand**, rather than generating it by pushing moves with python-chess, so the expected results don't come from the same library the matcher uses.
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
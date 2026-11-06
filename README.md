# Chess Vision

A camera watches an over-the-board chess game and outputs the PGN of that game. 
When playing a club game, players will often record the moves on paper as they are playing but after the game has ended they then need to re-enter the moves into a computer for in-depth analysis. This application aims to speed up this process by providing a digital text PGN automatically, ready to be used for computer analysis.
There is potential for further applications of this technology that would enable a chess club to record multiple games at once and even use the streams to broadcast the games live.

## Status

Phase 1 complete: a tested move-matching engine that finds the single legal move explaining a change in board occupancy, and flags the change when no move, or more than one, fits.

## Running the tests

```
pip install -r requirements-dev.txt
python -m pytest
```
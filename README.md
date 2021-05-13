# 442ChessProject

Most of this is explained in the project report.

The main program file is `ChessTime.py`, which needs to be run in two separate instances to connect to each other. The code currently has three built-in options for units to connect to, and also checks that it's running on one of those units itself. This sets the ip, wattage, and other variables automatically.

Currently it only runs on Chimera, since the CPU, BF1, and NGD are all built in, and their respective stockfish programs are referenced by the program. Stockfish is used as the engine for this program, but could be replaced by any other engine that uses a UCI. Stockfish is open source and licensed under GPL-v3, but none of the actual code is used in this repo.

I don't have the GPU code (attempt) in this repo, since it's non-functional modified Stockfish code.

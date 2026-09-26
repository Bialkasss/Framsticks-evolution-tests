@echo off
cd /d "%~dp0"
set "SIM_DIR=%~dp0"
python ..\FramsticksEvolution.py -path ..\.. -sim "%SIM_DIR%eval-allcriteria-mini.sim;%SIM_DIR%swimming-water.sim;%SIM_DIR%recording-body-coords.sim" -opt velocity -genformat 1 -popsize 50 -generations 200 -stagnation 50 -runs 4 -workers 4 -hof_savefile task7-f1-hof.gen -output_prefix task7-f1-parallel
pause

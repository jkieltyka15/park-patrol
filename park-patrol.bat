@echo off

:: define the location of main
set "game_dir=src"
set "game_file=__main__.py"
set "game_file_path=%game_dir%/%game_file%"

:: launch the game
python3 "%game_file_path%"
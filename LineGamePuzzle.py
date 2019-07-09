'''
LineGame Puzzle -- sk3p7ic -- 2019
-------------------------------------------------------------------------------

This game imports a .txt file to be used as a map. Within this map, the player
uses controls for going up/down/left/right in order to occupy all spaces in the
fewest number of moves. However, once a direction is set, the player cannot
change that direction until the player's on-screen character hits a boundary
wall. For more information, consult the provided README.md file.

Copyright (c) 2019, Joshua Ibrom (sk3p7ic)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from sys import platform as sys_platform # Stores the platform running the game
from os import system as sys_cmd # Used to run clear console
import sys, time # Used to exit and wait

class Game:
  '''Runs the game.'''
  # Main Game Variables
  GAME_MAP = [['#' for x in range(0, 12)] for x in range(0, 12)] # Map of game
  CURR_POS = (0, 0) # Position of the player stored as (y, x)
  MOVE_NUM = 0 # Stores the number of moves a player has made
  SPCS_REM = 0 # The number of spaces remaining
  PLAYER_CHAR = [['▒', '▒'], ['▒', '▒']] # The current character position
  USED_SPACES = [['▓', '▓'], ['▓', '▓']] # Spaces used by the player in past
  MAP_BOUNDRS = [['█', '█'], ['█', '█']] # The spaces taken by the map
  UNUSED_SPCE = [[' ', ' '], [' ', ' ']] # Empty space
  PLAYERSPEED = 0.000 # The speed at which the player will move, in seconds
  SYS_PLATFORM = None # Stores the platform the game is running on
  STDSCR = None # Stores the stdscr variable for curses, if being used

  def __init__(self, infile, platform, stdscr=None, start_position=(0,0)):
    '''Creates the map based off of input file and sets up game.'''
    # Import file map
    temp_map = [[char for char in line if char != '\n'] for line in infile]
    # Translate to proper game map
    for n, line in enumerate(temp_map):
      for m, char in enumerate(line):
        if char == '#':
          self.GAME_MAP[n][m] = self.MAP_BOUNDRS
        else:
          self.GAME_MAP[n][m] = self.UNUSED_SPCE
          self.SPCS_REM += 1
    # Set other variables
    self.CURR_POS = start_position
    self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1]] = self.PLAYER_CHAR
    if "win" in platform: self.SYS_PLATFORM = "win"
    else: self.SYS_PLATFORM = platform
    if self.SYS_PLATFORM != "win": self.STDSCR = stdscr # Get stdscr for *nix

  def colorize(self):
    '''Adds color to the game. Linux only.'''
    if self.SYS_PLATFORM != "win":
      curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Boundary
      curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Used
      curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Player

  def printMap(self):
    '''Prints the game map. Windows version.'''
    if self.SYS_PLATFORM == "win":
      def printer(args):
        '''Prints an array of args by pprinting top of arg, then bottom.'''
        # Iterate through top characters
        for arg in args:
          for char in arg[0]: # Selects top chars
            print(char * 2, end='') # Add more of char to prevent vert stretch
        print() # Newline
        # Iterate through bottom characters
        for arg in args:
          for char in arg[1]: # Selects bottom chars
            print(char * 2, end='')
        print()# Newline
    else:
      def printer(args):
        '''Prints the game map. *nix version.'''
        # Iterate through to characters
        for arg in args:
          for char in arg[0]: # Selects top characters
            if char == self.PLAYER_CHAR[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(3))
            if char == self.USED_SPACES[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(2))
            if char == self.MAP_BOUNDRS[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(1))
            if char == self.UNUSED_SPCE[0][0]:
              self.STDSCR.addstr(char * 2)
        self.STDSCR.addstr('\n') # Newline
        # Iterate through bottom characters
        for arg in args:
          for char in arg[1]: # Selects bottom characters
            if char == self.PLAYER_CHAR[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(3))
            if char == self.USED_SPACES[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(2))
            if char == self.MAP_BOUNDRS[0][0]:
              self.STDSCR.addstr(char * 2, curses.color_pair(1))
            if char == self.UNUSED_SPCE[0][0]:
              self.STDSCR.addstr(char * 2)
        self.STDSCR.addstr('\n') # Newline
        self.STDSCR.refresh()
    if self.SYS_PLATFORM == "win": sys_cmd("cls") # Clears the screen
    for line in self.GAME_MAP: printer(line) # Call the printer
    if self.SYS_PLATFORM == "win": # Print number of moves if on Windows
      print("\n[*] Moves: {moves}".format(moves=self.MOVE_NUM))
    else: # Add number of moves if using curses and reset to origin
      self.STDSCR.addstr("\n[*] Moves: {moves}".format(moves=self.MOVE_NUM))
      self.STDSCR.move(0, 0)

  def checkWin(self):
    '''Checks if there are any spaces remaining.'''
    return self.SPCS_REM == 0 # Return True if no spaces left

  def movePlayer(self, direction):
    '''Moves the player a specified direction.'''
    def collision_detect():
      '''Detects if collision occurs (boundary next character in sequence).'''
      if direction == 'u':
        next_char_type = self.GAME_MAP[self.CURR_POS[0] - 1][self.CURR_POS[1]]
      if direction == 'd':
        next_char_type = self.GAME_MAP[self.CURR_POS[0] + 1][self.CURR_POS[1]]
      if direction == 'l':
        next_char_type = self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1] - 1]
      if direction == 'r':
        next_char_type = self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1] + 1]
      if next_char_type == self.MAP_BOUNDRS:
        return True
      else:
        return False
    def update_map():
      '''Updates the game map and number of spaces remaining.'''
      # Update current player space
      self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1]] = self.PLAYER_CHAR
      # Update previous taken spaces
      if direction == 'u':
        self.GAME_MAP[self.CURR_POS[0]-1][self.CURR_POS[1]] = self.USED_SPACES
      if direction == 'd':
        self.GAME_MAP[self.CURR_POS[0]+1][self.CURR_POS[1]] = self.USED_SPACES
      if direction == 'l':
        self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1]-1] = self.USED_SPACES
      if direction == 'r':
        self.GAME_MAP[self.CURR_POS[0]][self.CURR_POS[1]+1] = self.USED_SPACES
      time.sleep(self.PLAYERSPEED)
      self.printMap()
      self.SPCS_REM = 0 # Reset spaces remaining for recount
      for y in range(0, len(self.GAME_MAP)):
        for x in range(0, len(self.GAME_MAP)):
          # Recount the number of spaces remaining
          if self.GAME_MAP[y][x] == self.UNUSED_SPCE: self.SPCS_REM += 1
    self.MOVE_NUM += 1 # Add another move to counter
    if direction == 'u':
      while not collision_detect():
        update_map()
        self.CURR_POS = (self.CURR_POS[0] - 1, self.CURR_POS[1])
    if direction == 'd':
      while not collision_detect():
        update_map()
        self.CURR_POS = (self.CURR_POS[0] + 1, self.CURR_POS[1])
    if direction == 'l':
      while not collision_detect():
        update_map()
        self.CURR_POS = (self.CURR_POS[0], self.CURR_POS[1] - 1)
    if direction == 'r':
      while not collision_detect():
        update_map()
        self.CURR_POS = (self.CURR_POS[0], self.CURR_POS[1] + 1)
    self.printMap()

  def gameloop(self, playerspeed=0.015):
    '''The main gameloop. Playerspeed is the speed at which a player's
    character will move.'''
    self.PLAYERSPEED = playerspeed
    self.printMap()
    while self.checkWin() == False: # Loop through game while no winner
      if self.SYS_PLATFORM == "win":
        if msvcrt.kbhit(): # If key is pressed
          key = ord(msvcrt.getch()) # Get the key
          if key == 119: game.movePlayer('u') # W
          if key == 97: game.movePlayer('l')  # A
          if key == 115: game.movePlayer('d') # S
          if key == 100: game.movePlayer('r') # D
          if key == 113 or key == 27: break
      else:
        key = self.STDSCR.getch() # Call getch and get -1 if no key pressed
        if key != -1: # If a key was pressed
          if key == 119: self.movePlayer('u') # W
          if key == 97: self.movePlayer('l')  # A
          if key == 115: self.movePlayer('d') # S
          if key == 100: self.movePlayer('r') # D
          if key == 113 or key == 27: break
    if self.checkWin(): print("\n\nWINNER!") # Display that player has won
    if self.SYS_PLATFORM != "win": # Allow player to see score if on *nix
      print("Press <ESC> or <q> to quit...")
      while True:
        key = self.STDSCR.getch()
        if key != -1 and key == 113 or key == 27: break

if "win" in sys_platform:
  def start():
    '''Starts the game. Windows version.'''
    infile = open("demo_map.txt", 'r') # File containing the map to be used
    game = Game(infile, sys_platform, (8, 8)) # Initialize game's components
    game.gameloop()
else:
  def start(stdscr):
    '''Starts the game. *nix version.'''
    stdscr.nodelay(1) # Don't wait to call getch
    curses.start_color() # Start the colors
    curses.use_default_colors()
    infile = open("demo_map.txt", 'r') # File containing the map to be used
    game = Game(infile, sys_platform, stdscr, (8, 8))
    game.colorize()
    game.gameloop()

if __name__ == "__main__":
  # Run start method depending on platform
  if "win" in sys_platform: # Windows
    import mscvrt # Used for getting keypresses in Windows
    start() # Start the game
  else: # *nix
    import curses # Used for getting keypresses
    curses.wrapper(start) # Starts the game in a wrapped session

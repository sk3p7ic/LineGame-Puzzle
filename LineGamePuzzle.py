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
from os import system as sys_cmd # Used to run "cls" command
import msvcrt, sys, time # Used to get keypresses, exit, and wait

class Game:
  '''Runs the game.'''
  GAME_MAP = [['#' for x in range(0, 12)] for x in range(0, 12)] # Map of game
  CURR_POS = (0, 0) # Position of the player stored as (y, x)
  MOVE_NUM = 0 # Stores the number of moves a player has made
  SPCS_REM = 0 # The number of spaces remaining
  PLAYER_CHAR = [['▒', '▒'], ['▒', '▒']] # The current character position
  USED_SPACES = [['▓', '▓'], ['▓', '▓']] # Spaces used by the player in past
  MAP_BOUNDRS = [['█', '█'], ['█', '█']] # The spaces taken by the map
  UNUSED_SPCE = [[' ', ' '], [' ', ' ']] # Empty space
  PLAYERSPEED = 0.000 # The speed at which the player will move, in seconds

  def __init__(self, infile, start_position=(0,0)):
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

  def printMap(self):
    '''Prints the game map.'''
    def printer(args):
      '''Prints an array of args by printing top of arg, then bottom.'''
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
    sys_cmd("cls") # Clears the screen
    for line in self.GAME_MAP: printer(line) # Call the printer
    print("\n[*] Moves: {moves}".format(moves=self.MOVE_NUM))
    
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
      if msvcrt.kbhit():
        key = ord(msvcrt.getch())
        if key == 119: game.movePlayer('u') # W
        if key == 97: game.movePlayer('l')  # A
        if key == 115: game.movePlayer('d') # S
        if key == 100: game.movePlayer('r') # D
        if key == 113 or key == 27: break
    if self.checkWin(): print("\n\nWINNER!")


if __name__ == "__main__":
  '''Code ran on startup.'''
  infile = open("demo_map.txt", 'r') # File containing the map to be used
  game = Game(infile, (8, 8)) # Initilize game's components
  game.gameloop() # Start the game
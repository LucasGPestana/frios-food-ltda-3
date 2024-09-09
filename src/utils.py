def changeColor(value: float) -> str:

  ansi_escape_colors = {
    "\033[0;31m": value < 0,
    "\033[0;32m": value > 0,
    "\033[0m": value == 0
  }

  for color in ansi_escape_colors.keys():

    if ansi_escape_colors[color]:

      return f"{color}{value}\033[m"
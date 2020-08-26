# Connect Counters

Connect counters is a variant of Connect 4 which I created in Python for my Advanced Higher Computing Science Project for session 2019-2020.
The goal of the game is to connect the greatest sequence of counters together, with counters being able to be connected either horizontally, vertically and diagonally.
The game can be played as single-player only and includes a single difficulity of A.I for the player to compete against.

The game randomly chooses either the player or A.I to go first, after which the game alternates between the two players' turns until the game board is full.
When the game board is full, the winner of the game is calculated and displayed to the user along with the greatest number of counters they and the A.I connected.

The game saves just one occurrence of the player's name along with the greatest number of counters that the player managed to connect to a database table.
Each time the same user plays the game, their score is only updated if their new score is greater than that saved in the database table.
After the winner of the game has been displayed, a leader board showing the names of the players, along with their scores, is displayed for the top 5 scores.

Connect Counters also features a unique user interface for the player to engage with.

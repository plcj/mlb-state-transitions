# mlb-state-transitions
Identification of game state transitions in MLB historical data

For the heck of it, here is an old personal project I developed off and on from 2011-2015.

The purpose was to discover which game states can possibly follow a given game state, and the likelihood of each, in various time periods, using historical data from retrosheet.org.

Most of this was done pretty early in my development experience and it shows, but it taught me a lot and I got answers. No idea if it still runs.

Example output from games from 2000-2013 is in 2000_-_2013.csv.

Next I wanted to create a graphical representation of transitions. getTxns.py and
gst.py are the start of this.

Something along these lines, possibly:

B4 (bottom of the 4th)

0000    x   x   .   .
0003        .   .   .
0020        .   x   .
0100        .   .   .
0023                .
0103                .
0120                x
0123
1000        .   .   .
...
3000                .

Rows show states, columns show which are possible from that state (.) and which occured (x). Blanks were not possible.

Events creating the above example might be: leadoff man HR, second batter doubles, third batter walks.

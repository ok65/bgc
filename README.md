# Board Games Club Website
## WIP Features
* List games owned by club members
* Filter search games
* Record match details (players, scores etc)
* Show stats for games (number of players, who always wins)
* Show player ranks/play info

## Complete Features
* Aspirational list

## Ranking Algorithm
What algorithm would be best to use? 

* Elo (aka Chess)
  * Is a 1v1 algorithm where your score goes up or down depending on win/loss and the score change is relative to the strength of the opponent.
  * Since most games are 1v1v1v1... the algorithm could be repeated for each pairing. Messy?
  * Pros: measures relative strength, rewards beating better players and doesn't penalise lack of play as much
  * Cons: Could be very complex for all the different game types (1v1v1v1, 2v2, no winners only losers). Also doesn't rewards runner ups.

* Points Pool Divvy
  * Idea that each player brings a set number of points into the match pool, then the points are awarded based on player success.
  * In a 1v1v1v1, if each player brings 10pts then you could award points based on position
  * Example would be a quadratic curve, where a 6player game would award points like: 23, 16, 10, 5, 2, 0 from a total pool of 60.
  * The polynomial index can be tweaked to bias first/second place more or less. In a 6 player game i=1.1: first gets 1/4 the points, i=2: first gets 2/3 the points; i=3: first gets half the points.
  * Pros: Rewards runner-ups, and can be easily tweaked to work for 1v1v1, teams or no winners games only losers.
  * Cons: Doesn't consider relative strength of players (could tweak the points a player brings into the pot)
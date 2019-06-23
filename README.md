<img src="sample_images/sample1.jpg" alt="hi" class="inline" width="800" height="400"/>

# Introduction

When playing games which are not perfect information games, where there is relevant information which might not be available to all players, maintaining knowledge about what other agents in the game know is important for predicting the actions of one's opponents, and thus choosing appropriate actions accordingly. This knowledge can be modeled in epistemic logic, and visualized with kripke models, and in this project we do both with the game Konigrufen, a game in which not only the complete state of the game hidden, but the objectives of each player is not perfectly known. For a player, or agent, to win the game they need to obtain as many points as possible (or at least more than half of the total points in the game). In order to increase the likelihood of accomplishing this, they need to win as many tricks as possible which yield as many points as possible. Therefore, for every trick they need to try to play the highest card out of all four players (while adhering to the rules). In order to properly do so, all the agents are required to reason about what their best card to play is. In this game proper reasoning can only be done when there is knowledge present about an agent's cards and its opponent's cards. Therefore in this implementation of Konigrufen, as the game progresses, public announcements are made based on actions of agents which updates their knowledge. We display the knowledge and reasoning of each agent during the game when it's their turn to play. Additionally, during the game the user is able to switch to a display where visualization of a couple of Kripke models is possible, which are also updated throughout the game. 
With this project we want to show that including components of epistemic logic in a simulation of a game, allows us to analyze realistic behaviour of agents playing the game.

## How to run?
In order to run our program, download the .zip or .tar.gz file. Additionally you will also need [Python](https://www.google.com/) (either version 2.7 or 3.5) and the [Pygame Module](https://www.pygame.org/). To run the Konigrufen program, unzip the folder after downloading it and execute the main.py file with python. On Mac/Linux run the command: python main.py from the command prompt. On Windows the standard Python installer associates the .py extension with a python file, so you should be able to double click main.py in order to run it, or you can also run it in the command prompt if you want with python main.py after locating its directory.

# Konigrufen
```diff
+ what is the game (klemen)
```
## The Rules
```diff
+ maybe include a nice table of the cards and their values or something (klemen)
```

The 54 cards in play are divided into 5 suits, the 4 regular suits (hearts, clubs, diamonds and spades) as well as a fifth suit of trump cards. Each of the 4 regular suits has 8 cards, divided into 4 face cards and 4 number cards, the only quirk relating to these is that with the red suit number cards, the lowest in number is the highest in value/strength and for the two black colored suits, the higher number wins. There are 22 trump cards, 21 numbered trump cards and one fool which in this set of rules counts as the 22nd and highest trump card.

The game starts with first 6 cards being set aside for later, then each player getting dealt 12 cards. The cards are dealt in a counterclockwise order starting with the person sitting immediately to the left of the dealer. Once the cards are dealt, each player is asked to state their intentions for this game, this is done in the opposite (clockwise) order starting with the person sitting to the right of the dealer. Each player may either do nothing or play. There are several things someone who wants to make a play can decide, all relating to the 6 cards set aside at the start of the game. They may play with 3, 2, 1 or none of the cards in the pile set aside or the 'talon'. This means that the talon is either divided into two sets of 3 cards (in order) 3 sets of 2 cards or 6 individual cards by the dealer (or someone else in case the dealer is the one making the play). Before the cards in the talon are opened, the person making the play must call a king of one of the four suits to his side. In the event that this king is in the talon, they now play alone. The play maker is allowed to take one of the sets of cards from the talon, either one of the groupings of 3 if this was the number they chose or one of the other configurations. They take these cards into their deck and place the corresponding number of cards face down in front of them as a start to their collection pile. any points in this pile will count towards the total number of points they manage to accrue in the trick taking stage of the game.

In the main stage of the game players start playing for tricks, the game proceeds clockwise, starting with the same person whom the dealer started dealing to. If a player starts with a certain suit, all other players must follow with that suit. If they do not have any cards in this suit, they may play one of the 22 trump cards, if they also have no trump cards, they may play any other card in their hand.

Once all the cards are played, whoever had the king called at the start of the game, combines their pile of taken tricks with the play maker and the other two players in the game do likewise. Cards are counted in groups of 3, a king is worth 5 points, a queen 4, a knight is worth 3 points a jack is worth 2 and every other card is worth 1 point. If there are 2 face cards in this set of 3, 1 point is deducted from the total and if there are 3 face cards, then 2 points are deducted to make the counting always add up to 70. In addition to the face cards, some trumps have value as well. The number 1 trump, the number 21 trump and the fool are all worth 5 points each and count as face cards when being counted. The difference between the two teams in points is then taken as the score. The only people getting any score from a game are the one who made a play and the one who was holding the king that was called at the start of the round. The other two players were essentially 'defending' or trying to minimize the number of points the other two receive at the end of the round.

## Including Epistemic Logic 
- Knowledge
- Public announcements
- Kripke models

# Object Oriented Implementation of Konigrufen
In this section we will describe the several classes that we created and how they are integrated in the program
## Cards
The cards class is a tuple consisting of four components `(suit,value,image,score)` where suit and image speak for themselves. The distinction between value and score however is that the former is the value the card has during the game (e.g. to win a trick) and the latter is for what the card is worth in score for winning the game. Additionally, the value of a card represents what the card actually is dependent on whether it's a trump or not (e.g. a value of 8 for a non-trump card is a King, a value of 7 is a Queen etcetera). For trump cards it simply resembles the trumps from 1 up to 21, and value 22 represents the Joker.

However, it is worth noting that in order to be sure that all interesting cards are included in each game (e.g. the Joker and Kings), we limited the number of cards from 54 to 48, such that each player has exactly 12 cards.  We excluded the first card of each common suit and excluded trump cards '2' and '3'.

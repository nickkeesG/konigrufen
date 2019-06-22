<img src="sample_images/sample1.jpg" alt="hi" class="inline" width="800" height="400"/>

# Introduction

When playing games which are not perfect information games, where there is relevant information which might not be available to all players, maintaining knowledge about what other agents in the game know is important for predicting the actions of one's opponents, and thus choosing appropriate actions accordingly. This knowledge can be modeled in epistemic logic, and visualized with kripke models, and in this project we do both with the game Konigrufen, a game in which not only the complete state of the game hidden, but the objectives of each player is not perfectly known. It is our goal to show that 
```diff
- so what actually is our goal here? that knowing things about things is good?
```

# Konigrufen
```diff
+ what is the game
```

## Implementation
```diff
+ python and stuff
```

## The Rules
The 54 cards in play are divided into 5 suits, the 4 regular suits (hearts, clubs, diamonds and spades) as well as a fifth suit of trump cards. Each of the 4 regular suits has 8 cards, divided into 4 face cards and 4 number cards, the only quirk relating to these is that with the red suit number cards, the lowest in number is the highest in value/strength and for the two black colored suits, the higher number wins. There are 22 trump cards, 21 numbered trump cards and one fool which in this set of rules counts as the 22nd and highest trump card.

The game starts with first 6 cards being set aside for later, then each player getting dealt 12 cards. The cards are dealt in a counterclockwise order starting with the person sitting immediately to the left of the dealer. Once the cards are dealt, each player is asked to state their intentions for this game, this is done in the opposite (clockwise) order starting with the person sitting to the right of the dealer. Each player may either do nothing or play. There are several things someone who wants to make a play can decide, all relating to the 6 cards set aside at the start of the game. They may play with 3, 2, 1 or none of the cards in the pile set aside or the 'talon'. This means that the talon is either divided into two sets of 3 cards (in order) 3 sets of 2 cards or 6 individual cards by the dealer (or someone else in case the dealer is the one making the play). Before the cards in the talon are opened, the person making the play must call a king of one of the four suits to his side. In the event that this king is in the talon, they now play alone. The play maker is allowed to take one of the sets of cards from the talon, either one of the groupings of 3 if this was the number they chose or one of the other configurations. They take these cards into their deck and place the corresponding number of cards face down in front of them as a start to their collection pile. any points in this pile will count towards the total number of points they manage to accrue in the trick taking stage of the game.

In the main stage of the game players start playing for tricks, the game proceeds clockwise, starting with the same person whom the dealer started dealing to. If a player starts with a certain suit, all other players must follow with that suit. If they do not have any cards in this suit, they may play one of the 22 trump cards, if they also have no trump cards, they may play any other card in their hand.

Once all the cards are played, whoever had the king called at the start of the game, combines their pile of taken tricks with the play maker and the other two players in the game do likewise. Cards are counted in groups of 3, a king is worth 5 points, a queen 4, a knight is worth 3 points a jack is worth 2 and every other card is worth 1 point. If there are 2 face cards in this set of 3, 1 point is deducted from the total and if there are 3 face cards, then 2 points are deducted to make the counting always add up to 70. In addition to the face cards, some trumps have value as well. The number 1 trump, the number 21 trump and the fool are all worth 5 points each and count as face cards when being counted. The difference between the two teams in points is then taken as the score. The only people getting any score from a game are the one who made a play and the one who was holding the king that was called at the start of the round. The other two players were essentially 'defending' or trying to minimize the number of points the other two receive at the end of the round.

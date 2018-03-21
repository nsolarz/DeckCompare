# DeckCompare
## A simple Magic: The Gathering deck comparison tool

### What does it do?
This is a very simple python tool to compare two deck.txt files, showing cards that were added/removed/modified/stayed the same between the two decks.

Supports deck files from TappedOut.net, MTGGoldfish.com, or any other simple deck.txt file. Works with decklists that have sideboards as well (see example decks for formatting)

### Arguments
```
usage: DeckCompare.py [-h] --oldDeck OLDDECK --newDeck NEWDECK [-v] [-a] [-r] [-m] [-s] [--forumReady]

A simple deck comparison tool. Default will show added, removed, and modified cards

optional arguments:
  -h, --help         show this help message and exit
  --oldDeck OLDDECK  The old deck to compare
  --newDeck NEWDECK  The new deck to compare
  -v, --verbose
  -a, --added        Shows cards only in the new deck
  -r, --removed      Shows cards only in the old deck
  -m, --modified     Shows cards in both decks but with different card counts
  -s, --same         Shows cards in both decks with the same card counts
  --forumReady       wraps the cardnames in [[ ]] for use within supported forums
```


### Example Usage
`./DeckCompare.py --oldDeck example-deck-1.txt --newDeck example-deck-2.txt -arms --forumReady`

### Example Output
```
Added:
Deck:
1 [[Canyon Slough]]
2 [[Commit]]
3 [[Dusk Legion Zealot]]
1 [[Essence Scatter]]
4 [[Fatal Push]]
3 [[Field of Ruin]]
1 [[Supreme Will]]
3 [[The Scarab God]]
2 [[Torrential Gearhulk]]
4 [[Vraska's Contempt]]

Sideboard:
2 [[Aethersphere Harvester]]
2 [[Arguel's Blood Fast]]
1 [[Doomfall]]
1 [[Glimmer of Genius]]
1 [[Golden Demise]]
1 [[Jace's Defeat]]
2 [[Moment of Craving]]
1 [[River's Rebuke]]

Removed:
Deck:
4 [[Angel of Invention]]
4 [[Concealed Courtyard]]
2 [[Contraband Kingpin]]
3 [[Gate to the Afterlife]]
1 [[Glacial Fortress]]
3 [[God-Pharaoh's Gift]]
2 [[Hostage Taker]]
1 [[Ipnu Rivulet]]
2 [[Kitesail Freebooter]]
4 [[Minister of Inquiries]]
1 [[Ravenous Chupacabra]]
1 [[Search for Azcanta]]
1 [[Trophy Mage]]

Sideboard:
2 [[Dreamstealer]]
3 [[Fatal Push]]
1 [[Hour of Glory]]
2 [[Settle the Wreckage]]
1 [[Solemnity]]
1 [[Vraska's Contempt]]

Modified:
Deck:
[[Fetid Pools]]: was 4 now 3
[[Glint-Sleeve Siphoner]]: was 4 now 2
[[Liliana, Death's Majesty]]: was 2 now 1
[[Swamp]]: was 6 now 3
[[Walking Ballista]]: was 2 now 4

Sideboard:
[[Negate]]: was 2 now 3

Same:
Deck:
4 [[Aether Hub]]
4 [[Champion of Wits]]
4 [[Drowned Catacomb]]
2 [[Gonti, Lord of Luxury]]
4 [[Island]]

Sideboard:
2 [[Duress]]
```

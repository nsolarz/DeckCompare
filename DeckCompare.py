#!/usr/bin/env python3
import argparse
import re
import logging


def main():
    """Main method. This will parse all of the arguments and return the results
    of the deck comparison to the std_out
    """
    parser = argparse.ArgumentParser(description='A simple deck comparison tool. Default will show added, removed, and modified cards')
    parser.add_argument('--oldDeck',
                      type=argparse.FileType('r', encoding='UTF-8'),
                      required=True, help="The old deck to compare")

    parser.add_argument('--newDeck',
                      type=argparse.FileType('r', encoding='UTF-8'),
                      required=True, help="The new deck to compare")

    parser.add_argument('-v', '--verbose', action='count', default=0)

    parser.add_argument('-a', '--added', action='store_true',
                      help="Shows cards only in the new deck")
    parser.add_argument('-r', '--removed', action='store_true',
                      help="Shows cards only in the old deck")
    parser.add_argument('-m', '--modified', action='store_true',
                      help="Shows cards in both decks but with different card counts")
    parser.add_argument('-s', '--same', action='store_true',
                      help="Shows cards in both decks with the same card counts")

    parser.add_argument('--forumReady', action='store_true',
                      help="wraps the cardnames in [[ ]] for use within supported forums")

    ## Load arguments and set logging level
    args = parser.parse_args()

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels)-1,args.verbose)]  # capped to number of levels

    logging.basicConfig(level=level,
                    format="%(asctime)s %(levelname)s %(message)s")

    logging.debug(args)

    ## Determine which card lists to show. If nothing is flagged, show Added,
    ## Removed, and Modified
    showList = [False, False, False, False]

    if (not args.added and not args.removed and not args.modified and not args.same):
        showList =[True,True,True,False]
    else:
        showList[0] = args.added
        showList[1] = args.removed
        showList[2] = args.modified
        showList[3] = args.same

    ## Load the deckfiles into their respective dictionaries
    leftDeck = loadDeck(args.oldDeck)
    rightDeck = loadDeck(args.newDeck)

    ## Retrieve the results of the comparison
    deckResults = dict_compare(rightDeck[0], leftDeck[0])
    sideboardResults = dict_compare(rightDeck[1], leftDeck[1])

    ## Print the results to stdout based on which flags are flipped

    ## Show Added cards
    if (showList[0]):
       print("Added:")
       if (len(deckResults[0]) >0):
           print("Deck:")
           for card in sorted((deckResults[0])):
               print(rightDeck[0][card] + " " +formatCard(card,args.forumReady))
       if (len(sideboardResults[0]) >0):
           print("\nSideboard:")
           for card in sorted((sideboardResults[0])):
               print(rightDeck[1][card] + " " +formatCard(card,args.forumReady))

    ## Show Removed cards
    if (showList[1]):
        print("\nRemoved:")
        if (len(deckResults[1]) >0):
            print("Deck:")
            for card in sorted((deckResults[1])):
                print(leftDeck[0][card] + " " +formatCard(card,args.forumReady))
        if (len(sideboardResults[1]) >0):
            print("\nSideboard:")
            for card in sorted((sideboardResults[1])):
                print(leftDeck[1][card] + " " +formatCard(card,args.forumReady))

    ## Show Modified cards
    if (showList[2]):
        print("\nModified:")
        if (len(deckResults[2]) >0):
            print("Deck:")
            for card in sorted((deckResults[2])):
                print(formatCard(card,args.forumReady) + ": was "
                    + deckResults[2][card][0]
                    + " now " + deckResults[2][card][1] )
        if (len(sideboardResults[2]) >0):
            print("\nSideboard:")
            for card in sorted((sideboardResults[2])):
                print(formatCard(card,args.forumReady) + ": was "
                    + sideboardResults[2][card][0]
                    + " now " + sideboardResults[2][card][1] )

    ## Show Same cards
    if (showList[3]):
        print("\nSame:")
        if (len(deckResults[3]) >0):
            print("Deck:")
            for card in sorted((deckResults[3])):
                print(leftDeck[0][card] + " " +formatCard(card,args.forumReady))
        if (len(sideboardResults[3]) >0):
            print("\nSideboard:")
            for card in sorted((sideboardResults[3])):
                print(leftDeck[1][card] + " " +formatCard(card,args.forumReady))





    ## Print an extra newline for cleanliness
    print("\n")


def loadDeck(deckFile):
    """Loads the deckfile text into a dictionary. The deck file can be an unsorted list with
    a sideboard separated by a newline and/or a line that says "Sideboard:".
    Tested deck.txt files from TappedOut and MTGGoldfish
    Card names must be unique per line and start with an integer count of how many copies
    there are in the deck (an 'x' may be included as well).

    Acceptable lines:
        1 Sol Ring

        1x Sol Ring

    """
    logging.debug("Parsing deck file")
    deck_file_pattern = "(\d+)x? (.+)"
    regex = re.compile(deck_file_pattern)


    content = deckFile.readlines()
    deckFile.close()
    content = [x.strip() for x in content]

    logging.debug("Deckfile contains " + str(len(content)) + " lines")

    deck = {}
    sideboard = {}
    inSideboard = False

    for cardline in content:
        logging.info(cardline)

        if ((cardline != "") and (cardline != "Sideboard:")):
            match = regex.match(cardline)
            if (not inSideboard):
                deck[match.group(2)] = match.group(1)
            else:
                sideboard[match.group(2)] = match.group(1)
        else:
            inSideboard = True

    logging.debug(deck)
    logging.debug(sideboard)
    return deck, sideboard

def forumWrap(cardName):
    """Wraps a cardname in [[ ]] for compatable forums/websites
    """
    return "[[" + cardName +"]]"

def formatCard(cardName, forForum):
    """Returns either a plain cardname or a wrapped one based on the forForum flag
    """
    if (forForum):
        return forumWrap(cardName)
    else:
        return cardName

def dict_compare(d1, d2):
    """Compares two dictionaries. Returns a tuple with the added, removed, modifed,
    and same results
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

if __name__ == "__main__":
    main()

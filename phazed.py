from question1to3 import (convert_cards, sameitems, check_run, 
check_allrun, samecolors, phazed_group_type)
from itertools import combinations

def accumulation_finder_forgroup(cards, total):
    '''
    
    This function will find if there's a possible accumulation depending on 
    the fibonacci sequence.
    It will take a list of cards (2-string) and an integer.
    It will output a list of cards that adds up to the total.
    
    '''
    
    # This variable will hold all the cards in the list of cards (cards). 
    cardlist = [card for card in cards]
    # This variable will hold the cards that add up to the total.
    result = []
    # This variable will hold all the cards but as values.
    cardvalues = []
    # This variable will hold all the possible combinations that add up to the
    # total (which still includes duplicate cards).
    tempset = []
    # This variable will hold all the possible cards that add up to the total.
    all_accumulations = []
    
    # First, we convert all the cards into values.
    for card in cardlist:
        cardvalues.append(convert_cards(card[0]))

    # Then, we find all the possible combinations with the values.    
    for i in range(1, 10):
        cardcombinations = list(combinations(cardvalues, i))
        
        # Next, we check if they add up to the total.
        for cards in cardcombinations:
            totalcombs = sum(cards)
            if totalcombs == total:
                tempset.append(cards)
                
    # If there are no possible combinations, it will instantly return
    # an empty list.
    if not tempset:
        return all_accumulations
    
    # Else, it will make sure the second set of accumulations have no 
    # duplicate cards.
    all_accumulations.append(tempset[-1])
    for card in tempset[-1]:
        cardvalues.remove(card)
    
    # It will repeat the combinations again but with the cards that do not
    # include the first accumulation.
    # This variable will hold all the possible combinations with the cards that
    # do not include the first accumulation.
    secondtempset = []    
    for i in range(3, len(cardvalues)):
        cardcombinations = list(combinations(cardvalues, i))
        
        for cards in cardcombinations:
            totalcombs = sum(cards)
            if totalcombs == total:
                secondtempset.append(cards)
                
    # This variable will hold all the cards from the cardlist.            
    cardlist_withvalues = [convert_cards(card[0]) for card in cardlist]
    
    # Next, we convert the values into cards.
    for group in all_accumulations:
        
        for value in group:
            cardposition = cardlist_withvalues.index(value)
            if cardlist[cardposition] in cardlist:
                result.append(cardlist[cardposition])
                cardlist_withvalues.pop(cardposition)
                cardlist.pop(cardposition)
        
    return result   

def group_validity(plannedcard, table, hand):
    '''
    
    This function will check if we are able to place a card on any of the
    phases on the table.
    It takes a 2-string, a 4-element list, and a list of cards.
    It outputs True/False, and 3 other integers.
    
    '''
    
    # This variable holds either True or False, and whether we can put down
    # the card or not.
    placedowncard = False
    # This variable holds the index of the table/ or on which player's phase
    # should the card be placed down.
    tableposition = 0
    # This variable will hold the index of the group we want to place the card
    # in.
    groupposition = 0
    # This variable will hold the index where we want to put the card in the 
    # group.
    indexposition = 0
    # This variable holds the fibonacci sequence.
    fibonacci = 34, 55, 68, 76, 81, 84, 86, 87, 88
    # This variable will tell us if there are any incomplete 
    # accumulations.
    incomplete_accum = False
    # This variable holds the position of the incomplete accumulation.
    accum_table = 0
    
    # This will check for any incomplete accumulations.
    for sets in table:
        if sets[0]:
            if sets[0] == 3:
                total = 0
                for card in sets[1][0]:
                    total += convert_cards(card[0])
                if total not in fibonacci:
                    accum_table = table.index(sets)
                    incomplete_accum = True 
    
    # First, we check if there are any phase 3s on the table.
    # If possible, it will put down all the cards that can be put down on the
    # phase.
    for sets in table:
        if sets[0]:
            if sets[0] == 3:
                
                # This variable holds all the cards from the phase's first 
                # group.
                temphand_first = [card for card in sets[1][0]]
                
                # If there are 2 groups in a phase, it will assign another
                # variable to hold all the cards from the second group.
                if len(sets[1]) == 2:
                    temphand_second = [card for card in sets[1][1]]
                
                
                # This variable holds the total number of cards needed to 
                # complete the fibonacci sequence.
                completed = 0
                # This variable will hold the current total of the group.
                total = 0
                
                # This will convert the cards into values and add it to
                # the total.
                for card in temphand_first:
                    total += convert_cards(card[0])
                
                # This will find the total number of cards needed to 
                # complete the fibonacci sequence.
                for num in fibonacci:
                    if total < num:
                        completed = num
                        break 
                     
                # This will check if the cards in the current hand
                # can fulfill the fibonacci sequence.
                # If so, it will return the card that can fulfill it and the
                # positions.
                if accumulation_finder_forgroup(hand, completed - total):
                    if plannedcard in \
                        accumulation_finder_forgroup(hand, completed - total):
                        placedowncard = True
                        tableposition = table.index(sets)
                        groupposition = 0
                        break
                else:
                    # If not, it will repeat the process again for the
                    # second group.
                    total = 0
                    for card in temphand_second:
                        total += convert_cards(card[0])
     
                    for num in fibonacci:
                        if total < num:
                            completed = num
                            break 
                            
                    if accumulation_finder_forgroup(hand, completed - total):
                        if plannedcard in \
                            accumulation_finder_forgroup(hand, 
                                                         completed - total):
                            placedowncard = True
                            tableposition = table.index(sets)
                            groupposition = 1
                            break
    if incomplete_accum is True and placedowncard is True:
        if tableposition != accum_table:
            return False, 0, 0, 0
    # These variables are repeated again here to make sure the variables
    # are empty.
    temphand_first = []
    temphand_second = []
    
    # If no cards can be placed down in the accumulation phases,
    # it will check the conditions for other phases.
    if placedowncard is False:
        for sets in table:
            
            if sets[0]:
                
                # This will hold all the cards in the first group
                # of the phase
                temphand_first = [card for card in sets[1][0]]
                # If there are 2 groups, another variable will be 
                # assigned to hold the second group's cards
                if len(sets[1]) == 2:
                    temphand_second = [card for card in sets[1][1]]
                
                # If it's phase 1 or 4, it will check if the card has the 
                # same value as the groups.
                if sets[0] == 1 or sets[0] == 4:

                    temphand_first.append(plannedcard)
                    temphand_second.append(plannedcard)

                    if sameitems(0, temphand_first) is True:
                        placedowncard = True
                        tableposition = table.index(sets)
                        groupposition = 0
                        break
                    elif sameitems(0, temphand_second) is True:
                        placedowncard = True
                        tableposition = table.index(sets)
                        groupposition = 1
                        break
                        
                # If it's phase 2, it will check if the card has the same suit
                # as the groups.
                elif sets[0] == 2:
                    
                    temphand_first.append(plannedcard)
                    if sameitems(1, temphand_first) is True:
                        placedowncard = True
                        tableposition = table.index(sets)
                        groupposition = 0
                        break
                
                # If it's phase 5, it will check if the card can be added as a
                # run. 
                elif sets[0] ==  5:
                    # This will make sure that the run we're planning to add
                    # a card in is less than 12. (Since 12 is the max for run)
                    if len(sets[1][0]) < 12: 
                        
                        # This variable will hold all the values of the cards.
                        cards_withvalues = [card[0] for card in 
                                            temphand_first if card[0] != 'A']
                            
                        # The code will test the card as the first card
                        # in the run first.
                        temphand_first.insert(0, plannedcard)

                        # This will check if it's a run or not.
                        if check_allrun(temphand_first) is True:
                            placedowncard = True
                            tableposition = table.index(sets)
                            groupposition = 0
                            indexposition = 0
                            break
                        else:
                            # If not, it will remove the first card and
                            # add the card in the end of the run.
                            # It will then check if it's a run.
                            temphand_first.pop(0)
                            temphand_first.insert(len(sets[1][0]), 
                                                  plannedcard)
                            if check_allrun(temphand_first) is True:
                                placedowncard = True
                                tableposition = table.index(sets)
                                groupposition = 0
                                indexposition = len(sets[1][0])
                                break
                
                # If it's phase 7, it will check if the card can be added
                # into a run and has the same color, or the same value group.
                elif sets[0] == 7:
                    
                    # This code will check if the card can be added into
                    # the run and is the same color.
                    temphand_first.insert(0, plannedcard)
                    cards_withvalues = [card[0] for card in temphand_first 
                                        if card[0] != 'A']
                    
                    # This will check if the run's length is less than 12,
                    # if the card is not in the run, and whether it has the
                    # same color.
                    if len(sets[1][0]) < 12:
                        if plannedcard[0] not in cards_withvalues:
                            if samecolors(temphand_first) is True:
                                
                                # It will then check if it's a run, if the card
                                # is added to the front of the run.
                                if check_allrun(temphand_first) is True:
                                    placedowncard = True
                                    tableposition = table.index(sets)
                                    groupposition = 0
                                    indexposition = 0
                                    break
                                else:
                                    # If not, it will check if it's a run
                                    # at the end of the run.
                                    temphand_first.pop(0)
                                    temphand_first.insert(len(sets[1][0]), 
                                                          plannedcard)
                                    if check_allrun(temphand_first) is True:
                                        placedowncard = True
                                        tableposition = table.index(sets)
                                        groupposition = 0
                                        indexposition = len(sets[1][0])
                                        break
                    
                    # If the card can't be added to the run, it will check
                    # if the card has the same value as the group.
                    temphand_second.insert(0, plannedcard)

                    if sameitems(0, temphand_second) is True:
                        placedowncard = True
                        tableposition = table.index(sets)
                        groupposition = 1
                        break
                    
    return placedowncard, tableposition, groupposition, indexposition  

def groupvalidity_forphase(plannedcard, phase, phasenumber, hand):
    '''
    
    This function will check if we can add more cards to our own phase,
    if we have not place our phase down.
    It will take in a 2-string, a list of cards (2-string), an integer, and
    another list of cards (2-string).
    It will output either True/False. 
    
    '''
    
    # This variable will hold the status of whether the card can be placed
    # down or not.
    placedowncard = False
    # This variable holds the fibonacci sequence.
    fibonacci = 34, 55, 68, 76, 81, 84, 86, 87, 88
    # This variable will hold all the cards in the phase's first group.
    temphand_first = [card for card in phase[0]]
    
    # If there are 2 groups in the phase, it will assign another variable to
    # hold the second group's cards.
    if len(phase) == 2:
        temphand_second = [card for card in phase[1]]

    # If if it's phase 1 or 4, it will check if the card has the same value.
    if phasenumber == 1 or phasenumber == 4:

        temphand_first.append(plannedcard)
        temphand_second.append(plannedcard)

        if sameitems(0, temphand_first) is True:
            placedowncard = True
         
        elif sameitems(0, temphand_second) is True:
            placedowncard = True
            
    # If it's phase 2, it will check if the card has the same suit.
    elif phasenumber == 2:

        temphand_first.append(plannedcard)

        if sameitems(1, temphand_first) is True:
            placedowncard = True
    
    # If it's phase 3, it will check if there are any cards that can fulfill
    # the fibonacci sequence.
    elif phasenumber == 3:
        
        # This variable holds the total number of cards needed to 
        # complete the fibonacci sequence.
        completed = 0
        # This variable will hold the current total of the group.
        total = 0
        
        # This will convert the cards into values and add it to
        # the total
        for card in temphand_first:
            total += convert_cards(card[0])
        
        # This will find the total number of cards needed to 
        # complete the fibonacci sequence.
        for num in fibonacci:
            if total < num:
                completed = num
                break
        
        # This will check if the cards in the current hand
        # can fulfill the fibonacci sequence.
        if accumulation_finder_forgroup(hand, completed - total):
            if plannedcard in accumulation_finder_forgroup(hand, 
                                                           completed - total):
                placedowncard = True
                
        else:
            # If not, it will repeat the process again for the
            # second group.
            total = 0
            for card in temphand_second:
                total += convert_cards(card[0])

            for num in fibonacci:
                if total < num:
                    completed = num
                    break 

            if accumulation_finder_forgroup(hand, completed - total):
                if plannedcard in \
                    accumulation_finder_forgroup(hand, completed - total):
                    placedowncard = True
                    
    # If it's phase 5, it will check if the card can be added as a
    # run. 
    elif phasenumber ==  5:
        
        # The code will test the card as the first card
        # in the run first.
        temphand_first.insert(0, plannedcard)
        
        # This will check if it's a run or not.
        if check_allrun(temphand_first) is True:
            placedowncard = True
            
        else:
            # If not, it will remove the first card and add it again at the end
            # of the run.
            temphand_first.pop(0)
            temphand_first.insert(len(phase[0]), plannedcard)
            # It will then check if it's a run or not.
            if check_allrun(temphand_first) is True:
                placedowncard = True
                
    # If it's phase 7, it will check if the card can be added to the run and 
    # has the same color, or the group with the same values.
    elif phasenumber == 7:
        
        # It will check if it can be added to the run first.
        # And the card will be added to the front of the list first.
        temphand_first.insert(0, plannedcard)
        
        # If the card has the same color, it will check if it's a run.
        if samecolors(temphand_first) is True:

            if check_allrun(temphand_first) is True:
                placedowncard = True
                
            else:
                # If it's not considered a run when the card was added to the
                # front of the run. Then, it will check if it's a run
                # when the card is added to the end of the run.
                temphand_first.pop(0)
                temphand_first.insert(len(phase[0]), plannedcard)
                if check_allrun(temphand_first) is True:
                    placedowncard = True

        # If the card can't be added to the run, it will check if the 
        # card has the same value as the second group.
        temphand_second.insert(0, plannedcard)
        
        if sameitems(0, temphand_second) is True:
            placedowncard = True
           
            
                    
    return placedowncard
    
def calculating_phase(hand, phase_status):
    '''
    
    This function will check if a phase can be made from the hand.
    It will take a list of cards, and an integer.
    It will output a list, and either True or False.
    
    '''
    
    # This variable holds all the aces from the hand.
    aces = []
    # This variable holds all the cards from the hand that are not aces.
    remainder = []
    # This variable will hold the status of whether the phase is 
    # completed or not.
    completed_phase = False
    
    # First, we separate the aces and the other cards to their variables.
    for card in hand:
        if card[0] == 'A':
            aces.append(card)
        else:
            remainder.append(card)
    
    # This variable holds the phase that can be placed down.
    possible_phase = []
    # This variable holds the groups in the phase, which will be appended
    # into the possible_phase variable.
    possible_group = []
    
    # If the phase needed right now is 1, it will find all the cards that 
    # have the same value into lists of 3 elements.
    if phase_status == 1:
        possible_phase = possible_sameitems(3, 0, aces, remainder)
        if len(possible_phase) == 2:
            completed_phase = True
    
    # If it's phase 2, it will find all the cards that have the same suit into
    # a list of 7 elements.
    elif phase_status == 2:
        possible_phase = possible_sameitems(7, 1, aces, remainder)
        if len(possible_phase) == 1:
            completed_phase = True
    
    # If it's phase 3, it will find all the cards that add up to 34 into
    # 2 lists.
    elif phase_status == 3:
        possible_phase = accumulation_finder(hand)
        if len(possible_phase) == 2:
            completed_phase = True
    
    # If it's phase 4, it will find all the cards with the same value into 
    # lists of 4 elements.
    elif phase_status == 4:
        possible_phase = possible_sameitems(4, 0, aces, remainder)
        if len(possible_phase) == 2:
            completed_phase = True
    
    # If it's phase 5, it will find all the cards that form a run.
    elif phase_status == 5:
        possible_phase = first_run_finder(aces, remainder)
        
        if possible_phase:
            possible_phase = [possible_phase]
            if len(possible_phase) == 1:
                completed_phase = True
    
    # If it's phase 6, it will separate the hand to black cards and red cards.
    # Then, it will check if an accumulation of 34 can be formed depending
    # on their colors.
    elif phase_status == 6:
        
        # This variable holds all the suits that are black.
        black = ['C', 'S']
        
        # This variable will hold all the cards that are black.
        black_cards = []
        # This variable will hold all the cards that are red.
        red_cards = []
        
        # First, we separate the cards to black or red. 
        for card in hand:
            if card[1] in black:
                black_cards.append(card)
            else:
                red_cards.append(card)
                
        # Next, we find the possible accumulations depending on their color.
        blackaccum = accumulation_finder(black_cards)
        redaccum = accumulation_finder(red_cards)
        length_blackaccum = 0
        length_redaccum = 0

        # This will check if there are any accumulations found or not.
        if blackaccum:
            length_blackaccum = len(blackaccum)
        if redaccum:
            length_redaccum = len(redaccum)

        if length_blackaccum == 1 and length_redaccum == 1:
            possible_phase.append(blackaccum[0])
            possible_phase.append(redaccum[0])
        elif length_blackaccum == 0 and length_redaccum == 1:
            possible_phase.append(redaccum[0])
        elif length_blackaccum == 1 and length_redaccum == 0:
            possible_phase.append(blackaccum[0])
        elif length_blackaccum == 2 and length_redaccum == 0:
            possible_phase.append(blackaccum[0])
            possible_phase.append(blackaccum[1])
        elif length_blackaccum == 0 and length_redaccum == 2:
            possible_phase.append(redaccum[0])
            possible_phase.append(redaccum[1])

        if len(possible_phase) == 2:
            completed_phase = True
    
    # If it's phase 7, it will find all the cards that form a same color
    # run and a 4 element list of cards with the same value.
    elif phase_status == 7:
        
        # This variable holds all the suits that are black.
        black = ['C', 'S']
        
        # This variable will hold all the cards that are black.
        black_cards = []
        # This variable will hold all the cards that are red.
        red_cards = []

        # This will separate the cards depending on their color.
        for card in remainder:
            if card[1] in black:
                black_cards.append(card)
            else:
                red_cards.append(card)
        
        # It will then check the run depending on their colors.
        black_run = second_run_finder(aces, black_cards)
        red_run = second_run_finder(aces, red_cards)
        
        # Next, it will check if any runs are found.
        if black_run:
            for card in black_run:
                possible_group.append(card)
            possible_phase.append(possible_group)
        elif red_run:
            for card in red_run:
                possible_group.append(card)
            possible_phase.append(possible_group)
        
        # If a run is found, the cards will be removed from the original lists
        # to prevent duplicates when finding the next group.
        if possible_phase:
            for card in possible_phase[0]:
                if card[0] != 'A':
                    remainder.remove(card)
                else:
                    aces.remove(card)

        # Then, we find all the cards that have the same value in a 
        # 4 element string.
        samevalue_phase = possible_sameitems(4, 0, aces, remainder)
        
        
        if samevalue_phase: 
            possible_phase.append(samevalue_phase[0])

        if len(possible_phase) == 2:
            completed_phase = True
    
    return possible_phase, completed_phase
    
def first_run_finder(aces, remainder):
    '''
    
    This function will find all the possible 8-element runs.
    It will take 2 lists of 2-strings.
    It will output a list of cards(2-string).
    
    '''
    
    # This variable will hold the cards in aces.
    acelist = [card for card in aces]    
    # This variable will hold all the values of the cards.
    cardvalues = []
    # This list will hold all the unique values.
    runlist = []
    # This card will hold the possible run.
    runvalue_inhand = []
    
    # First, we convert the cards into values.
    for card in remainder:
        cardvalues.append(convert_cards(card[0]))
    
    # Then, we find all the unique values and then sort it.
    for card in cardvalues:
        if card not in runlist:
            runlist.append(card)
    runlist.sort()
    
    # This variable holds all the possible run orders.
    runorders = [(2, 3, 4, 5, 6, 7, 8, 9), (3, 4, 5, 6, 7, 8, 9, 10), 
                 (4, 5, 6, 7, 8, 9, 10, 11), (5, 6, 7, 8, 9, 10, 11, 12), 
                 (6, 7, 8, 9, 10, 11, 12, 13), 
                 (7, 8, 9, 10, 11, 12, 13, 2), 
                 (8, 9, 10, 11, 12, 13, 2, 3), 
                 (9, 10, 11, 12, 13, 2, 3, 4), 
                 (10, 11, 12, 13, 2, 3, 4, 5), 
                 (11, 12, 13, 2, 3, 4, 5, 6), 
                 (12, 13, 2, 3, 4, 5, 6, 7), (13, 2, 3, 4, 5, 6, 7, 8)]

    # Then, this will check if we have the cards in the run of the runorder.
    for run in runorders:
        # This variable holds the aces needed in the run.
        aceneeded = 0
        # This will count the aces needed in the run.
        for value in run:
            if value not in runlist:
                aceneeded += 1
        # If we have enough aces to form a run, it will be appended.
        if aceneeded == 0:
            runvalue_inhand.append(run)
        elif aceneeded <= len(acelist) and aceneeded <= 6:
            runvalue_inhand.append(run)
    
    if not runvalue_inhand:
        return runvalue_inhand
    
    # This variable holds all the cards of the run.
    runcards_inhand = [] 
    # This variable holds all the values of the original list.
    cardlist_withvalues = [convert_cards(card[0]) for card in remainder]
    
    # Here, we convert the values into cards.
    for value in runvalue_inhand[0]:
        if value in cardlist_withvalues:
            cardposition = cardlist_withvalues.index(value)
            if remainder[cardposition] in remainder:
                    runcards_inhand.append(remainder[cardposition])
        else:
            runcards_inhand.append(acelist[0])
            acelist.pop(0)
            
    return runcards_inhand
    
def second_run_finder(aces, remainder):
    '''
    
    This function will find all the possible 8-element runs.
    It will take 2 lists of 2-strings.
    It will output a list of cards(2-string).
    
    '''
    
    # This variable will hold the cards in aces.
    acelist = [card for card in aces]    
    # This variable will hold all the values of the cards.
    cardvalues = []
    # This list will hold all the unique values.
    runlist = []
    # This card will hold the possible run.
    runvalue_inhand = []

    # First, we convert the cards into values.
    for card in remainder:
        cardvalues.append(convert_cards(card[0]))
    
    
    # Then, we find all the unique values and then sort it.
    for card in cardvalues:
        if card not in runlist:
            runlist.append(card)
    runlist.sort()
    
    # This variable holds all the possible run orders.
    runorders = [(2, 3, 4, 5,), (3, 4, 5, 6), (4, 5, 6, 7), (5, 6, 7, 8),
                     (6, 7, 8, 9), (7, 8, 9, 10), (8, 9, 10, 11), 
                     (9, 10, 11, 12), (10, 11, 12, 13), (11, 12, 13, 2), 
                     (12, 13, 2, 3), (13, 2, 3, 4)] 
    
    # Then, this will check if we have the cards in the run of the runorder.
    for run in runorders:
        # This variable holds the aces needed in the run.
        aceneeded = 0
        # This will count the aces needed in the run.
        for value in run:
            if value not in runlist:
                aceneeded += 1
        # If we have enough aces to form a run, it will be appended.
        if aceneeded == 0:
            runvalue_inhand.append(run)
        elif aceneeded <= len(acelist) and aceneeded <= 2:
            runvalue_inhand.append(run)
    
    if not runvalue_inhand:
        return runvalue_inhand
    
    # This variable holds all the cards of the run.
    runcards_inhand = []    
    # This variable holds all the values of the original list.
    cardlist_withvalues = [convert_cards(card[0]) for card in remainder]
    
    # Here, we convert the values into cards.
    for value in runvalue_inhand[0]:
        if value in cardlist_withvalues:
            cardposition = cardlist_withvalues.index(value)
            if remainder[cardposition] in remainder:
                    runcards_inhand.append(remainder[cardposition])          
        else:
            runcards_inhand.append(acelist[0])
            acelist.pop(0)
    return runcards_inhand

def accumulation_finder(cards):
    '''
    
    This function will find if there's a possible accumulation of 34.
    It will take a list of cards (2-string).
    It will output a list of cards that adds up to 34.
    
    '''
    
    # This variable will hold all the cards in the list of cards (cards). 
    cardlist = [card for card in cards]
    # This variable will hold the cards that add up to the total.
    result = []
    # This variable will hold all the cards but as values.
    cardvalues = []
    # This variable will hold all the possible combinations that add up to the
    # total (which still includes duplicate cards).
    tempset = []
    # This variable will hold all the possible cards that add up to the total.
    all_accumulations = []
    
    # First, we convert all the cards into values.
    for card in cardlist:
        cardvalues.append(convert_cards(card[0]))

    # Then, we find all the possible combinations with the values. 
    # the range is 3-8 as the lowest possible amount of cards to make a 34 
    # is 3 and the highest is 8 (since we need to find 2 accumulations).
    for i in range(3, 8):
        cardcombinations = list(combinations(cardvalues, i))
        # Next, we check if they add up to 34.
        for cards in cardcombinations:
            totalcombs = sum(cards)
            if totalcombs == 34:
                tempset.append(cards)
    
    # If there are no possible combinations, it will instantly return
    # an empty list.
    if not tempset:
        return all_accumulations
    
    # Else, it will make sure the second set of accumulations have no 
    # duplicate cards.
    all_accumulations.append(tempset[-1])
    for card in tempset[-1]:
        cardvalues.remove(card)
    
    # It will repeat the combinations again but with the cards that do not
    # include the first accumulation.
    # This variable will hold all the possible combinations with the cards that
    # do not include the first accumulation.
    secondtempset = []    
    for i in range(3, len(cardvalues)):
        cardcombinations = list(combinations(cardvalues, i))
        
        for cards in cardcombinations:
            totalcombs = sum(cards)
            if totalcombs == 34:
                secondtempset.append(cards)
    
    # This variable will hold all the cards from the cardlist.  
    cardlist_withvalues = [convert_cards(card[0]) for card in cardlist]
    
    # If another accumulation is found, it will be added to the
    # all_accumulations list.
    if secondtempset:
        all_accumulations.append(secondtempset[-1])
    
    # Next, we convert the values into cards.
    for group in all_accumulations:
        small_list = []
        for value in group:
            cardposition = cardlist_withvalues.index(value)
            if cardlist[cardposition] in cardlist:
                small_list.append(cardlist[cardposition])
                cardlist_withvalues.pop(cardposition)
                cardlist.pop(cardposition)
        result.append(small_list)
    return result                              
            
            
def possible_sameitems(length, index, aces, remainder):
    '''
    
    This function will find all the lists with the same items.
    It will take in the length that is wanted for the list, the index they wish
    to match (0 for value, 1 for suit), 2 lists of 2-strings.
    It will output all the possible lists with the same items.
    
    '''
    
    # This variable holds the frequencies of the items.
    tally = {}
    # This variable holds all the possible lists with the same item.
    phase_sameitems = []
    # This variable holds one of the lists with the same item, which will
    # be appended into phase_sameitems.
    set_sameitems = []
    
    # First, we find the frequencies of the items.
    for card in remainder:
            if card[index] in tally:
                tally[card[index]] += 1
            else:
                tally[card[index]] = 1
    
    # Then we check if the frequency is more than the length.
    for key in tally:
        if tally[key] >= length:
            # If so, it will make 1 list.
            for card in remainder:
                if card[index] == key:
                    set_sameitems.append(card)
                    
            # This will remove the elements in the list until it matches
            # the length needed.
            while len(set_sameitems) > length:
                set_sameitems.pop(-1)
            phase_sameitems.append(set_sameitems)
            
            # This will remove the cards to prevent duplicates.
            for card in set_sameitems:
                remainder.remove(card)
                
            set_sameitems = []
        
        # The frequency has to be bigger than 2 because you can only play a 
        # group if it at least has 2 natural numbers.
        elif tally[key] >= 2 and tally[key] < length:
            
            # If the frequency does not go over the wanted length, we can fill
            # the rest of the cards with aces (If there are any).
            if len(aces) >= (length - tally[key]):
                for card in remainder:
                        if card[index] == key:
                            set_sameitems.append(card)
                for card in aces:
                    set_sameitems.append(card)    
                while len(set_sameitems) > length:
                    set_sameitems.pop(-1)
                phase_sameitems.append(set_sameitems)
                
                for card in set_sameitems:
                    if card[0] != 'A':
                        remainder.remove(card)
                    else:
                        aces.remove(card)
                set_sameitems = []
    
    if len(phase_sameitems) >= 2:
        return phase_sameitems[-2:]
    else:
        return phase_sameitems

def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    '''
    
    This function is to find out what play should be done next.
    It takes in an integer, a 4 element list, a list of lists, 
    another integer, a list of 2 strings, and a 2-string.
    It outputs a tuple that consists of either integers, a list, a 2 string.
       
    '''
    
    # This variable holds all the aces in the hand
    aces = []
    # This variable holds all the cards that are not aces.
    remainder = []
    
    # First, we separate the aces and the other cards.
    for card in hand:
        if card[0] == 'A':
            aces.append(card)
        else:
            remainder.append(card)
    
    # Then we check if we've completed a phase or not.
    if not table[player_id][0]:
        
        # If not, we find out if we can place a phase or not.
        current_groups_in_hand = calculating_phase(hand, 
                                                   phase_status[player_id] + 1)
        
        
       
        if turn_history: 
            if player_id not in turn_history[-1]:
                if current_groups_in_hand[1] is False:
                    # If it's our first play and we can't place any phases,
                    # we find out whether we should take from the discard pile
                    # or the deck.
                    hand.append(discard)
                    new_groups_in_hand = calculating_phase(
                        hand, phase_status[player_id] + 1)
                    
                    # This variable holds the status of whether the group we're
                    # planning on playing has an ace or not.
                    aceavailable = False
                    
                    # This will check if the group has an ace or not.
                    if current_groups_in_hand[0]:
                        for card in current_groups_in_hand[0][0]:
                            if card[0] == 'A':
                                aceavailable = True
                                break
                                
                    if aceavailable is True:
                        # If there is an ace, it will check if the card 
                        # from the discard pile can replace the ace.
                        if current_groups_in_hand[0] != new_groups_in_hand[0]:
                            return (2, discard)
                    
                    # Then we check if the discard pile card can complete
                    # the phase.
                    if len(new_groups_in_hand[0]) > \
                        len(current_groups_in_hand[0]):
                        return (2, discard)
                    else:
                        # If not, it will check again if the discard can help
                        # in getting another group.
                        hand.pop(-1)
                        
                        # This variable holds all the other cards beside
                        # the cards that have already formed a group.
                        temporary_cards = []

                        # We first find the remaining cards that have not
                        # formed a group.
                        if current_groups_in_hand[0]:
                            temporary_cards = [card for card in remainder]    
                            for card in remainder:
                                if card in current_groups_in_hand[0][0]:
                                    temporary_cards.remove(card)   
                        else:
                            temporary_cards = [card for card in remainder]
                        
                        # If the discard pile card is an ace and our
                        # phase status isn't 3 or 6 (accumulations), it will
                        # take it.
                        if phase_status[player_id] + 1 != 3 or \
                            phase_status[player_id] + 1 != 6:
                            if discard[0] == 'A':
                                    return (2, discard)
                        
                        # If our current phase status is 1, and if the discard
                        # card pile helps increase the frequency of the value,
                        # the card from the discard pile will be taken.
                        if phase_status[player_id] + 1 == 1:  
                            tally = {}
                            # This will count the frequency of the values.
                            for card in temporary_cards:
                                if card[0] in tally:
                                    tally[card[0]] += 1
                                else:
                                    tally[card[0]] = 1
                            
                            # It will then check if the discard card pile 
                            # is in the tally but it will prioritize the
                            # cards with the highest frequency first.
                            for key in tally:
                                if tally[key] == 2:
                                    if discard[0] == key:
                                        return (2, discard)
                                    
                            if discard[0] in tally:
                                return (2, discard)
                            else:
                                return (1, None)
                        
                        # If it's phase 2, if the discard pile card matches
                        # the card suit with the highest frequency, it will
                        # take the card from the discard pile.
                        elif phase_status[player_id] + 1 == 2:
                            tally = {}
                            # This counts the frequency of the suits.
                            for card in temporary_cards:
                                if card[1] in tally:
                                    tally[card[1]] += 1
                                else:
                                    tally[card[1]] = 1
                            
                            # This variable holds the suit with the highest
                            # frequency.
                            highestsuit = ''
                            # This variable holds the frequency of the 
                            # highest suit.
                            highsuitwithpoints = 0
                            
                            # It will then check if the discard card pile 
                            # is in the tally but it will prioritize the
                            # cards with the highest frequency first.
                            for key in tally:
                                if tally[key] > highsuitwithpoints:
                                    highsuitwithpoints = tally[key]
                                    highestsuit = key
                                    
                            if discard[1] == highestsuit:
                                return (2, discard)
                            else:
                                return (1, None)
                         
                        # If the phase is 4, it will check if the discard
                        # card pile helps increase the frequency of the value,
                        # the card from the discard pile will be taken.
                        elif phase_status[player_id] + 1 == 4:
                            tally = {}
                            # This counts up the frequency of the cards'
                            # values. 
                            for card in temporary_cards:
                                if card[0] in tally:
                                    tally[card[0]] += 1
                                else:
                                    tally[card[0]] = 1
                            
                            # It will then check if the discard card pile 
                            # is in the tally but it will prioritize the
                            # cards with the highest frequency first.
                            for key in tally:
                                if tally[key] == 3:
                                    if discard[0] == key:
                                        return (2, discard)
                                    
                            for key in tally:
                                if tally[key] == 2:
                                    if discard[0] == key:
                                        return (2, discard) 
                                    
                            if discard[0] in tally:
                                return (2, discard)
                            else:
                                return (1, None)
                            
                        # If it's none of the phases above,it will simply
                        # just take a card from the deck.
                        return (1, None)
                else:
                    # If it's still the first turn and we have a phase in our
                    # hand, it will check if we can put the discard card 
                    # anywhere on the table. If so, it will take the 
                    # discard card.
                    if group_validity(discard, table, hand)[0] is True:
                        return (2, discard)
                    else:
                        # If not, we check if the discard card can be added
                        # to the phase in our hand.
                        if groupvalidity_forphase(discard, 
                                                  current_groups_in_hand[0], 
                                                  phase_status[player_id] + 1,
                                                  hand) is True:
                            return (2, discard)
                        else:
                            return (1, None)

            else:
                if current_groups_in_hand[1] is True:
                    # If it's not the first turn and we have a phase in our
                    # hand, the phase will be played.
                    return (3, (phase_status[player_id] + 1,
                                current_groups_in_hand[0]))
                else:
                    # If it's the first turn and we dont have a phase in our
                    # hand, this code will decide what card we should discard.
                    
                    # This variable holds the remaining cards that are not
                    # in a group.
                    temporary_cards = []
                    
                    # This code will find the remaining cards.
                    if current_groups_in_hand[0]:
                        temporary_cards = [card for card in remainder]    
                        for card in remainder:
                            if card in current_groups_in_hand[0][0]:
                                temporary_cards.remove(card)
                    else:
                        temporary_cards = [card for card in remainder]
                    
                    # If the current phase is 1 or 4, it will discard the card
                    # value with the lowest frequency.
                    if phase_status[player_id] + 1 == 1 or \
                        phase_status[player_id] + 1 == 4:
                        
                        # This variable will hold the value with the lowest 
                        # frequency.
                        discard_value = 0
                        tally = {}
                        
                        # This will count the frequency of the values.
                        for card in temporary_cards:
                            if card[0] in tally:
                                tally[card[0]] += 1
                            else:
                                tally[card[0]] = 1
                        
                        # This will find the value with a frequency of 1.
                        lowestcard = 1       
                        for key in tally:
                            if tally[key] == lowestcard:
                                discard_value = key
                                break
                        
                        # If none of the values have a frequency of 1, it will
                        # find the next lowest frequency.
                        while not discard_value:
                            for key in tally:
                                if tally[key] == lowestcard + 1:
                                    discard_value = key
                            lowestcard += 1
                        
                        for card in temporary_cards:
                            if card[0] == discard_value:
                                return (5, card)
                    
                    # If it's phase 2, it will discard the suit with the lowest
                    # frequency.
                    elif phase_status[player_id] + 1 == 2:
                        
                        # This variable will hold the suit with the lowest 
                        # frequency.
                        discard_value = 0
                        tally = {}
                        
                        # This will count the suit's frequency.
                        for card in temporary_cards:
                            if card[1] in tally:
                                tally[card[1]] += 1
                            else:
                                tally[card[1]] = 1
                                
                        # This will find the value with a frequency of 1.      
                        lowestcard = 1       
                        for key in tally:
                            if tally[key] == lowestcard:
                                discard_value = key
                                break
                        
                        # If none of the values have a frequency of 1, it will
                        # find the next lowest frequency.
                        while not discard_value:
                            for key in tally:
                                if tally[key] == lowestcard + 1:
                                    discard_value = key
                            lowestcard += 1
                                    
                            
                        for card in temporary_cards:
                            if card[1] == discard_value:
                                return (5, card)
                            
                    # If it's phase 3 or 6, it will discard the card with 
                    # the lowest value.
                    elif phase_status[player_id] + 1 == 3 or \
                        phase_status[player_id] + 1 == 6:
                        
                        # This variable holds the card with the lowest value.
                        lowest_card = ''
                        # This variable holds the value of the lowest card.
                        # (It's currently 14 as the highest card value is 13) 
                        lowest_point = 14
                        
                        # If there is an ace in our hand, it will be discarded.
                        for card in hand:
                            if card[0] == 'A':
                                return (5, card)
                            
                        # This will find the lowest possible card
                        if temporary_cards:  
                            for card in temporary_cards:
                                if convert_cards(card) < lowest_point:
                                    lowest_card = card
                                    lowest_point = convert_cards(card)
                            return (5, lowest_card)
                        else:
                            for card in hand:
                                if convert_cards(card) < lowest_point:
                                    lowest_card = card
                                    lowest_point = convert_cards(card)
                            return (5, lowest_card)
                            
                    # If it's phase 5, it will discard any duplicates.
                    # If there aren't any it will discard the card with
                    # the highest value.
                    elif phase_status[player_id] + 1 == 5:
                        # This variable will hold the suit with the lowest 
                        # frequency.
                        discard_value = 0
                        tally = {}
                        # This variable holds the value of the highest card.
                        highestpoint = 0
                        
                        # This will count the frequency of the cards' values.
                        for card in temporary_cards:
                            if card[0] in tally:
                                tally[card[0]] += 1
                            else:
                                tally[card[0]] = 1
                        
                        # This will discard duplicates.
                        for key in tally:
                            if tally[key] > 1:
                                discard_value = key
                                break
                        
                        # If there aren't any duplicates, it will discard 
                        # the highest value card.
                        if not discard_value:
                                for card in temporary_cards:
                                    if convert_cards(card[0]) > highestpoint:
                                        highestpoint = convert_cards(card[0])
                                        discard_value = card[0]

                        for card in temporary_cards:
                            if card[0] == discard_value:
                                return (5, card)
                    
                    # If it's phase 7, it will discard depending on the 
                    # group we currently have.
                    elif phase_status[player_id] + 1 == 7:
                        if current_groups_in_hand[0]:
                            if 3 in phazed_group_type(current_groups_in_hand[0]
                                                      [0]):
                                # If the group is a same value group, 
                                # it will discard duplicates for the run.
                                
                                # This variable will hold the suit with the 
                                # lowest frequency.
                                discard_value = 0
                                tally = {}
                                
                                # This will count the frequency of the values.
                                for card in temporary_cards:
                                    if card[0] in tally:
                                        tally[card[0]] += 1
                                    else:
                                        tally[card[0]] = 1
                                
                                # It will then discard duplicates. 
                                for key in tally:
                                    if tally[key] > 1:
                                        discard_value = key
                                        break
                                
                                highestpoint = 0
                                # If there aren't any duplicates, it will
                                # discard the highest value card.
                                if not discard_value:
                                    for card in temporary_cards:
                                        if convert_cards(card[0]) > \
                                            highestpoint:
                                            highestpoint = convert_cards(
                                                card[0])
                                            discard_value = card[0]

                                
                                for card in temporary_cards:
                                    if card[0] == discard_value:
                                        return (5, card)
                                
                            elif 3 not in phazed_group_type(
                                current_groups_in_hand[0][0]):
                                # This variable will hold the suit with the 
                                # lowest frequency.
                                discard_value = ''
                                tally = {}
                                # This will count the frequency of the values.
                                for card in temporary_cards:
                                    if card[0] in tally:
                                        tally[card[0]] += 1
                                    else:
                                        tally[card[0]] = 1 
                                        
                                # It will then discard the card with the 
                                # lowest frequency.
                                lowestcard = 1       
                                for key in tally:
                                    if tally[key] == lowestcard:
                                        discard_value = key
                                        break       
                                while not discard_value:
                                    for key in tally:
                                        if tally[key] == lowestcard + 1:
                                            discard_value = key
                                    lowestcard += 1
                                
                                for card in temporary_cards:
                                    if card[0] == discard_value:
                                        return (5, card)
                        else:
                            # If no groups are formed yet, it will discard 
                            # duplicates.
                            
                            # This variable will hold the suit with the lowest 
                            # frequency.
                            discard_value = 0
                            tally = {}
                            # This will count the frequency of the values.
                            for card in temporary_cards:
                                if card[0] in tally:
                                    tally[card[0]] += 1
                                else:
                                    tally[card[0]] = 1
                            
                            # It will then discard duplicates.
                            for key in tally:
                                if tally[key] > 1:
                                    discard_value = key
                                    break
                           
                            highestpoint = 0
                            
                            # If there are no duplicates, it will discard
                            # the card with the highest value.
                            if not discard_value:
                                for card in temporary_cards:
                                    if convert_cards(card[0]) > highestpoint:
                                        highestpoint = convert_cards(card[0])
                                        discard_value = card[0]

                            for card in temporary_cards:
                                if card[0] == discard_value:
                                    return (5, card)

                                                       
        else:
            # Since this is the first turn too, it will repeat the process
            # of lines 955-1119
            if current_groups_in_hand[1] is False:
                # If it's our first play and we can't place any phases,
                # we find out whether we should take from the discard pile
                # or the deck.
                hand.append(discard)
                new_groups_in_hand = calculating_phase(
                    hand, phase_status[player_id] + 1)

                # This variable holds the status of whether the group we're
                # planning on playing has an ace or not.
                aceavailable = False

                # This will check if the group has an ace or not.
                if current_groups_in_hand[0]:
                    for card in current_groups_in_hand[0][0]:
                        if card[0] == 'A':
                            aceavailable = True
                            break

                if aceavailable is True:
                    # If there is an ace, it will check if the card 
                    # from the discard pile can replace the ace.
                    if current_groups_in_hand[0] != new_groups_in_hand[0]:
                        return (2, discard)

                # Then we check if the discard pile card can complete
                # the phase.
                if len(new_groups_in_hand[0]) > \
                    len(current_groups_in_hand[0]):
                    return (2, discard)
                else:
                    # If not, it will check again if the discard can help
                    # in getting another group.
                    hand.pop(-1)

                    # This variable holds all the other cards beside
                    # the cards that have already formed a group.
                    temporary_cards = []

                    # We first find the remaining cards that have not
                    # formed a group.
                    if current_groups_in_hand[0]:
                        temporary_cards = [card for card in remainder]    
                        for card in remainder:
                            if card in current_groups_in_hand[0][0]:
                                temporary_cards.remove(card)   
                    else:
                        temporary_cards = [card for card in remainder]

                    # If the discard pile card is an ace and our
                    # phase status isn't 3 or 6 (accumulations), it will
                    # take it.
                    if phase_status[player_id] + 1 != 3 or \
                        phase_status[player_id] + 1 != 6:
                        if discard[0] == 'A':
                                return (2, discard)

                    # If our current phase status is 1, and if the discard
                    # card pile helps increase the frequency of the value,
                    # the card from the discard pile will be taken.
                    if phase_status[player_id] + 1 == 1:  
                        tally = {}
                        # This will count the frequency of the values.
                        for card in temporary_cards:
                            if card[0] in tally:
                                tally[card[0]] += 1
                            else:
                                tally[card[0]] = 1

                        # It will then check if the discard card pile 
                        # is in the tally but it will prioritize the
                        # cards with the highest frequency first.
                        for key in tally:
                            if tally[key] == 2:
                                if discard[0] == key:
                                    return (2, discard)

                        if discard[0] in tally:
                            return (2, discard)
                        else:
                            return (1, None)

                    # If it's phase 2, if the discard pile card matches
                    # the card suit with the highest frequency, it will
                    # take the card from the discard pile.
                    elif phase_status[player_id] + 1 == 2:
                        tally = {}
                        # This counts the frequency of the suits.
                        for card in temporary_cards:
                            if card[1] in tally:
                                tally[card[1]] += 1
                            else:
                                tally[card[1]] = 1

                        # This variable holds the suit with the highest
                        # frequency.
                        highestsuit = ''
                        # This variable holds the frequency of the 
                        # highest suit.
                        highsuitwithpoints = 0

                        # It will then check if the discard card pile 
                        # is in the tally but it will prioritize the
                        # cards with the highest frequency first.
                        for key in tally:
                            if tally[key] > highsuitwithpoints:
                                highsuitwithpoints = tally[key]
                                highestsuit = key

                        if discard[1] == highestsuit:
                            return (2, discard)
                        else:
                            return (1, None)

                    # If the phase is 4, it will check if the discard
                    # card pile helps increase the frequency of the value,
                    # the card from the discard pile will be taken.
                    elif phase_status[player_id] + 1 == 4:
                        tally = {}
                        # This counts up the frequency of the cards'
                        # values. 
                        for card in temporary_cards:
                            if card[0] in tally:
                                tally[card[0]] += 1
                            else:
                                tally[card[0]] = 1

                        # It will then check if the discard card pile 
                        # is in the tally but it will prioritize the
                        # cards with the highest frequency first.
                        for key in tally:
                            if tally[key] == 3:
                                if discard[0] == key:
                                    return (2, discard)

                        for key in tally:
                            if tally[key] == 2:
                                if discard[0] == key:
                                    return (2, discard) 

                        if discard[0] in tally:
                            return (2, discard)
                        else:
                            return (1, None)

                    # If it's none of the phases above,it will simply
                    # just take a card from the deck.
                    return (1, None)
            else:
                # If it's still the first turn and we have a phase in our
                # hand, it will check if we can put the discard card 
                # anywhere on the table. If so, it will take the 
                # discard card.
                if group_validity(discard, table, hand)[0] is True:
                    return (2, discard)
                else:
                    # If not, we check if the discard card can be added
                    # to the phase in our hand.
                    if groupvalidity_forphase(discard, 
                                              current_groups_in_hand[0], 
                                              phase_status[player_id] + 1,
                                              hand) is True:
                        return (2, discard)
                    else:
                        return (1, None)
          
    else:
        
        if turn_history:
            if player_id not in turn_history[-1]:
                # If the phase has already been completed and it's the first
                # turn, it will check if the card on discard pile can be 
                # placed anywhere on the table.
                if group_validity(discard, table, hand)[0] is True:
                    return (2, discard)
                else:
                    return (1, None)
            else:
                # If it's not the first turn, it will check if any of 
                # the cards in our hand can be placed down on the table.
                for card in hand:
                    if group_validity(card, table, hand)[0] is True:
                        return (4, (card, (group_validity(card, 
                                                          table, hand)[1], 
                                           group_validity(card, 
                                                          table, hand)[2], 
                                           group_validity(card, 
                                                          table, hand)[3])))
                    
                    
                # If not, it will discard the card with the 
                # highest value.
                mostpoints_inhand = 0
                mostpoints_card = ''
                for card in hand:
                    if card[0] == 'A':
                        return (5, card)
                    elif convert_cards(card[0]) > mostpoints_inhand:
                        mostpoints_inhand = convert_cards(card[0])
                        mostpoints_card = card
                return (5, mostpoints_card)
                   
        else:
            # Since this is also the first turn, it repeats the process in line
            # 1566-1569
            if group_validity(discard, table)[0] is True:
                return (2, discard)
            else:
                return (1, None)
                    

  
if __name__ == '__main__':
    # Example call to the function.
    
    print(phazed_play(1, [(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C',
      '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'),
      (5, 'JS')]), (1, [(2, 'JS'), (3, (5, [['2C', '3H', '4D', 'AD', '6S',
      '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS',
      (1, 0, 9)))])], [0, 5, 0, 0], ['QD', 'KD'], '7H'))
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing=True


# In[2]:


class cards:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    def __str__(self):
        return self.rank+" of "+self.suit


# In[3]:


class deck:
     def __init__(self):
            self.deck=[]
            for i in suits:
                for j in ranks:
                    self.deck.append(cards(i,j))
    
     def __str__(self):
            deck_comp=''
            for i in self.deck:
                deck_comp=deck_comp+i.__str__()+"\n"
            return 'The deck has : \n'+deck_comp
    
     def shuffle(self):
        random.shuffle(self.deck)
        
     def deal(self):
         return self.deck.pop()
    


# In[4]:


d=deck()


# In[5]:


print(d)


# In[6]:


class Hand:
    def __init__(self):
        self.cards=[]
        self.value=0
        self.aces=0
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
    def adjust(self):
        while self.value>21 and self.aces:
            self.value-=10
            self.aces-=1


# In[7]:


test_deck=deck()
test_deck.shuffle()
test_player=Hand()

pull=test_deck.deal()
print(pull)
test_player.add_card(pull)
print(test_player.value)


# In[8]:


class chips:
    def __init__(self,tot=100):
        self.tot=tot
        self.bet=0
    def win(self):
        self.tot+=self.bet
    def lose(self):
        self.tot-=self.bet


# In[9]:


def takebet(chips):
    while True:
        try:
            chips.bet=int(input('How many chips you want to bet'))
        except:
            print('Sorry enter integer')
        else:
            if(chips.bet>chips.tot):
                print(f'sorry!! cant take bet as you have {chips.tot}')
            else:
                break;


# In[10]:


def hit(deck,hand):
    card=deck.deal()
    hand.add_card(card)
    hand.adjust()


# In[11]:


def hit_or_stand(deck,hand):
    global playing
    while True:
        x=input('Enter your choice hit or stand as h or s ')
        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print('Player stands')
            playing=False
        else:
            print('Sorry! Didnt get that')
        break


# In[12]:


def show_some(player,dealer):
    print('\nDealers hand :')
    print('\nFirst Card hidden ')
    print(dealer.cards[1])
    print('\nplayers cards :')
    for i in player.cards:
        print(i)
    
def show_all(player,dealer):
    print('\nDealer hand : ')
    for i in dealer.cards:
        print(i)
    print(f'dealers hand : {dealer.value}')
    print('\nPlayers hand')
    for j in player.cards:
        print(j)
    print(f'player hand : {player.value}')


# In[13]:


def player_wins(dealer,player,chips):
    print('player wins')
    chips.win()
    
def player_busts(dealer,player,chips):
    print('player loses')
    chips.lose()
    
def dealer_wins(dealer,player,chips):
    print('dealer wins')
    chips.lose()
    
def dealer_busts(dealer,player,chips):
    print('dealer loses')
    chips.win()

def push(dealer,player):
    print('player and dealer tie')


# In[16]:


playing=True
con=True
while con:
    Deck=deck()
    Deck.shuffle()
    player_hand=Hand()
    player_hand.add_card(Deck.deal())
    player_hand.add_card(Deck.deal())
    dealer_hand=Hand()
    dealer_hand.add_card(Deck.deal())
    dealer_hand.add_card(Deck.deal())
    player_chip=chips()
    takebet(player_chip)
    show_some(player_hand,dealer_hand)
    while playing:
        hit_or_stand(Deck,player_hand)
        show_some(player_hand,dealer_hand)
        if player_hand.value>21:
            player_busts(dealer_hand,player_hand,player_chip)
            break
    if player_hand.value<=21:
        while dealer_hand.value<player_hand.value:
            hit(Deck,dealer_hand)
        show_all(player_hand,dealer_hand)
        if dealer_hand.value>21:
            dealer_busts(dealer_hand,player_hand,player_chip)
        elif dealer_hand.value>player_hand.value:
            dealer_wins(dealer_hand,player_hand,player_chip)
        elif dealer_hand<player_hand:
            player_wins(dealer_hand,player_hand,player_chip)
        else:
            push(dealer_hand,player_hand)
    print(f'\n player total chip : {player_chip.tot}')
    while True:
        x=input('Enter your choice to continue as Y or N ')
        if x[0].lower()=='y':
            con=True
        elif x[0].lower()=='n':
            print('Thank you')
            con=False
            break;
        else:
            print('Sorry! Didnt get that')
        break


# In[ ]:





# In[ ]:





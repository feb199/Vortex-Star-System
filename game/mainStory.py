import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.console import clear

from classes.ship import Ship
from classes.event import Event, EventOption

from game.story.backstory import backstory
from game.story.endgame import endgame



story1Content = "The crew are on the way to another planet when they are suddenly attacked by aliens What should the crew do?"
story1Options = [
    EventOption("Fire Ships Weapons", "The ship uses its main weapon."),
    EventOption("Try to communicate", "You attempt to communicate with the aliens it appears they don't understand you.")
]
def story1(): return Event("Attacked By Alien", story1Options, story1Content)


desertPlanetContent = """You land on this new planet and discovered it's a desert planet,
there appear to be only a few lakes here and there, and there doesn't seem to be much life,
except for tents, your crew goes over to one of them, maybe the occupiers are friendly?

You go over to the tents and something doesn't feel right and then it hits you you've been ambushed."""
desertPlanetOptions = [
    EventOption("Draw your weapons", "You draw your weapons and this doesn't end well, they are all stronger than you."),
    EventOption("Reason with them", """You reason with the group and explain how you're lost, the group reason with you and apologise for the misunderstanding.
You ask them if they'd like to join your crew and they accept.""")
]
def desertPlanetEvent(): return Event("Suspicious Tents", desertPlanetOptions, desertPlanetContent)


metalPlanetContent = """We land on what appears to be a metallic planet,
absolutely everything is metal, metal buildings, metal trees, metal animals, even the ground is metal,
you encounter a metal resident who notices that your crew are not metallic and so must not be from the planet."""
metalPlanetOptions = [
    EventOption("Flee", "You attempt to flee and the metal residents give you a weird look while tilting their heads."),
    EventOption("Confront", """You confront the metal residents and they appear to be very helpful but also curious about you,
they also have some parts that you can use to upgrade the ship and give it the ability to translate alien language.
They appear to be very happy giving you the parts, you ask them if they'd like to join you and they politely decline.""")
]
def metalPlanetEvent(): return Event("Metal Residents", metalPlanetOptions, metalPlanetContent)


greenPlanetContent = """You land on a green planet, rich in flora, but almost no fauna, the place is beautiful,
like something off a postcard or something, your crew want to take pictures of the amazing scenery,
but as they look for cameras they hear someone calling for help, it seems a group of locals have been poisoned by some of the plants,
maybe this isn't so beautiful, perhaps see if you can help them?

You go over to the group and ask them what happened and the group explain to you they were looking at some of the flowers
when one of them sprayed spores all over the group and poisoned them in the process,
you ask the group if you can help in any way they reply with they don't know but something about this seems familiar to you.
You gather your crew and explain to them you've seen this before and think you know how to help so you ask the crew to gather
some ingredients which are: dott leaves, flower nectar and a leaf from nettles.
You tell the crew to be careful while they look for the ingredients and you stay behind with the group.

An hour passes and your crew haven't returned and you start to get worried."""
greenPlanetOptions = [
    EventOption("Stay with the group", "You stay with the group and hope your crew return but unfortunately, they don't, you lost them."),
    EventOption("Find your crew", """You decide to go and find your crew when you suddenly see them being attacked by giant flower monsters,
you draw your weapon and attack the monster setting your crew free and you all run back to the group with the ingredients.
You make the antidote for the group and they all immediately start to feel better, they thank you.""")
]
def greenPlanetEvent(): return Event("Infection", greenPlanetOptions, greenPlanetContent)


oceanPlanetContent = """You land on an ocean planet, almost entirely covered with an ocean of strange purple liquid,
except for a few scattered islands, this means your crew can at least come out and have a look.
Your crew thinks that maybe the purple ocean is just water with something in it, that gives it a purple could,
but after analysis, it appears to be a mixture of several unknown chemicals, suddenly you see a creature come out of the water,
it sees you and starts to come towards your island."""
oceanPlanetOptions = [
    EventOption("Shoot at it", """You raise your weapons and the creature flops on your island and is completely friendly
so you lower your weapons and adventure around the island, there appears to be no relics on this planet
so you and your crew just take in all the scenery, there also appears to be no hostages on this planet either
but there are broken parts that you can use to upgrade and fix the ship."""),
    EventOption("Flee", """You and your crew start to run as the creature flops on your island but you soon realise it's
completely friendly so you lower your weapons and adventure around the island, there appears to be no relics on this planet
so you and your crew just take in all the scenery, there also appears to be no hostages on this planet either
but there are broken parts that you can use to upgrade and fix the ship.""")
]
def oceanPlanetEvent(): return Event("Creature", oceanPlanetOptions, oceanPlanetContent)


icyPlanetContent = """You land on an icy planet, and it's extremely cold, however, your crew finds a cave to take shelter,
and it's quite warm inside, but noise is heard deep within the cave, it seems the crew are not alone."""
icyPlanetOptions = [
    EventOption("Leave", """You and your crew leave and go back to the ship"""),
    EventOption("Stay and investigate", """You stay and find out what made the noise and it turns out you've stumbled into a Polar bear's home and it doesn't seem happy,
you run out of the cave and all of a sudden you see spears flying at you, you duck and it gets the polar bear the bear lets out a growl and retreats to it's a cave.
It appears you have been saved by the cavemen and they offer their hands out to help you all stand,
you thank them and they smile at you they ask you if you lost and you say yes and that you're trying to get home.

They offer to help in any way possible and you simply say you're looking for parts to help rebuild and upgrade your ship,
the cavemen say we have some parts here that might be of use to you follow us and we'll show you.
You follow them and they have a big cave that looks to be their home,
they say right here and they have a box filled with relics and other parts, take them all the men say.
You thank them and they follow you to your ship, you ask them if they'd like to join you and they accept.""")
]
def icyPlanetEvent(): return Event("Polar Bear", icyPlanetOptions, icyPlanetContent)


def story():
    if Ship.player is None: return [ False, None, "No Player" ]
    ship = Ship.player
    
    clear()
    backstory(ship)
    # clear()

def endGameStory():
    if Ship.player is None: return [ False, None, "No Player" ]
    ship = Ship.player
    
    clear()
    endgame(ship)
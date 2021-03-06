from typing import List

from .token import Token

PHRASAL_VERBS_ = {
    "abide by", "account for", "ache for", "act on", "act out", "act up", "act upon", "add on", "add up", "add up to",
    "agree with", "aim at", "allow for", "allow of", "amount to", "amp up", "angle for", "answer back", "answer for",
    "argue down", "argue out", "ask about", "ask after", "ask around", "ask for", "ask in", "ask out", "ask over",
    "ask round", "auction off", "back away", "back down", "back into", "back off", "back out", "back out of", "back up",
    "bag out", "bail out", "bail out of", "bail out on", "bail up", "ball up", "balls up", "bang about", "bang around",
    "bang on", "bang on about", "bang out", "bang up", "bank on", "bargain down", "bargain for", "bargain on",
    "barge in", "barge into", "bash about", "bash in", "bash out", "bash up", "bawl out", "be after", "be along",
    "be away", "be carried away", "be cut out for", "be cut up", "be down", "be down on", "be down with", "be fed up",
    "be in", "be in on", "be into", "be not on", "be off", "be on", "be on about", "be onto", "be out", "be out of",
    "be out to", "be snowed under", "be taken aback", "be taken in", "be taken with", "be to do with", "be up",
    "be up for", "be up to", "beam up", "bear down on", "bear on", "bear out", "bear up", "bear up under", "bear with",
    "beat down", "beat out", "beat up", "beaver away", "beaver away at", "bed down", "bed out", "beef up", "belong to",
    "belong with", "belt out", "belt up", "bend down", "bend over", "bend over backwards", "big up", "bitch up",
    "black out", "blank out", "blare out", "blast off", "blaze away", "bleed out", "bliss out", "block in", "block off",
    "block out", "block up", "blow away", "blow down", "blow in", "blow off", "blow out", "blow over", "blow through",
    "blow up", "blurt out", "board out", "board up", "bog down", "bog in", "bog into", "bog off", "boil down",
    "boil down to", "boil over", "boil up", "bolster up", "bone up", "bone up on", "book in", "book into", "book out",
    "book up", "boot up", "border on", "boss about", "boss around", "botch up", "bottle away", "bottle out",
    "bottle up", "bottom out", "bounce back", "bounce into", "bounce off", "bow down to", "bow out", "bow to",
    "bowl out", "bowl over", "box in", "box up", "brace up", "branch out", "break away", "break down", "break for",
    "break in", "break into", "break off", "break out", "break out in", "break out of", "break through", "break up",
    "breed out", "breeze along", "breeze in", "breeze into", "breeze through", "brick in", "brick up", "brighten up",
    "bring about", "bring along", "bring around", "bring back", "bring down", "bring forth", "bring forward",
    "bring in", "bring off", "bring on", "bring out", "bring out in", "bring round", "bring up", "brush off",
    "brush up", "bubble over", "buck up", "bucket down", "buckle down", "buckle under", "buckle up", "budge up",
    "buff up", "buff up on", "bug off", "bug out", "build around", "build in", "build into", "build on", "build up",
    "bulk out", "bulk up", "bump into", "bump off", "bump up", "bundle off", "bundle out", "bundle up", "bunk off",
    "buoy up", "burn down", "burn off", "burn out", "burn up", "burst in", "burst into", "burst out", "bust up",
    "butt in", "butt out", "butter up", "button up", "buy in", "buy into", "buy off", "buy out", "buy up",
    "buzz around", "buzz off", "call after", "call around", "call at", "call back", "call for", "call forth", "call in",
    "call off", "call on", "call out", "call round", "call up", "calm down", "cancel out", "cap off", "care for",
    "carried away", "carry forward", "carry off", "carry on", "carry on with", "carry out", "carry over",
    "carry through", "cart off", "carve out", "carve up", "cash in", "cash in on", "cash out", "cash up",
    "cast about for", "cast around for", "cast aside", "cast off", "cast out", "cast round for", "cast up", "catch at",
    "catch on", "catch out", "catch up", "catch up in", "catch up on", "catch up with", "cater for", "cater to",
    "cave in", "chalk out", "chalk up", "chalk up to", "chance upon", "change over", "charge up", "charge with",
    "chase down", "chase off", "chase up", "chat away", "chat up", "cheat on", "cheat out of", "check by", "check in",
    "check into", "check off", "check on", "check out", "check out of", "check over", "check up on", "cheer on",
    "cheer up", "chew off", "chew on", "chew out", "chew over", "chew up", "chicken out", "chill out", "chime in",
    "chip away at", "chip in", "choke off", "choke out", "choke up", "choose up", "chop down", "chop up", "chow down",
    "chow down on", "chuck away", "chuck in", "chuck out", "chuck up", "churn out", "clag up", "clam up",
    "clamp down on", "claw back", "clean off", "clean out", "clean up", "clear away", "clear off", "clear out",
    "clear up", "click through", "climb down", "cling on", "cling on to", "cling to", "clock in", "clock off",
    "clock on", "clock out", "clock up", "clog up", "close down", "close in", "close in on", "close in upon",
    "close off", "close on", "close out", "close up", "cloud over", "clown about", "clown around", "coast along",
    "cobble together", "cock up", "colour (color) in", "colour (color) up", "come about", "come across", "come along",
    "come apart", "come around", "come around to", "come back", "come before", "come by", "come down", "come down on",
    "come down to", "come down upon", "come down with", "come forth", "come forth with", "come from", "come in",
    "come in for", "come into", "come into use", "come off", "come off it", "come on", "come out", "come out in",
    "come out of", "come out with", "come over", "come round", "come through", "come through with", "come to",
    "come up", "come up against", "come up with", "come upon", "cone off", "conjure up", "conk out", "contract in",
    "contract out", "contract out of", "cool down", "cool off", "coop up", "cop it", "cop off", "cop out", "cost up",
    "cotton on", "cotton up to", "cough up", "could do with", "count against", "count among", "count down", "count for",
    "count in", "count off", "count on", "count out", "count towards", "count up", "count upon", "cover for",
    "cover up", "cowboy up", "cozy up", "cozy up to", "crack down on", "crack on", "crack up", "crank out", "crank up",
    "crash out", "cream off", "creep in", "creep into", "creep out", "creep out on", "creep over", "creep up on",
    "crop up", "cross off", "cross out", "cross up", "cruise through", "crumb down", "cry off", "cry out", "cuddle up",
    "cuddle up to", "cut across", "cut back", "cut back on", "cut down", "cut down on", "cut in", "cut it out",
    "cut off", "cut out", "cut out on", "cut through", "cut up", "damp down", "damp off", "dash down", "dash off",
    "dawn on", "deal in", "deal with", "decide on", "decide upon", "deck out", "dial in", "dial into", "dial up",
    "die away", "die back", "die down", "die for", "die off", "die on", "die out", "dig in", "dig into", "dig out",
    "dig up", "dime out", "dine out", "dine out on", "dip in", "dip into", "dip out", "disagree with", "dish out",
    "dish up", "dive in", "dive into", "divide up", "divvy out", "divvy up", "do away with", "do in", "do out of",
    "do over", "do up", "do with", "do without", "dob in", "dole out", "doss about", "doss around", "doss down",
    "double as", "double back", "double down", "double down on", "double over", "double up", "double up as", "doze off",
    "drag on", "draw back", "draw down", "draw even", "draw in", "draw into", "draw on", "draw out", "draw up",
    "draw upon", "dream of", "dream up", "dredge up", "dress down", "dress up", "drift apart", "drift off",
    "drill down", "drill down through", "drill into", "drink up", "drive away", "drive back", "drive by", "drive off",
    "drive out", "drive up", "drone on", "drop around", "drop away", "drop back", "drop behind", "drop by", "drop in",
    "drop off", "drop out", "drop over", "drop round", "drop someone in it", "drop through", "drown in", "drown out",
    "drum into", "drum out", "drum up", "dry off", "dry out", "dry up", "duck out of", "duff up", "dumb down",
    "dump on", "dust down", "dust off", "dwell on", "dwell upon", "ease off", "ease up", "eat away", "eat in",
    "eat into", "eat out", "eat up", "ebb away", "edge out", "edge up", "egg on", "eke out", "embark on", "embark upon",
    "empty out", "end in", "end up", "end up with", "enter for", "enter into", "eye up", "face off", "face up to",
    "faff about", "faff around", "fall about", "fall apart", "fall back", "fall back on", "fall behind", "fall down",
    "fall for", "fall in", "fall into", "fall off", "fall out", "fall over", "fall through", "fall under", "farm out",
    "fart about", "fart around", "fasten down", "fasten on", "fasten onto", "fasten up", "fathom out", "fatten up",
    "fawn on", "fawn over", "feed off", "feed on", "feed up", "feel up", "feel up to", "fence in", "fence off",
    "fend for", "fend off", "ferret about", "ferret around", "ferret out", "fess up", "fess up to", "fetch up",
    "fiddle about", "fiddle around", "fiddle away", "fight back", "fight it out", "fight off", "figure on",
    "figure out", "file away", "file for", "fill in", "fill in for", "fill in on", "fill out", "fill up", "filter in",
    "filter out", "find out", "finish off", "finish up", "finish up with", "finish with", "fink on", "fink out",
    "fire away", "fire off", "fire up", "firm up", "fish for", "fish out", "fit in", "fit in with", "fit into",
    "fit out", "fit out with", "fit up", "fix up", "fizzle out", "flag down", "flag up", "flake out", "flame out",
    "flame up", "flare out", "flare up", "flash about", "flash around", "flash back", "flash by", "flash past",
    "flesh out", "flick over", "flick through", "flip off", "flip out", "flip through", "float about", "float around",
    "flog off", "floor it", "flounce off", "flounce out", "fluff out", "fluff up", "fly about", "fly around", "fly at",
    "fly by", "fly into", "fob off", "fob off on", "fob off onto", "fob off with", "focus on", "fold up", "follow on",
    "follow on from", "follow through", "follow up", "fool about", "fool around", "fool with", "forge ahead",
    "fork out", "fork over", "freak out", "free up", "freeze out", "freeze over", "freeze up", "freshen up",
    "frighten away", "frighten off", "fritter away", "front for", "front off", "front onto", "front out", "front up",
    "frown on", "fuel up", "gad about", "gad around", "gag for", "gang up", "gang up against", "gang up on", "gear to",
    "gear towards", "gear up", "gee up", "geek out", "get about", "get above", "get across", "get across to",
    "get after", "get ahead", "get ahead of", "get along", "get along in", "get along with", "get around",
    "get around to", "get at", "get away", "get away from", "get away with", "get back", "get back at", "get back into",
    "get back to", "get back together", "get behind", "get behind with", "get by", "get by on", "get by with",
    "get down", "get down on", "get down to", "get in", "get in on", "get in with", "get into", "get it", "get it off",
    "get it off with", "get it on", "get it on with", "get it together", "get it up", "get off", "get off it",
    "get off on", "get off with", "get on", "get on at", "get on for", "get on to", "get on with", "get onto",
    "get out", "get out of", "get over", "get over with", "get round", "get round (around) to", "get round (or around)",
    "get round to", "get through", "get through to", "get to", "get together", "get up", "get up to", "ghost away",
    "gin up", "ginger up", "give away", "give back", "give in", "give in to", "give it to", "give it up for",
    "give it up to", "give of", "give off", "give onto", "give out", "give out to", "give over", "give over to",
    "give up", "give up on", "give up to", "give way", "give way to", "give yourself up", "give yourself up to",
    "gloss over", "gnaw at", "gnaw away at", "go about", "go across", "go after", "go against", "go ahead",
    "go ahead with", "go along with", "go around", "go at", "go away", "go back", "go back on", "go before", "go below",
    "go by", "go down", "go down on", "go down to", "go down with", "go for", "go for it", "go forth", "go forward",
    "go in", "go in for", "go in with", "go into", "go it", "go it alone", "go off", "go off with", "go on",
    "go on about", "go on at", "go on to", "go on with", "go one", "go out", "go out for", "go out to", "go out with",
    "go over", "go over to", "go past", "go round", "go through", "go through with", "go to", "go together",
    "go towards", "go under", "go up", "go up to", "go with", "go without", "goof around", "goof off", "goof on",
    "goof up", "grasp at", "grass on", "grass up", "grey out", "grind away", "grind down", "grind into", "grind on",
    "grind out", "grind up", "grow apart", "grow away from", "grow back", "grow from", "grow into", "grow on",
    "grow out", "grow out of", "grow to", "grow together", "grow up", "grow up on", "grow upon", "gun for", "gussy up",
    "hack around", "hack into", "hack off", "hack up", "ham up", "hammer away at", "hammer into", "hammer out",
    "hand back", "hand down", "hand in", "hand on", "hand out", "hand over", "hang about", "hang around", "hang back",
    "hang back from", "hang in there", "hang it up", "hang on", "hang onto", "hang out", "hang out for", "hang over",
    "hang together", "hang up", "hang up on", "hang with", "hanker after", "hanker for", "harp on", "hash out",
    "hash up", "hate on", "have against", "have around", "have down as", "have in", "have it away", "have it in for",
    "have it off", "have it out with", "have off", "have on", "have over", "have round", "have up", "head for",
    "head off", "head out", "head up", "hear about", "hear from", "hear of", "hear out", "heat up", "help out",
    "hem in", "hew to", "hide away", "hide out", "hinge on", "hinge upon", "hit back", "hit for", "hit it off",
    "hit it off with", "hit on", "hit out at", "hit up", "hit up on", "hit upon", "hit with", "hive off",
    "hold against", "hold back", "hold back from", "hold down", "hold forth", "hold off", "hold off on", "hold on",
    "hold on to", "hold onto", "hold out", "hold out against", "hold out for", "hold out on", "hold over", "hold to",
    "hold together", "hold up", "hold with", "hole up", "hollow out", "home in on", "hone in on", "hook into",
    "hook up", "hook up to", "hoon around", "hop in", "hop it", "hop on", "hop out", "horse around", "hose down",
    "hound out", "hover around", "hunker down", "hunt down", "hunt out", "hunt up", "hush up", "hutch up", "ice over",
    "ice up", "iron out", "issue forth", "jabber away", "jack around", "jack in", "jack up", "jam on", "jaw away",
    "jazz up", "jerk around", "jerk off", "jockey into", "jog along", "jog on", "join in", "joke around", "jot down",
    "juice up", "jump at", "jump in", "jump off", "jump on", "keel over", "keep around", "keep at", "keep away",
    "keep back", "keep down", "keep from", "keep in", "keep in with", "keep off", "keep on", "keep out", "keep to",
    "keep up", "keep up at", "keep up with", "key down", "key in", "key in on", "key on", "key to", "key up",
    "kick about", "kick around", "kick around with", "kick back", "kick down", "kick in", "kick off", "kick out",
    "kick up", "kill off", "kip down", "kip down on", "kiss off", "kiss up to", "knock about", "knock around",
    "knock back", "knock down", "knock it off", "knock off", "knock out", "knock over", "knock together", "knock up",
    "knuckle down", "knuckle under", "land in", "land up in", "land with", "lap up", "large it up", "lark about",
    "lark around", "lark it up", "lash down", "lash into", "lash out", "lash out against", "lash out at", "lash out on",
    "latch on", "latch on to", "latch onto", "laugh off", "lay down", "lay into", "lay off", "lay on", "lay out",
    "lead on", "lead to", "leak out", "lean on", "leap at", "leap on", "leap out at", "leap upon", "leave on",
    "leave out", "let down", "let in", "let in on", "let off", "let on", "let out", "level off", "level out",
    "level up", "level with", "lie around", "lie down", "lie with", "lift off", "light out", "light up", "lighten up",
    "limber up", "limber up for", "line up", "link up", "link up with", "listen out for", "listen up", "live by",
    "live down", "live for", "live in", "live it up", "live off", "live on", "live out", "live through",
    "live together", "live up to", "live with", "liven up", "load down", "load up", "load up on", "lock away",
    "lock down", "lock in", "lock onto", "lock out", "lock up", "lock yourself away", "log in", "log into", "log off",
    "log on", "log out", "look after", "look at", "look back", "look down on", "look for", "look forward to", "look in",
    "look in on", "look into", "look on", "look on as", "look out", "look out for", "look over", "look round",
    "look through", "look to", "look up", "look up to", "look upon as", "loose off", "loose on", "loose upon",
    "loosen up", "lord it over", "lose out", "lose out on", "lose out to", "luck into", "luck out", "lust after",
    "magic away", "make after", "make away with", "make do with", "make for", "make into", "make it", "make it up to",
    "make of", "make off", "make off with", "make out", "make over", "make towards", "make up", "make up for",
    "make up to", "make with", "man down", "man up", "mark down", "mark down as", "mark off", "mark out",
    "mark out for", "mark out from", "mark up", "marry in", "marry off", "marry out", "marry up", "mash up", "max out",
    "measure against", "measure off", "measure out", "measure up", "measure up to", "meet up", "meet up with",
    "meet with", "melt down", "mess about", "mess about with", "mess around", "mess around with", "mess over",
    "mess up", "mess with", "mete out", "mill around", "miss out", "miss out on", "mix up", "mix with", "mock up",
    "moggy off", "monkey around", "mooch about", "mooch around", "mop up", "mope about", "mope around", "mount up",
    "mouth off", "move ahead", "move along", "move away", "move away from", "move down", "move in", "move in on",
    "move into", "move on", "move out", "move towards", "move up", "muddle along", "muddle through", "muddle up",
    "mug up", "mug up on", "mull over", "muscle in", "muscle in on", "muscle into", "muscle out", "naff off", "nag at",
    "nail down", "name after", "narrow down", "nerd out", "nip off", "nip out", "nod off", "nod through", "nose about",
    "nose around", "nose out", "note down", "nut out", "nuzzle up", "nuzzle up to", "occur to", "open up", "operate on",
    "opt for", "opt in", "opt into", "opt out", "order about", "order around", "order in", "order out", "order out for",
    "order up", "owe to", "own up", "pack away", "pack in", "pack it in", "pack off", "pack out", "pack up", "pad down",
    "pad out", "pair off", "pair off with", "pair up", "pal about", "pal around", "pal up", "palm off", "pan out",
    "paper over", "pare back", "pare down", "part with", "pass around", "pass as", "pass away", "pass back", "pass by",
    "pass down", "pass for", "pass off", "pass on", "pass on to", "pass out", "pass over", "pass round", "pass through",
    "pass to", "pass up", "pat down", "patch together", "patch up", "pay back", "pay down", "pay for", "pay into",
    "pay off", "peck at", "peel away", "peel away from", "peel off", "peel off from", "peel out", "peg away",
    "peg down", "peg it", "peg out", "pen in", "pen up", "pencil in", "pep up", "perk up", "peter out", "phase in",
    "phase out", "phone in", "pick apart", "pick at", "pick off", "pick on", "pick out", "pick through", "pick up",
    "pick up after", "pick up on", "pick yourself up", "pig off", "pig out", "pile in", "pile into", "pile on",
    "pile out", "pile up", "pin down", "pin on", "pin up", "pine away", "pine for", "pipe down", "pipe up",
    "pit against", "pit out", "pitch for", "pitch in", "pitch into", "plant out", "plate up", "play about",
    "play along", "play around", "play at", "play away", "play back", "play down", "play off", "play on", "play out",
    "play up", "play up to", "play upon", "play with", "plead out", "plough back", "plough into", "plough on",
    "plough through", "plough up", "plow back", "plow into", "plow on", "plow through", "plow up", "pluck at",
    "pluck up", "plug away", "plug in", "plug into", "plump down", "plump for", "plump up", "plump yourself down",
    "point out", "poke about", "poke around", "polish off", "polish up", "pony up", "poop out", "poop out on",
    "pootle along", "pop down", "pop down to", "pop in", "pop off", "pop out", "pop up", "pore over", "potter about",
    "potter around", "pour down", "pour forth", "power down", "power off", "power up", "prattle on", "press ahead",
    "press for", "press forward with", "press into", "press on", "press upon", "prey on", "prey upon", "price in",
    "price up", "print out", "prop up", "pry out", "psych out", "psych up", "pucker up", "pull ahead", "pull apart",
    "pull away", "pull back", "pull down", "pull for", "pull in", "pull off", "pull on", "pull out", "pull over",
    "pull through", "pull to", "pull together", "pull up", "pull yourself together", "pump (money) into", "pump in",
    "pump out", "pump up", "push about", "push ahead", "push along", "push around", "push in", "push off", "push on",
    "push out", "push over", "push through", "put across", "put aside", "put away", "put back", "put by", "put down",
    "put down for", "put down to", "put forward", "put in", "put in for", "put off", "put on", "put out", "put over",
    "put through", "put together", "put towards", "put up", "put up to", "put up with", "quarrel out", "quarrel with",
    "queer up", "quieten down", "quit on", "race off", "rack off", "rack out", "rack up", "rain down on", "rain off",
    "rain out", "rake in", "rake it in", "rake off", "rake over", "rake up", "ramble on", "ramp up", "rap out",
    "rat on", "rat out", "rat through", "ratchet up", "rattle off", "reach out", "reach out for", "reach out to",
    "read off", "read out", "read up on", "reason out", "reckon on", "reel in", "reel off", "reel out", "rein in",
    "rent out", "ride off", "ride on", "ride out", "ride up", "ring back", "ring in", "ring off", "ring out",
    "ring round", "ring up", "ring with", "rip off", "rip on", "rise above", "rise to", "rise up", "rock up",
    "roll back", "roll by", "roll in", "roll off", "roll on", "roll out", "roll up", "romp in", "romp through",
    "room in", "root about", "root around", "root for", "root out", "root up", "rope in", "rope into", "rope off",
    "rough out", "rough up", "round down", "round off", "round on", "round out", "round up", "row back", "rub along",
    "rub down", "rub in", "rub into", "rub it in", "rub off on", "rub on", "rub out", "rub up against", "rub up on",
    "rule out", "run across", "run after", "run against", "run along", "run around", "run away", "run by", "run down",
    "run for", "run in", "run into", "run off", "run off with", "run on", "run out", "run out of", "run over",
    "run past", "run through", "run to", "run up", "run up against", "run up on", "run with", "rush away", "rush in",
    "rush into", "rush off", "rush out", "rustle up", "sack out", "saddle up", "saddle with", "sag off", "sail into",
    "sail through", "sally forth", "sally out", "salt away", "save on", "save up", "saw off", "saw up", "scale back",
    "scale down", "scale up", "scare away", "scare off", "scout about", "scout around", "scout out", "scout round",
    "scout up", "scrape along", "scrape by", "scrape in", "scrape into", "scrape through", "scrape together",
    "scrape up", "scratch around for", "screen off", "screen out", "screw around", "screw over", "screw up", "scuzz up",
    "see about", "see into", "see off", "see out", "see through", "see to", "seek out", "sell off", "sell on",
    "sell out", "sell up", "send back", "send for", "send in", "send off", "send off for", "send out", "send out for",
    "send up", "set about", "set apart", "set aside", "set back", "set forth", "set in", "set off", "set on", "set out",
    "set to", "set up", "set upon", "settle down", "settle for", "settle in", "settle on", "settle up", "sex up",
    "shack up", "shade in", "shade out", "shake down", "shake off", "shake out", "shake up", "shape up", "share in",
    "share out", "shave by", "shave from", "shave off", "shell out", "ship off", "ship out", "shoot away", "shoot back",
    "shoot for", "shoot off", "shoot out", "shoot up", "shop around", "shore up", "short out", "shout down",
    "shout out", "show around", "show in", "show off", "show out", "show over", "show round", "show through", "show up",
    "shrug off", "shut away", "shut down", "shut in", "shut off", "shut out", "shut out of", "shut up",
    "shut yourself away", "shy away", "shy away from", "side with", "sidle up to", "sift through", "sign away",
    "sign for", "sign in", "sign into", "sign off", "sign off on", "sign on", "sign on with", "sign out", "sign out of",
    "sign up", "sign with", "simmer down", "sing along", "sing out", "sing up", "single out", "sink in", "sit about",
    "sit around", "sit back", "sit by", "sit down", "sit for", "sit in", "sit in for", "sit in on", "sit on", "sit out",
    "sit over", "sit through", "sit up", "sit with", "size up", "skeeve out", "skin up", "skive off", "slack off",
    "slacken off", "slag off", "slant toward", "sleep around", "sleep in", "sleep off", "sleep on", "sleep out",
    "sleep over", "sleep through", "sleep together", "slice off", "slice up", "slip away", "slip by", "slip down",
    "slip in", "slip into", "slip off", "slip off to", "slip on", "slip out", "slip through", "slip up", "slob about",
    "slob around", "slope off", "slough off", "slow down", "slow up", "slug it out", "smack of", "smash down",
    "smash in", "smash up", "smoke out", "snaffle up", "snap off", "snap out of", "snap to it", "snap up", "snarl up",
    "sneak out", "sneak up on", "sneeze at", "sniff around", "sniff at", "sniff out", "snitch on", "snuff out",
    "snuggle up", "snuggle up to", "soak up", "sober up", "sock away", "sock in", "soften up", "soldier on", "sort out",
    "sound off", "sound out", "space out", "spaff away", "spark off", "spark up", "speak out", "speak to", "speak up",
    "speed up", "spell out", "spew out", "spew up", "spice up", "spiff up", "spike up", "spill out", "spill over",
    "spin around", "spin off", "spin out", "spirit away", "spirit off", "spit it out", "spit out", "splash down",
    "splash out", "splash out on", "split up", "spoil for", "sponge down", "sponge off", "sponge on", "spring back",
    "spring for", "spring from", "spring on", "spring up", "spruce up", "spur on", "square away", "square off",
    "square off against", "square up", "square up to", "square with", "squeeze up", "stack up", "stack up against",
    "staff up", "stamp out", "stand about", "stand around", "stand aside", "stand back", "stand by", "stand down",
    "stand for", "stand in for", "stand off", "stand out", "stand up", "stand up for", "stand up to", "stare down",
    "start off", "start off on", "start on", "start on at", "start out", "start out as", "start out to", "start over",
    "start up", "stash away", "stave in", "stave off", "stay away", "stay away from", "stay in", "stay on", "stay out",
    "stay over", "stay up", "steal away", "steal out", "steal over", "steal up", "steal up on", "steer clear of",
    "stem from", "step aside", "step back", "step down", "step forward", "step in", "step on it", "step out", "step to",
    "step up", "stick around", "stick at", "stick by", "stick down", "stick it to", "stick out", "stick out for",
    "stick to", "stick together", "stick up", "stick up for", "stick with", "stiffen up", "stir up", "stitch together",
    "stitch up", "stomp off", "stomp on", "stop around", "stop back", "stop behind", "stop by", "stop in", "stop off",
    "stop out", "stop over", "stop up", "store up", "storm off", "storm out", "stow away", "straighten out",
    "straighten up", "stretch out", "stretch to", "stretcher off", "strike back", "strike down", "strike off",
    "strike on", "strike out", "strike up", "strike upon", "string along", "string out", "string together", "string up",
    "strip away", "strip down", "strip down to", "strip of", "strip off", "strip out", "strip to", "stub out",
    "stuff up", "stumble across", "stumble upon", "stump up", "suck in", "suck into", "suck up", "suck up to",
    "suit up", "sum up", "summon up", "suss out", "swallow up", "swan about", "swan around", "swan in", "swan off",
    "swear by", "swear down", "swear in", "swear off", "sweep through", "swing around", "swing at", "swing by",
    "swing round", "switch off", "switch on", "switch over", "syphon off", "tack on", "tack onto", "tag along",
    "tag on", "tag onto", "tag with", "tail away", "tail back", "tail off", "take aback", "take after", "take apart",
    "take aside", "take away", "take back", "take down", "take for", "take in", "take it", "take it out on",
    "take it upon yourself", "take off", "take on", "take out", "take over", "take through", "take to", "take up",
    "talk around", "talk at", "talk back", "talk down", "talk down to", "talk into", "talk out", "talk out of",
    "talk over", "talk round", "talk through", "talk up", "talk yourself out", "tap for", "tap into", "tap off with",
    "tap out", "tap up", "taper off", "team up", "tear apart", "tear at", "tear away", "tear down", "tear into",
    "tear off", "tear out", "tear up", "tee off", "tee off on", "tee up", "tell apart", "tell off", "tell on",
    "tense up", "text out", "think over", "think through", "think up", "thrash out", "throw away", "throw in",
    "throw off", "throw on", "throw out", "throw over", "throw together", "throw up", "throw yourself at",
    "throw yourself into", "tick along", "tick away", "tick by", "tick off", "tick over", "tickle up", "tide over",
    "tidy up", "tie back", "tie down", "tie in", "tie in with", "tie up", "tighten up", "time out", "tip off",
    "tip over", "tire of", "tire out", "toddle off", "tone down", "tone in with", "tone up", "tool up", "tootle off",
    "top off", "top out", "top up", "torque up", "toss about", "toss around", "toss aside", "toss back", "toss down",
    "toss for", "toss off", "toss up", "total up", "touch down", "touch for", "touch off", "touch on", "touch up",
    "touch upon", "toughen up", "tow away", "toy around with", "toy at", "toy over", "toy with", "track down",
    "trade down", "trade in", "trade off", "trade on", "trade up", "trade upon", "train up", "trickle down",
    "trickle up", "trigger off", "trip out", "trip over", "trip up", "trot off", "trot off to", "trot out",
    "trudge through", "trump up", "try back", "try for", "try it on", "try on", "try out", "try out for", "tuck away",
    "tuck in", "tuck into", "tuck up", "tune in", "tune in to", "tune out", "tune up", "turf out", "turn against",
    "turn around", "turn away", "turn back", "turn down", "turn in", "turn into", "turn off", "turn on", "turn out",
    "turn over", "turn to", "turn up", "type in", "type out", "type up", "urge on", "urge upon", "use up", "usher in",
    "vacuum up", "vamp up", "veer onto", "veg out", "venture forth", "wade in", "wade into", "wade through",
    "wait about", "wait around", "wait behind", "wait in", "wait on", "wait out", "wait up", "wait upon", "wake up",
    "walk away from", "walk away with", "walk back", "walk back from", "walk in on", "walk into", "walk off",
    "walk off with", "walk on", "walk out", "walk out on", "walk through", "walk up", "waltz through", "wander off",
    "want out", "ward off", "warm up", "wash away", "wash down", "wash out", "wash over", "wash up", "waste away",
    "watch out", "watch out for", "watch over", "water down", "wave aside", "wave down", "wave off", "wave on",
    "wean off", "wear away", "wear down", "wear off", "wear out", "weasel out", "weasel out of", "weed out",
    "weigh down on", "weigh in", "weigh in on", "weigh on", "weigh out", "weigh up", "weird off on", "weird out",
    "well up", "wheel around", "wheel out", "wheel round", "while away", "whip into", "whip off", "whip out",
    "whip out of", "whip through", "whip up", "whisk away", "whisk off", "white out", "wig out", "wiggle out",
    "wiggle out of", "wimp out", "win back", "win out", "win over", "win round", "win through", "wind down", "wind on",
    "wind up", "winkle out", "winnow down", "winnow out", "wipe out", "wipe up", "wire up", "wise up", "word up",
    "work at", "work off", "work on", "work out", "work over", "work through", "wrap around", "wrap round", "wrap up",
    "wriggle out of", "write down", "write in", "write off", "write out", "write up", "yack on", "yammer on",
    "yield to", "zero in on", "zero out", "zip around", "zip by", "zip it", "zip up", "zone in", "zone in on",
    "zone out", "zonk out", "zoom in", "zoom in on", "zoom off", "zoom out"
}


def is_phrasal_verb_(sentence: str) -> bool:
    return sentence in PHRASAL_VERBS_


def check_after_verb_token_(token: Token) -> bool:
    return token.tag in ("ADV", "PRT")


def get_phrasal_verbs(text_tokens: List[Token]) -> List[Token]:
    phrasal_verbs = []
    i = 0
    while i < len(text_tokens):
        if text_tokens[i].tag != "VERB":
            i += 1
            continue

        phrasal_verb_words = 0
        phrasal_verb = ""
        if i + 1 < len(text_tokens) and check_after_verb_token_(text_tokens[i + 1]):
            phrasal_verb = " ".join((text_tokens[i].lemmatize().word, text_tokens[i + 1].lemmatize().word))
            phrasal_verb_words = 2 if is_phrasal_verb_(phrasal_verb) else 0

            if i + 2 < len(text_tokens) and check_after_verb_token_(text_tokens[i + 2]):
                phrasal_verb3 = " ".join((phrasal_verb, text_tokens[i + 2].lemmatize().word))
                if is_phrasal_verb_(phrasal_verb3):
                    phrasal_verb = phrasal_verb3
                    phrasal_verb_words = 3

        if phrasal_verb_words:
            phrasal_verbs.append(text_tokens[i].clone(phrasal_verb, Token.PHRASAL_VERB_TAG))

            i += phrasal_verb_words
        else:
            i += 1

    return phrasal_verbs

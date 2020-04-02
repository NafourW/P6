from pyparsing import *

def parse_rcl(rule):
    with open("logfiles/incomplete.rcl", "r") as file:
        counter = 0
        line = file.readline() 
        while line:
            counter += 1
            try:
                rule.parseString(line)
            except ParseException as e:
                print(e)
                break

            line = file.readline()
        
        print("Lines parsed: " + str(counter))
        error_line = line if line else "No errors while parsing"
        print(error_line)     

# General
integer = Word(nums)  # simple unsigned integer
realNumber = Combine(ZeroOrMore(Word("-", max=1)) + integer + Optional('.' + integer + Optional(((Literal('e-')) ^ (Literal('e+'))) + integer)))
space = " "
lp = Literal("(").suppress()
rp = Literal(")").suppress()
frame = integer
cycle = integer
time = Group(frame + Suppress(",") + cycle)
receive = "Recv"
coach = "Coach"
parameterContent = Combine(ZeroOrMore(Word(alphanums) | space))
parameter = OneOrMore(lp + parameterContent + rp)

# initialization
initialize = "init"
teamName = Word(alphanums)
playerName = Group(teamName + Suppress("_") + (integer | Literal(coach)))
goalieIndicator = lp + "goalie" + rp
initCommand = lp + initialize + teamName + parameter + ZeroOrMore(goalieIndicator) + rp
initialization = time + receive + playerName + Suppress(":") + initCommand

# message
drop_ball = Group("drop_ball")
play_on = Group("play_on")
before_kick_off = Group("before_kick_off")
kick_off = Group("kick_off" + Suppress("_") + (Literal('l') | Literal('r')))
kick_in = Group("kick_in" + Suppress("_") + (Literal('l') | Literal('r')))
free_kick = Group("free_kick" + Suppress("_") + (Literal('l') | Literal('r')))
free_kick_fault = Group("free_kick_fault" + Suppress("_") + (Literal('l') | Literal('r')))
indirect_free_kick = Group("indirect_free_kick" + Suppress("_") + (Literal('l') | Literal('r')))
corner_kick = Group("corner_kick" + Suppress("_") + (Literal('l') | Literal('r')))
half_time = Group("half_time")
first_half_over = Group("first_half_over")
time_extended = Group("time_extended")
goal = Group("goal" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)
goal_kick = Group("goal_kick" + Suppress("_") + (Literal('l') | Literal('r')))
goalie_catch_ball = Group("goalie_catch_ball" + Suppress("_") + (Literal('l') | Literal('r')))
catch_fault = Group("catch_fault" + Suppress("_") + (Literal('l') | Literal('r')))
offside = Group("offside" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_onfield = Group("penalty_onfield" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_foul = Group("penalty_foul" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_kick = Group("penalty_kick" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_setup = Group("penalty_setup" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_ready = Group("penalty_ready" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_taken = Group("penalty_taken" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_miss = Group("penalty_miss" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_score = Group("penalty_score" + Suppress("_") + (Literal('l') | Literal('r')))
penalty_winner = Group("penalty_winner" + Suppress("_") + (Literal('l') | Literal('r')))
foul = Group("foul" + Suppress("_") + (Literal('l') | Literal('r')))
foul_charge = Group("foul_charge" + Suppress("_") + (Literal('l') | Literal('r')))
foul_push = Group("foul_push" + Suppress("_") + (Literal('l') | Literal('r')))
foul_multiple_attack = Group("foul_multiple_attack" + Suppress("_") + (Literal('l') | Literal('r')))
foul_ballout = Group("foul_ballout" + Suppress("_") + (Literal('l') | Literal('r')))
back_pass = Group("back_pass" + Suppress("_") + (Literal('l') | Literal('r')))
yellow_card = Group("yellow_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)
red_card = Group("red_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)
illegal_defense = Group("illegal_defense" + Suppress("_") + (Literal('l') | Literal('r')))
pause = Group("pause")
time_up = Group("time_up")
time_over = Group("time_over")
human_judge = Group("human_judge")
messageKeyword = drop_ball | play_on | before_kick_off | kick_off | kick_in | free_kick | free_kick_fault | indirect_free_kick | corner_kick | half_time | first_half_over | time_extended | goal | goal_kick | goalie_catch_ball | catch_fault | offside | penalty_onfield | penalty_foul | penalty_kick | penalty_setup | penalty_ready | penalty_taken | penalty_miss | penalty_score | penalty_winner | foul | foul_charge | foul_push | foul_multiple_attack | foul_ballout | back_pass | yellow_card | red_card | illegal_defense | pause | time_up | time_over | human_judge
message = time + lp + "referee" + messageKeyword + rp

# action
kick = Group("kick" + realNumber + realNumber)
long_kick = Group("long_kick" + realNumber + realNumber)
goalieCatch = ("goalieCatch" + realNumber)
pointto = Group("pointto" + realNumber + realNumber)
tackle = Group("tackle" + realNumber + Optional((Literal("on") | Literal("off"))))
catch = Group("catch" + realNumber)
move = Group("move" + realNumber + realNumber)
dash = Group("dash" + realNumber + Optional(realNumber))
turn = Group("turn" + realNumber)
turn_neck = Group("turn_neck" + realNumber)
change_view = Group("change_view" + (Literal("wide") | Literal("narrow") | Literal("normal")))
attentionto = Group("attentionto" + (Group(Literal("our") + integer) | Group(Literal("off"))))
say = Group("say" + Suppress('"') + SkipTo(Suppress('"'), include=True))
bye = Group("bye")

# coach action
change_player_type = Group("change_player_type" + integer + integer)
say_coach_freeform = Group("say" + lp + Group("freeform" + Suppress('"') + SkipTo(Suppress('"'), include=True)) + rp)
player_htype = Group(lp + Word(alphas) + realNumber + rp)
player_mark = Group(lp + Word(alphas) + Group(Suppress("{") + integer + Suppress("}")) + rp)
player_info = ZeroOrMore(Group(lp + (Literal("dont") | Literal("do")) + Word(alphas) + Group(Suppress("{") + integer + Suppress("}")) + (player_htype | player_mark) + rp))
coach_info_content = Group(integer + Group(lp + Word(alphas) + rp) + player_info)
say_coach_info = Group("say " + lp + Group("info" + lp + coach_info_content + rp) + rp)
eye_on = Group(Literal("eye on"))

act_player = kick | long_kick | goalieCatch | pointto | tackle | catch | move | dash | turn | turn_neck | change_view | attentionto | say | bye
act_coach = change_player_type | say_coach_freeform | say_coach_info | eye_on
actCommand = OneOrMore(lp + (act_player | act_coach) + rp)

synch_see = Group(lp + "synch_see" + rp) + OneOrMore(Group(lp + parameterContent + Group(lp + parameterContent + rp) + rp))

team_graphic = Group(lp + "team_graphic" + lp + Group(SkipTo(lineEnd)))
setupCommand = synch_see | team_graphic
action = time + receive + playerName + Suppress(":") + (actCommand | setupCommand)

line = initialization | action | message


#print(rclParsing.strParsing('''8000,0	(referee penalty_setup_r)'''))
#print(type(rclParsing.strParsing('''0,370	Recv CYRUS2018_11: (turn 0)(turn_neck 0)  ''')))

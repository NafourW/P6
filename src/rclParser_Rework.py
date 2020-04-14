from pyparsing import Word, Combine, ZeroOrMore, Optional, Literal, Suppress, Group, alphanums, OneOrMore, nums, SkipTo, alphas, lineEnd


class rclParsing:
    is_game_end = False
    team_name_l = None
    team_name_r = None
    player_name = None
    kick_off_counter = 0
    yellow_cards = []
    red_cards = []

    def strParsing(self, rcl_string):
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
        teamName = Combine(Word(alphanums) + Optional("_" + Word(alphanums)))
        #playerName needs to be taken care of in AST, as teams with '_' in their names causes confusions
        playerName = (Group(Word(alphanums) + "_" + (integer | Literal(coach)) + Optional("_" + (integer | Literal(coach))))).setParseAction(rcl_Parser.get_player)
        goalieIndicator = lp + "goalie" + rp
        initCommand = (lp + "init" + teamName + parameter + ZeroOrMore(goalieIndicator) + rp).setParseAction(rclParsing.get_team_name)
        initialization = time + receive + teamName + SkipTo(":", include=True) + initCommand
        #initialization = time + receive + playerName + Suppress(":") + initCommand

        # message
        play_on = Group("play_on")
        before_kick_off = Group("before_kick_off")
        kick_off = Group("kick_off" + Suppress("_") + (Literal('l') | Literal('r'))).setParseAction(rclParsing.game_has_begun)
        kick_in = Group("kick_in" + Suppress("_") + (Literal('l') | Literal('r')))
        free_kick = Group("free_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        indirect_free_kick = Group("indirect_free_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        corner_kick = Group("corner_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        half_time = Group("half_time")
        time_extended = Group("time_extended")
        goal = (Group("goal" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rcl_Parser.goal_announce)
        goal_kick = Group("goal_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        goalie_catch_ball = Group("goalie_catch_ball" + Suppress("_") + (Literal('l') | Literal('r')))
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
        yellow_card = (Group("yellow_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rcl_Parser.get_yellow_card)
        red_card = (Group("red_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rcl_Parser.get_red_card)
        time_over = Group("time_over").setParseAction(rclParsing.game_has_ended)
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

        # coach action
        change_player_type = Group("change_player_type" + integer + integer)
        say_coach_freeform = Group("say" + lp + Group("freeform" + Suppress('"') + SkipTo(Suppress('"'), include=True)) + rp)
        player_htype = Group(lp + Word(alphas) + realNumber + rp)
        player_mark = Group(lp + Word(alphas) + Group(Suppress("{") + integer + Suppress("}")) + rp)
        player_info = ZeroOrMore(Group(lp + (Literal("dont") | Literal("do")) + Word(alphas) + Group(Suppress("{") + integer + Suppress("}")) + (player_htype | player_mark) + rp))
        coach_info_content = Group(integer + Group(lp + Word(alphas) + rp) + player_info)
        say_coach_info = Group("say " + lp + Group("info" + lp + coach_info_content + rp) + rp)
        eye_on = Group(Literal("eye on"))

        act_player = kick | long_kick | goalieCatch | pointto | tackle | catch | move | dash | turn | turn_neck | change_view | attentionto | say
        act_coach = change_player_type | say_coach_freeform | say_coach_info | eye_on
        actCommand = (OneOrMore(lp + (act_player | act_coach) + rp)).setParseAction(rcl_Parser.get_player_action)

        synch_see = Group(lp + "synch_see" + rp) + OneOrMore(Group(lp + parameterContent + Group(lp + parameterContent + rp) + rp))

        team_graphic = Group(lp + "team_graphic" + lp + Group(SkipTo(lineEnd)))
        setupCommand = synch_see | team_graphic
        action = time + "Recv" + playerName + Suppress(":") + (actCommand | setupCommand)


        command = initialization | action | message
        line = command

        return line.parseString(rcl_string)

    def get_initialization_info(self, line):
        # General
        integer = Word(nums)
        lp = Literal("(").suppress()
        rp = Literal(")").suppress()
        time = Group(integer + Suppress(",") + integer)
        coach = "Coach"
        parameterContent = Combine(ZeroOrMore(Word(alphanums) | " "))
        parameter = OneOrMore(lp + parameterContent + rp)


        # initialization
        teamName = Combine(Word(alphanums) + Optional("_" + Word(alphanums)))
        #playerName needs to be taken care of in AST, as teams with '_' in their names causes confusions
        playerName = Group(Word(alphanums) + Suppress("_") + (integer | Literal(coach)) + Optional(Suppress("_") + (integer | Literal(coach))))
        goalieIndicator = lp + "goalie" + rp
        initCommand = lp + "init" + teamName + parameter + ZeroOrMore(goalieIndicator) + rp
        initialization = time + "Recv" + playerName + Suppress(":") + initCommand

        return initialization.parseString(line)


    def get_team_name(self, initCommand):
        if rclParsing.team_name_l is not None:
            rclParsing.team_name_r = ''  # convert from None to string
            rclParsing.team_name_r = initCommand[1]
        else:
            rclParsing.team_name_l = ''  # convert from None to string
            rclParsing.team_name_l = initCommand[1]

    def game_has_begun(self, kick_off):
        if rcl_Parser.kick_off_counter == 0:
            if kick_off[0][1] == 'l':
                print("The game just begun with a kick off from " + rcl_Parser.team_name_l)
            elif kick_off[0][1] == 'r':
                print("The game just begun with a kick off from " + rcl_Parser.team_name_r)
            rcl_Parser.kick_off_counter += 1
        elif rcl_Parser.kick_off_counter > 0:
            if kick_off[0][1] == 'l':
                print("And we continue from " + rcl_Parser.team_name_l)
            elif kick_off[0][1] == 'r':
                print("And we continue from " + rcl_Parser.team_name_r)
            rcl_Parser.kick_off_counter += 1

    def get_player(self, playerName):
        player = ''
        i = 0
        while i < (len(playerName[0]) - 1):
            player += playerName[0][i]
            i += 1
        
        player += playerName[0][(len(playerName[0]) - 1)]
        
        if player in rcl_Parser.yellow_cards:
            print(player + " needs to be careful, he just received a yellow card!")
        elif player in rcl_Parser.red_cards:
            print("What the hell is " + player + " doing? He already got a red card!")
        else:
            rcl_Parser.player_name = player

    def get_player_action(self, actCommand):
        print(actCommand)


    def goal_announce(self, goal):
        if goal[0][1] == 'l':
            print(rclParsing.team_name_l + " has scored!")

        elif goal[0][1] == 'r':
            print(rclParsing.team_name_r + " has scored!")

    def get_yellow_card(self, yellow_card):
        if yellow_card[0][1] == 'l':
            player = str(rcl_Parser.team_name_l) + '_' + str(yellow_card[0][2])
            rcl_Parser.yellow_cards.append(player)
            print("Well, that's a yellow card for " + player + "!")
        elif yellow_card[0][1] == 'r':
            player = str(rcl_Parser.team_name_r) + '_' + str(yellow_card[0][2])
            rcl_Parser.yellow_cards.append(player)
            print("Well, that's a yellow card for " + player + "!")

    def get_red_card(self, red_card):
        if red_card[0][1] == 'l':
            player = str(rcl_Parser.team_name_l) + '_' + str(red_card[0][2])
            rcl_Parser.red_cards.append(player)
            print(player + " just received a red card!")
        elif red_card[0][1] == 'r':
            player = str(rcl_Parser.team_name_r) + '_' + str(red_card[0][2])
            rcl_Parser.red_cards.append(player)
            print(player + " just received a red card!")

    def game_has_ended(self):
        rclParsing.is_game_end = True

rcl_Parser = rclParsing()
rcl_Parser.strParsing("0,23	Recv CYRUS2019_1: (init CYRUS2019 (version 14) (goalie))")
rcl_Parser.strParsing("0,45	Recv HELIOS2019_1: (init HELIOS2019 (version 15) (goalie))")
#rcl_Parser.strParsing("2324,0	(referee yellow_card_l_2)")
#rcl_Parser.strParsing("2324,0	(referee red_card_r_11)")
#rcl_Parser.strParsing("5997,0	Recv HELIOS2019_9: (turn 0)(turn_neck 0)")
#rcl_Parser.strParsing("")
rcl_Parser.strParsing("90,0	Recv CYRUS2019_10: (kick 100 0.744628)(turn_neck -45)")

#rcl_Parser.strParsing("2542,0	(referee goal_r_1)")
#print(rcl_Parser.strParsing("2542,0	(referee goal_r_1)"))
#print(rcl_Parser.strParsing("8000,0	(referee penalty_setup_r)"))
#print(type(rclParsing.strParsing('''0,370	Recv CYRUS2018_11: (turn 0)(turn_neck 0)  ''')))

'''
    def get_endGame_info(self, line):
        # General
        integer = Word(nums)  # simple unsigned integer
        lp = Literal("(").suppress()
        rp = Literal(")").suppress()
        frame = integer
        cycle = integer
        time = Group(frame + Suppress(",") + cycle)

        # message
        time_up = Group("time_up")
        time_over = Group("time_over")
        human_judge = Group("human_judge")
        messageKeyword = time_up | time_over | human_judge
        message = time + lp + "referee" + messageKeyword + rp

        return message.parseString(line)
'''
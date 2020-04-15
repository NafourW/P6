from pyparsing import Word, Combine, ZeroOrMore, Optional, Literal, Suppress, Group, alphanums, OneOrMore, nums, SkipTo, alphas, lineEnd


class rclParsing:
    current_frame = 0
    current_cycle = 0
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
        #time = Group(frame + Suppress(",") + cycle)
        time = (Group(frame + Suppress(",") + cycle)).setParseAction(rclParsing.get_time)
        parameterContent = Combine(ZeroOrMore(Word(alphanums) | space))
        parameter = OneOrMore(lp + parameterContent + rp)

        # initialization
        teamName = Combine(Word(alphanums) + Optional("_" + Word(alphanums)))
        playerName = (Group(Word(alphanums) + "_" + (integer | Literal("Coach")) + Optional("_" + (integer | Literal("Coach"))))).setParseAction(rclParsing.get_player)
        goalieIndicator = lp + "goalie" + rp
        initCommand = (lp + "init" + teamName + parameter + ZeroOrMore(goalieIndicator) + rp).setParseAction(rclParsing.get_team_name)
        initialization = time + "Recv" + teamName + SkipTo(":", include=True) + initCommand

        # regular_game
        play_on = Group("play_on")
        kick_off = Group("kick_off" + Suppress("_") + (Literal('l') | Literal('r'))).setParseAction(rclParsing.game_has_begun)
        kick_in = Group("kick_in" + Suppress("_") + (Literal('l') | Literal('r')))
        free_kick = Group("free_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        corner_kick = Group("corner_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        half_time = Group("half_time")
        time_extended = Group("time_extended")
        goal = (Group("goal" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rclParsing.goal_announce)
        goal_kick = Group("goal_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        goalie_catch_ball = Group("goalie_catch_ball" + Suppress("_") + (Literal('l') | Literal('r')))
        offside = Group("offside" + Suppress("_") + (Literal('l') | Literal('r')))
        time_over = Group("time_over").setParseAction(rclParsing.game_has_ended)
        
        # penalty_game
        penalty_onfield = Group("penalty_onfield" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_foul = Group("penalty_foul" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_kick = Group("penalty_kick" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_setup = Group("penalty_setup" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_ready = Group("penalty_ready" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_taken = Group("penalty_taken" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_miss = Group("penalty_miss" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_score = Group("penalty_score" + Suppress("_") + (Literal('l') | Literal('r')))
        penalty_winner = Group("penalty_winner" + Suppress("_") + (Literal('l') | Literal('r')))
        
        # fouls
        foul = Group("foul" + Suppress("_") + (Literal('l') | Literal('r')))
        foul_charge = Group("foul_charge" + Suppress("_") + (Literal('l') | Literal('r')))
        foul_push = Group("foul_push" + Suppress("_") + (Literal('l') | Literal('r')))
        yellow_card = (Group("yellow_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rclParsing.get_yellow_card)
        red_card = (Group("red_card" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)).setParseAction(rclParsing.get_red_card)
        
        # messages
        regular_game = play_on | kick_off | kick_in | free_kick | corner_kick | half_time | time_extended | goal | goal_kick | goalie_catch_ball | offside | time_over
        fouls = foul | foul_charge | foul_push | yellow_card | red_card
        penalty_game = penalty_onfield | penalty_foul | penalty_kick | penalty_setup | penalty_ready | penalty_taken | penalty_miss | penalty_score | penalty_winner
        messageKeyword = regular_game | fouls | penalty_game
        message = time + lp + "referee" + messageKeyword + rp

        # action
        kick = Group("kick" + realNumber + realNumber)
        long_kick = Group("long_kick" + realNumber + realNumber)
        goalieCatch = ("goalieCatch" + realNumber)
        tackle = Group("tackle" + realNumber + Optional((Literal("on") | Literal("off"))))
        catch = Group("catch" + realNumber)
        move = Group("move" + realNumber + realNumber)
        dash = Group("dash" + realNumber + Optional(realNumber))

        act_player = kick | long_kick | goalieCatch | tackle | catch | move | dash
        actCommand = (OneOrMore(lp + (act_player + rp))).setParseAction(rclParsing.get_player_action)

        action = time + "Recv" + playerName + Suppress(":") + actCommand

        command = initialization | action | message | SkipTo(lineEnd)
        line = command

        return line.parseString(rcl_string)

    def get_initialization_info(self, line):
        # General
        integer = Word(nums)
        lp = Literal("(").suppress()
        rp = Literal(")").suppress()
        time = Group(integer + Suppress(",") + integer)
        parameterContent = Combine(ZeroOrMore(Word(alphanums) | " "))
        parameter = OneOrMore(lp + parameterContent + rp)

        # initialization
        teamName = Combine(Word(alphanums) + Optional("_" + Word(alphanums)))
        #playerName needs to be taken care of in AST, as teams with '_' in their names causes confusions
        playerName = Group(Word(alphanums) + Suppress("_") + (integer | Literal("Coach")) + Optional(Suppress("_") + (integer | Literal("Coach"))))
        goalieIndicator = lp + "goalie" + rp
        initCommand = lp + "init" + teamName + parameter + ZeroOrMore(goalieIndicator) + rp
        initialization = time + "Recv" + playerName + Suppress(":") + initCommand

        return initialization.parseString(line)


    def get_time(self, time):
        rclParsing.current_frame = time[0][0]
        rclParsing.current_cycle = time[0][1]
        print("Time: " + rclParsing.current_frame + ", " + rclParsing.current_cycle, end="\r")


    def get_team_name(self, initCommand):
        if rclParsing.team_name_l is not None:
            rclParsing.team_name_r = ''  # convert from None to string
            rclParsing.team_name_r = initCommand[1]
        else:
            rclParsing.team_name_l = ''  # convert from None to string
            rclParsing.team_name_l = initCommand[1]


    def game_has_begun(self, kick_off):
        if rclParsing.kick_off_counter == 0:
            if kick_off[0][1] == 'l':
                print("The game just begun with a kick off from " + rclParsing.team_name_l)
            elif kick_off[0][1] == 'r':
                print("The game just begun with a kick off from " + rclParsing.team_name_r)
            rclParsing.kick_off_counter += 1
        elif rclParsing.kick_off_counter > 0:
            if kick_off[0][1] == 'l':
                print("And we continue from " + rclParsing.team_name_l)
            elif kick_off[0][1] == 'r':
                print("And we continue from " + rclParsing.team_name_r)
            rclParsing.kick_off_counter += 1


    def get_player(self, playerName):
        player = ''
        i = 0
        while i < (len(playerName[0]) - 1):
            player += playerName[0][i]
            i += 1
        
        player += playerName[0][(len(playerName[0]) - 1)]
        '''
        if player in rclParsing.yellow_cards:
            print(player + " needs to be careful, he just received a yellow card!")
        elif player in rclParsing.red_cards:
            print("What the hell is " + player + " doing? He already got a red card!")
        else:
            rclParsing.player_name = player
        '''
        rclParsing.player_name = player


    def get_player_action(self, actCommand):
        #print(actCommand)
        pass


    def goal_announce(self, goal):
        if goal[0][1] == 'l':
            print(rclParsing.team_name_l + " has scored!")

        elif goal[0][1] == 'r':
            print(rclParsing.team_name_r + " has scored!")


    def get_yellow_card(self, yellow_card):
        if yellow_card[0][1] == 'l':
            player = str(rclParsing.team_name_l) + '_' + str(yellow_card[0][2])
            rclParsing.yellow_cards.append(player)
            print("Well, that's a yellow card for " + player + "!")
        elif yellow_card[0][1] == 'r':
            player = str(rclParsing.team_name_r) + '_' + str(yellow_card[0][2])
            rclParsing.yellow_cards.append(player)
            print("Well, that's a yellow card for " + player + "!")


    def get_red_card(self, red_card):
        if red_card[0][1] == 'l':
            player = str(rclParsing.team_name_l) + '_' + str(red_card[0][2])
            rclParsing.red_cards.append(player)
            print(player + " just received a red card!")
        elif red_card[0][1] == 'r':
            player = str(rclParsing.team_name_r) + '_' + str(red_card[0][2])
            rclParsing.red_cards.append(player)
            print(player + " just received a red card!")


    def game_has_ended(self):
        rclParsing.is_game_end = True


#rcl_Parser = rclParsing()
#rcl_Parser.strParsing('''0,173	Recv CYRUS2019_Coach: (team_graphic (16 7 "8 8 1 1" "b c None" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb" "bbbbbbbb"))''')
#rcl_Parser.strParsing("0,23	Recv CYRUS2019_1: (init CYRUS2019 (version 14) (goalie))")
#rcl_Parser.strParsing("0,45	Recv HELIOS2019_1: (init HELIOS2019 (version 15) (goalie))")
#rcl_Parser.strParsing("90,0	Recv CYRUS2019_10: (kick 100 0.744628)(turn_neck -45)")
#print(rcl_Parser.team_name_l)
#print(rcl_Parser.team_name_r)


#rcl_Parser.strParsing("")
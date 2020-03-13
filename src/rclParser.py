from pyparsing import Word, Combine, Literal, ZeroOrMore, Group, Optional, Suppress, OneOrMore, SkipTo, nums, alphanums, restOfLine, alphas

class rclParsing:
    
    def strParsing(self):
        # General
        irrelevant = restOfLine
        integer = Word(nums)  # simple unsigned integer
        realNumber = Combine(ZeroOrMore(Word("-", max=1)) + integer + Optional('.' + integer))
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
        play_on = Group("play_on")
        kick_off = Group("kick_off" + Suppress("_") + (Literal('l') | Literal('r')))
        goal = Group("goal" + Suppress("_") + (Literal('l') | Literal('r')) + Suppress("_") + integer)
        time_up = Group("time_up")
        time_over = Group("time_over")
        messageKeyword = play_on | kick_off | goal | time_up | time_over
        message = time + lp + "referee" + messageKeyword + rp

        # action
        move = Group("move" + realNumber + realNumber)
        dash = Group("dash" + realNumber)
        turn = Group("turn" + realNumber)
        turn_neck = Group("turn_neck" + realNumber)
        change_view = Group("change_view" + (Literal("wide") | Literal("narrow") | Literal("normal")))
        attentionto = Group("attentionto" + (Group(Literal("our") + integer) | Group(Literal("off"))))
        say = Group("say" + Suppress('"') + SkipTo(Suppress('"'), include=True))
        bye = Group("bye")

        # coach action
        change_player_type = Group("change_player_type" + integer + integer)
        say_coach_freeform = Group(
            "say" + lp + Group("freeform" + Suppress('"') + SkipTo(Suppress('"'), include=True)) + rp)
        player_mark = Group(lp + "mark" + Group(Suppress("{") + integer + Suppress("}")) + rp)
        player_info = ZeroOrMore(Group(lp + (Literal("dont") | Literal("do")) + "our" + Group(
            Suppress("{") + integer + Suppress("}")) + player_mark + rp))
        coach_info_content = Group(integer + Group(lp + Word(alphas) + rp) + player_info)
        say_coach_info = Group("say " + lp + Group("info" + lp + coach_info_content + rp) + rp)
        eye_on = Group(Literal("eye on"))

        act_player = move | dash | turn | turn_neck | change_view | attentionto | say | bye
        act_coach = change_player_type | say_coach_freeform | say_coach_info | eye_on
        actCommand = OneOrMore(lp + (act_player | act_coach) + rp)

        synch_see = Group(lp + "synch_see" + rp) + OneOrMore(Group(lp + parameterContent + Group(lp + parameterContent + rp) + rp))

        team_graphic = Group(lp + "team_graphic" + Group(lp + SkipTo(rp, include=True) + rp))
        setupCommand = synch_see | team_graphic
        action = time + receive + playerName + Suppress(":") + (actCommand | setupCommand)

        command = initialization | action | message
        line = command

        return line.parseString(self)

#print(rclParsing.strParsing('''0,92	Recv Fractals2019_Coach: (team_graphic (31 7 "8 8 3 1" ". c #555555" "X c #AAAAAA" "o c white" "oXXXoooo" ".ooooooo" "XXoooooo" "oX.ooooo" "oXXXoooo" "oooooooo" "oooooooo" "oooooooo"))'''))
#print(type(rclParsing.strParsing('''0,370	Recv CYRUS2018_11: (turn 0)(turn_neck 0)  ''')))
#test_action2 = '''1,0	Recv HELIOS2019_2: (dash 68.304)(turn_neck -83)'''
#test_action3 = '''1,0	Recv HELIOS2019_2: (dash 68.304)(turn_neck -83)(change_view normal)'''
#test_action4 = '''1,0	Recv HELIOS2019_2: (dash 68.304)(turn_neck -83)(change_view normal)(attentionto our 11)'''
#Trash test strings
#test_initialize = "0,32	Recv Fractals2019_1: (init Fractals2019 (version 15) (goalie))"
#test_message = "95,0	(referee play_on)"
#test_message2 = "7685,51	(referee kick_off_r)"
#test_message3 = "7685,0	(referee goal_l_1)"

#variable = Word(alphas, max=1)   # single letter variable, such as x, z, m, etc.
#arithOp  = Word("+-*/", max=1)   # arithmetic operators
#equation = variable + "=" + integer + arithOp + integer    # will match "x=2+2", etc
#test = "x = 2 * 5"

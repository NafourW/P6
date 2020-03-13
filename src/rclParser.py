from pyparsing import *

class rclParsing:
    
    def strParsing(self):
        #General
        integer  = Word(nums)            # simple unsigned integer
        realNumber = Combine(ZeroOrMore(Word("-", max = 1)) + integer + Optional('.' + integer))
        space = " "
        lp = Literal("(").suppress()
        rp = Literal(")").suppress()
        frame = integer
        cycle = integer
        time = Group(frame + Suppress(",") + cycle)
        receive = "Recv"
        parameterContent = Combine(ZeroOrMore(Word(alphanums) | space))
        parameter = OneOrMore(lp + parameterContent + rp)

        # initialization
        initialize = "init"
        teamName = Word(alphanums)
        playerName = Group(teamName + Suppress("_") + integer)
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
        say = Group(Literal("say") + Suppress('"') + SkipTo(Suppress('"'), include=True))
        bye = Group("bye")

        actCommand_keyword = move | dash | turn | turn_neck | change_view | attentionto | say | bye
        actCommand = OneOrMore(lp + actCommand_keyword + rp)
        action = time + receive + playerName + Suppress(":") + actCommand

        irrelevant = restOfLine
        command = initialization | action | message | empty | irrelevant
        line_test = command
        

        return line_test.parseString(self)

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

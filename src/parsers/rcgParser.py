from pyparsing import Word, Literal, ZeroOrMore, SkipTo, lineEnd, nums, alphanums, Combine, Suppress, Group, Suppress, Optional, OneOrMore

class rcgParsing:
    current_frame = 0
    is_game_end = False
    team_name_1 = None
    team_name_2 = None
    team_score_1 = 0
    team_score_2 = 0
    goal_alarm = 0  # Turns to 'True' when a player scores
    goal_frame = 0

    def get_ball_info(self, line):
        left_p = Literal("(").suppress()
        right_p = Literal(")").suppress()
        frame_number = Word(nums) 

        show_frame = Word("show ") + frame_number
        ball = left_p + left_p + Literal("b") + right_p + Group(Word(nums + "-.") * 4) + right_p

        frame_line = left_p + Group(show_frame).suppress() + ball + SkipTo(lineEnd).suppress()

        parsed_ball_info = frame_line.parseString(line)
        ball_info = {
            "pos_x" : parsed_ball_info[1][0],
            "pos_y" : parsed_ball_info[1][1],
            "vel_x" : parsed_ball_info[1][2],
            "vel_y" : parsed_ball_info[1][3]
        }
        return ball_info


    def get_player_info(self, line):
        left_p = Literal("(").suppress()
        right_p = Literal(")").suppress()
        frame_number = Word(nums)

        # Frame and ball information
        show_frame = Word("show ") + frame_number
        ball = left_p + left_p + Literal("b") + right_p + Word(nums + "-.") * 4 + right_p

        # Player information
        player_number = left_p + (Word("r") ^ Word("l")) + Word(nums) + right_p

        # Player positions
        player_position = Word(alphanums + "-.")

        # Player view mode - H for high and L for low
        view_mode = left_p + Literal("v") + (Word("h") ^ Word("l")) + Word(nums) + right_p
        stamina = left_p + Literal("s") + Word(nums + "-.") * 4 + right_p

        # Outer flag rules
        flag_pos = Word("lrbtc", max=1)
        field_side = Word("lr", max=1)
        distance_from_center = Word(nums)
        outer_flag = flag_pos + ZeroOrMore(field_side) + distance_from_center

        # Inner flag rules
        inner_flag_pos = Word("lrc", max=1)
        inner_flag = inner_flag_pos + (Word("b") ^ Word("t"))

        # Center flag
        center_flag = Literal("c")
        flag = left_p + Literal("f") + (outer_flag ^ inner_flag ^ center_flag) + right_p

        # Additional information
        additional = left_p + Literal("c") + Word(nums + "-.") * 11 + right_p

        player = left_p + Group(player_number) + Group(ZeroOrMore(player_position)) + Group(view_mode) + Group(stamina) + Group(ZeroOrMore(flag)) + Group(additional) + right_p

        # Frame lines
        frame_line1 = show_frame.suppress() + ball.suppress() + (Group(player) * 11)
        frame_line2 = (Group(player) * 11)

        read_line = left_p + (frame_line1 + frame_line2) + right_p

        parsed_players = read_line.parseString(line)

        # Place information into dictionary to easily query information
        player_info = {}
        counter = 1
        for player in parsed_players:
            body_info = player[1]
            view_mode = player[2]
            stamina = player[3]

            player_info[str(counter)] = {
            "side" : player[0][0],
            "unum" : player[0][1],
            "type_id" : body_info[0],
            "state" : body_info[1],
            "pos_x" : body_info[2],
            "pos_y" : body_info[3],
            "vel_x" : body_info[4],
            "vel_y" : body_info[5],
            "body_angle" : body_info[6],
            "head_angle" : body_info[7],
            "view_quality" : view_mode[1],
            "view_width" : view_mode[2],
            "stamina" : stamina[1],
            "stamina_effort" : stamina[2],
            "stamina_recovery" : stamina[3],
            "stamina_capacity" : stamina[4]
            }
            
            counter += 1

        return player_info


    def strParsing(self, rcg_string):
        left_p = Literal("(")
        right_p = Literal(")")
        frame_number = Word(nums) 
        teamscore_result_name = Word(alphanums)
        teamscore_result_value = Word(alphanums)
        teamscore_result_score = Word(nums)
        # This needs to be taken care of by AST because some teams have '_' in their names
        teamscore_result = (teamscore_result_name + "_" + teamscore_result_value + Optional("_" + teamscore_result_score)).setParseAction(rcgParsing.get_team_result)

        # Playmode
        # Playmode list
        play_mode_list = (Word(" play_on") ^ Word(" time_over") ^ Word(" free_kick_r") ^ Word(" free_kick_l") ^ Word(" indirect_free_kick_l") ^ Word(" indirect_free_kick_r") ^ Word(" kick_in_l") ^ Word(" kick_in_r") ^ Word(" foul_charge_r") ^ Word(" foul_charge_l") ^ Word(" kick_off_l") ^ Word(" kick_off_r") ^ Word(" corner_kick_l") ^ Word(" corner_kick_r") ^ Word(" offside_r") ^ Word(" offside_l") ^ Word(" foul_charge_l") ^ Word(" foul_charge_r") ^ Word(" goal_kick_l") ^ Word(" goal_kick_r") ^ Word(" penalty_setup_l") ^ Word(" penalty_setup_r") ^ Word(" penalty_ready_l") ^ Word(" penalty_ready_r") ^ Word(" penalty_taken_l") ^ Word(" penalty_taken_r") ^ Word(" penalty_miss_l") ^ Word(" penalty_miss_r") ^ Word(" penalty_score_r") ^ Word(" penalty_score_l") )        
        play_mode = (Word("playmode ") + Word(nums) + play_mode_list).setParseAction(rcgParsing.goal_notification)

        # Teamname
        team_name = Combine(Word(alphanums) + Optional(OneOrMore((Literal("-") | Literal("_")) + Word(alphanums))))

        # Teamscore
        team_score = Word("team ") + Word(nums) + team_name + team_name + Word(nums) * 2
        team_score_penalty = Word("team ") + Word(nums) + team_name + team_name + Word(nums) * 6

        # Frame and ball information
        show_frame = Word("show ") + frame_number.setParseAction(rcgParsing.get_current_frame)
        ball = left_p + left_p + Literal("b") + right_p + Word(nums + "-.") * 4 + right_p

        # Player information
        player_number = left_p + (Word("r") ^ Word("l")) + Word(nums) + right_p

        # Player positions
        player_position = Word(alphanums + "-.")

        # Player view mode - H for high and L for low
        view_mode = left_p + Literal("v") + (Word("h") ^ Word("l")) + Word(nums) + right_p
        stamina = left_p + Literal("s") + Word(nums + "-.") * 4 + right_p

        # Outer flag rules
        flag_pos = Word("lrbtc", max=1)
        field_side = Word("lr", max=1)
        distance_from_center = Word(nums)
        outer_flag = flag_pos + ZeroOrMore(field_side) + distance_from_center

        # Inner flag rules
        inner_flag_pos = Word("lrc", max=1)
        inner_flag = inner_flag_pos + (Word("b") ^ Word("t"))

        # Center flag
        center_flag = Literal("c")
        flag = left_p + Literal("f") + (outer_flag ^ inner_flag ^ center_flag) + right_p

        # Additional information
        additional = left_p + Literal("c") + Word(nums + "-.") * 11 + right_p

        player = left_p + player_number + ZeroOrMore(player_position) + view_mode + stamina + ZeroOrMore(flag) + additional + right_p

        # Start of game
        start = Word("ULG5")
        server_param = "server_param " + SkipTo(lineEnd)
        player_param = "player_param " + SkipTo(lineEnd)
        player_type = "player_type " + SkipTo(lineEnd)

        # End game - (msg 6000 1 "(result 201806211300 CYRUS2018_0-vs-HELIOS2018_1)")
        end_game = Word("result") + Word(nums) + teamscore_result + Suppress("-vs-") + teamscore_result + Suppress(right_p)+ Suppress('"').setParseAction(rcgParsing.game_has_ended)
        team_graphic = (Word("team_graphic_l") ^ Word("team_graphic_r")) + SkipTo(lineEnd)

        msg = "msg" + frame_number + Word(nums) + Suppress('"') + Suppress(left_p) + (end_game|team_graphic)

        # Frame lines
        frame_line1 = show_frame + ball + (player * 11)
        frame_line2 = (player * 11)

        read_line = start ^ (left_p + (server_param ^ player_param ^ player_type ^ msg ^ ((frame_line1 + frame_line2) ^ play_mode ^ team_score ^ team_score_penalty) + right_p))

        return read_line.parseString(rcg_string)


    def get_current_frame(self, show_frame):
        rcgParsing.current_frame = show_frame[0]
        #print(rcgParsing.current_frame)


    def goal_notification(self, play_mode):
        if (play_mode[2] == "goal_r") or (play_mode[2] == "goal_l"):
            rcgParsing.goal_frame = int(play_mode[1])
            rcgParsing.goal_alarm += 1


    def get_team_result(self, teamscore_result):
        if rcgParsing.team_name_1 is not None:
            rcgParsing.team_score_2 = int(teamscore_result[len(teamscore_result) - 1])
            rcgParsing.team_name_2 = ''
            i = 0
            while i < (len(teamscore_result) - 2):
                rcgParsing.team_name_2 += teamscore_result[i]
                i += 1

        else:
            rcgParsing.team_score_1 = int(teamscore_result[len(teamscore_result) - 1])
            rcgParsing.team_name_1 = ''
            i = 0
            while i < (len(teamscore_result) - 2):
                rcgParsing.team_name_1 += teamscore_result[i]
                i += 1


    def game_has_ended(self):
        print("Finally the game has ended, and the victory goes to ")
        if rcgParsing.team_score_1 == rcgParsing.team_score_2:
            print("no one! Because we got a draw!")
        elif rcgParsing.team_score_1 > rcgParsing.team_score_2:
            print(rcgParsing.team_name_1 + "!")
        elif rcgParsing.team_score_2 > rcgParsing.team_score_1:
            print(rcgParsing.team_name_2 + "!")
        rcgParsing.is_game_end = True


# rcg_Parser = rcgParsing()
# rcg_Parser.strParsing('''(team 8129 Receptivity MT2019 1 1 0 1 0 0)''')
#rcg_Parser.strParsing('''(playmode 1567 foul_charge_r)''')
#rcg_Parser.strParsing('''(playmode 1682 goal_l)''')
#rcg_Parser.strParsing('''''')
#rcg_Parser.strParsing('''(msg 6000 1 "(result 201806211300 CYRUS2018_0-vs-HELIOS2018_1)")''')
#print(rcg_Parser.strParsing('''(msg 6000 1 "(result 201806211300 CYRUS2018_0-vs-HELIOS2018_1)")'''))
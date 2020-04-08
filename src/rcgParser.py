from pyparsing import Word, Literal, ZeroOrMore, SkipTo, lineEnd, nums, alphanums, Combine, Suppress, Group, Suppress

class rcgParsing:
    def get_ball_info(self, line):
        left_p = Literal("(").suppress()
        right_p = Literal(")").suppress()
        frame_number = Word(nums) 

        show_frame = Word("show ") + frame_number
        ball = left_p + left_p + Literal("b") + right_p + Group(Word(nums + "-.") * 4) + right_p

        frame_line = left_p + Group(show_frame).suppress() + ball + SkipTo(lineEnd)

        return frame_line.parseString(line)

    def strParsing(self, rcg_string):
        left_p = Literal("(")
        right_p = Literal(")")
        frame_number = Word(nums) 
        # This needs to be taken care of by AST because some teams have '_' in their names
        teamscore_result = Combine(ZeroOrMore(alphanums + "_")) + Suppress("_") + nums


        # Playmode
        # Playmode list
        play_mode_list = (Word(" play_on") ^ Word(" time_over") ^ Word(" free_kick_r") ^ Word(" free_kick_l") ^ Word(" kick_in_l") ^ Word(" kick_in_r") ^ Word(" foul_charge_r") ^ Word(" foul_charge_l") ^ Word(" kick_off_l") ^ Word(" kick_off_r") ^ Word(" corner_kick_l") ^ Word(" corner_kick_r") ^ Word(" offside_r") ^ Word(" offside_l") ^ Word(" foul_charge_l") ^ Word(" foul_charge_r") ^ Word(" goal_kick_l") ^ Word(" goal_kick_r"))
        play_mode = Word("playmode ") + Word(nums) + play_mode_list

        # Teamscore
        team_score = Word("team ") + Word(nums) + Word(alphanums) + Word(alphanums) + Word(nums) * 2

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

        player = left_p + player_number + ZeroOrMore(player_position) + view_mode + stamina + ZeroOrMore(flag) + additional + right_p

        # Start of game
        start = Word("ULG5")
        server_param = "server_param " + SkipTo(lineEnd)
        player_param = "player_param " + SkipTo(lineEnd)
        player_type = "player_type " + SkipTo(lineEnd)

        # End game - (msg 6000 1 "(result 201806211300 CYRUS2018_0-vs-HELIOS2018_1)")
        end_game = "msg" + frame_number + Word(nums) + Suppress('"') + Suppress(left_p) + "result" + Word(nums) + teamscore_result + Suppress("-vs-") + teamscore_result + Suppress(right_p)+ Suppress('"')
        team_graphic = "msg" + frame_number + Word(nums) + Suppress('"') + Suppress(left_p) + (Word("team_graphic_l") ^ Word("team_graphic_r")) + SkipTo(lineEnd)

        # Frame lines
        frame_line1 = show_frame + ball + (player * 11)
        frame_line2 = (player * 11)

        read_line = start ^ (left_p + (server_param ^ player_param ^ player_type ^ end_game ^ team_graphic ^ ((frame_line1 + frame_line2) ^ play_mode ^ team_score) + right_p))

        return read_line.parseString(rcg_string)
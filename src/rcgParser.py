from pyparsing import *

left_p = Literal("(")
right_p = Literal(")")
frame_number = Word(nums) 

# Playmode
play_mode = Word("playmode ") + Word(nums) + Word(" play_on")

# Frame and ball information
show_frame = Word("show ") + frame_number
ball = left_p + left_p + Literal("b") + right_p + Word(nums + "-.") * 4 + right_p

# Player information
player_number = left_p + (Word("r") ^ Word("l")) + Word(nums) + right_p

# Player positions
player_pos1 = player_pos2 = player_pos3 = player_pos4 = player_pos5 = player_pos6 = player_pos7 = player_pos8 = Word(alphanums + "-.")
player_position = player_pos1 + player_pos2 + player_pos3 + player_pos4 + player_pos5 + player_pos6 + player_pos7 + player_pos8

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

# Penalty box
# TODO Add penalty box to flag variable
# penalty_box_flag = 

flag = left_p + Literal("f") + (outer_flag ^ inner_flag ^ center_flag) + right_p

# Additional information
additional = left_p + Literal("c") + Word(nums + "-.") * 11 + right_p

player = left_p + player_number + player_position + view_mode + stamina + ZeroOrMore(flag) + additional + right_p


frame_line1 =  show_frame + ball + (player * 11)
frame_line2 = (player * 11)
read_line = left_p + ((frame_line1 + frame_line2) ^ play_mode) + right_p

with open("logfiles/test.rcg", "r") as file:
    counter = 0
    line = file.readline() 
    while line:
        counter += 1
        try:
            read_line.parseString(line)
        except ParseException as e:
            print(e)
            break

        line = file.readline()
    
    print(counter)
    print(line)

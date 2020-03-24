from pyparsing import *

ws = " "
left_p = Literal("(")
right_p = Literal(")")
show = Word("show ")
frame_number = Word(nums) 
ball_literal = Literal("b")
ball_location = Word(nums) * 4
left_player = Literal("l")
right_player = Literal("r")
single_number_word = Word(nums)
single_pos_or_neg_number = Word(nums + "-.")
player_position_word = Word(alphanums + "-.")

# Frame and ball information
show_frame = show + frame_number
ball = left_p + left_p + ball_literal + right_p + ball_location + right_p

# Player information
player_number = left_p + left_p + oneOf(["r", "l"]) + single_number_word + right_p

# TODO Find out what these values denote
player_pos1 = player_pos2 = player_pos3 = player_pos4 = player_pos5 = player_pos6 = player_pos7 = player_pos8 = player_position_word
player_position = player_pos1 + player_pos2 + player_pos3 + player_pos4 + player_pos5 + player_pos6 + player_pos7 + player_pos8

# TODO View mode can also be "l" for low
view_mode = left_p + Literal("v") + Literal("h") + single_number_word + right_p
stamina = left_p + Literal("s") + single_pos_or_neg_number + single_pos_or_neg_number + single_number_word + single_number_word + right_p

# Outer flag rules
flag_pos = Word("lrbt", max=1)
field_side = Word("lr", max=1)
distance_from_center = Word(nums, max=1)
outer_flag = flag_pos + ZeroOrMore(field_side) + distance_from_center

# Inner flag rules
inner_flag_pos = Word("lrc", max=1)
inner_flag = inner_flag_pos + oneOf(["b", "t"])

# Center flag
center_flag = Literal("c")

# Penalty box
# TODO Add penalty box to flag variable
# penalty_box_flag = 

flag = left_p + Literal("f") + (outer_flag ^ inner_flag ^ center_flag) + right_p

# Additional information
additional = left_p + Literal("c") + single_number_word * 11 + right_p

player = player_number + player_position + view_mode + stamina + flag + additional + right_p


read_line = left_p + show_frame + ball + (player * 11) + right_p
rcg_line = "(show 2 ((b) 0 0 0 0) ((l 1) 17 0x9 -48.3991 -0.0284 0.1915 -0.009 -1.136 -80 (v h 180) (s 7943.41 0.92242 1 130557) (f l 2) (c 0 1 184 0 1 186 1 1 0 0 2)) ((l 2) 16 0x1 -12.5 -5 0 0 162.385 -21 (v h 180) (s 8000 0.832181 1 130600) (f l 11) (c 0 0 175 0 1 176 1 1 0 0 2)) ((l 3) 6 0x1 -11.9934 4.7474 0.1997 -0.0996 -27.578 -81 (v h 120) (s 7945.54 0.926261 1 130554) (f l 2) (c 0 1 169 0 1 171 2 0 0 0 2)) ((l 4) 0 0x1 -11.0815 -15.448 0.2074 0.1408 30.995 65 (v h 180) (s 7945 1 1 130555) (f l 11) (c 0 1 164 0 1 166 1 0 0 0 1)) ((l 5) 8 0x1 -11.4082 15.2748 0.0763 -0.209 -68.232 -90 (v h 60) (s 7945.11 0.987558 1 130555) (f l 11) (c 0 1 159 0 1 161 2 0 0 0 2)) ((l 6) 14 0x1 -6.5227 -1.3164 0.0546 0.1797 73.94 89 (v h 180) (s 7941.57 0.928521 1 130558) (f l 11) (c 0 1 154 0 1 156 1 0 0 0 1)) ((l 7) 2 0x1 -9.7308 -10.3194 0.1015 0.1813 60.619 -21 (v h 180) (s 7943.6 0.880395 1 130556) (f l 2) (c 0 1 149 0 1 151 1 0 0 0 2)) ((l 8) 15 0x1 -9.5688 10.5121 0.1644 -0.1097 -35.368 -31 (v h 120) (s 7945.86 0.904284 1 130554) (f l 2) (c 0 1 144 0 1 146 2 0 0 0 2)) ((l 9) 11 0x1 -0.3463 -23.2523 0.0706 0.2516 79.004 89 (v h 120) (s 7946.32 0.968648 1 130554) (f l 2) (c 0 1 139 0 1 141 2 0 0 0 2)) ((l 10) 10 0x1 -0.513 23.1816 -0.0049 -0.2347 -86.598 -90 (v h 120) (s 7941.21 0.930058 1 130559) (f l 2) (c 0 1 134 0 1 136 2 0 0 0 2)) ((l 11) 5 0x1 -0.385 0 0 0 -178.708 -46 (v h 60) (s 8000 0.885698 1 130600) (f l 2) (c 0 0 130 0 1 131 2 0 0 0 2)) ((r 1) 0 0x9 48.5949 -0.0485 -0.162 -0.0194 -173.912 -80 (v h 180) (s 7977.5 1 1 130555) (f r 2) (c 0 1 154 0 1 156 1 1 0 0 2)) ((r 2) 6 0x1 24.679 10.7966 -0.1265 -0.0802 -145.001 -11 (v h 120) (s 7977.23 0.926261 1 130554) (f r 11) (c 0 1 144 0 1 146 2 1 0 0 2)) ((r 3) 14 0x1 24.2197 -10.5871 -0.1309 0.0687 152.23 63 (v h 120) (s 7958.59 0.928521 1 130517) (f r 2) (c 0 2 138 0 1 141 2 0 0 0 2)) ((r 4) 2 0x1 15.8907 22.6481 -0.0412 -0.1327 -107.207 56 (v h 180) (s 7978.2 0.880395 1 130556) (f r 2) (c 0 1 134 0 1 136 1 0 0 0 2)) ((r 5) 5 0x1 15.9602 -22.6464 -0.0191 0.1694 100.723 -26 (v h 120) (s 7975.29 0.885698 1 130551) (f r 2) (c 0 1 129 0 1 131 2 0 0 0 2)) ((r 6) 8 0x1 19.5877 -0.097 -0.164 -0.0386 -168.912 -49 (v h 120) (s 7977.44 0.987558 1 130555) (f r 2) (c 0 1 124 0 1 126 2 0 0 0 2)) ((r 7) 15 0x1 11.6423 7.9531 -0.1363 -0.0179 -173.42 -1 (v h 120) (s 7977.07 0.904284 1 130554) (f r 2) (c 0 1 119 0 1 121 2 0 0 0 2)) ((r 8) 17 0x1 11.6488 -8.1599 -0.1119 -0.051 -158.561 -56 (v h 60) (s 7978.29 0.92242 1 130557) (f r 11) (c 0 1 114 0 1 116 2 0 0 0 2)) ((r 9) 10 0x1 4.3113 23.4026 0.2726 -0.1327 -24.874 -90 (v h 120) (s 7882.43 0.930058 1 130518) (f r 2) (c 0 2 108 0 1 111 2 0 0 0 2)) ((r 10) 11 0x1 3.4561 -23.6423 0.2095 0.1643 40.741 9 (v h 120) (s 7946.32 0.968648 1 130554) (f r 2) (c 0 1 104 0 1 106 2 0 0 0 2)) ((r 11) 16 0x1 9.7047 -0.3305 0.0273 -0.1647 -83.373 -81 (v h 180) (s 7976.72 0.832181 1 130553) (f r 2) (c 0 1 99 0 1 101 1 0 0 0 2)))"
print(read_line.parseString(rcg_line))

# plus 12
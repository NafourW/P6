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
player_number = left_p + left_p + (Word("r") ^ Word("l")) + single_pos_or_neg_number + right_p

# TODO Find out what these values denote
player_pos1 = player_pos2 = player_pos3 = player_pos4 = player_pos5 = player_pos6 = player_pos7 = player_pos8 = player_position_word
player_position = player_pos1 + player_pos2 + player_pos3 + player_pos4 + player_pos5 + player_pos6 + player_pos7 + player_pos8

# TODO View mode can also be "l" for low
view_mode = left_p + Literal("v") + (Word("h") ^ Word("l")) + single_pos_or_neg_number + right_p
stamina = left_p + Literal("s") + single_pos_or_neg_number + single_pos_or_neg_number + single_pos_or_neg_number + single_pos_or_neg_number + right_p

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
additional = left_p + Literal("c") + single_pos_or_neg_number * 11 + right_p

player = player_number + player_position + view_mode + stamina + ZeroOrMore(flag) + additional + right_p


read_line = left_p + show_frame + ball + (player * 11)
read_line1 = (player * 11)
read_line2 = read_line + read_line1 + right_p

with open("logfiles/test.rcg", "r") as file:
    # print(file.readline())
    counter = 0
    line = file.readline() 
    while file.readline():
        counter += 1
        print(counter)
        try:
            print(read_line2.parseString(line))
        except ParseException:
            print(line)
        
        line = file.readline() 

# rcg_line = "(show 22 ((b) 0 0 0 0) ((l 1) 0 0x9 -33.4371 0.1925 0.1743 0.0083 -0.199 0 (v h 120) (s 7165 1 1 129835) (f l 11) (c 0 16 498 0 1 515 2 0 0 0 10)) ((l 2) 10 0x1 -6.5928 -0.0327 0.2934 -0.0926 -15.288 -90 (v h 60) (s 6910.91 0.943286 1 129732) (f l 10) (c 0 20 433 0 1 454 3 3 0 0 7)) ((l 3) 4 0x1 -13.2399 -18.9864 0.0002 0 55.584 -34 (v h 120) (s 7785.3 0.979394 1 129615) (f l 10) (c 0 12 410 0 1 423 2 3 0 0 6)) ((l 4) 5 0x1 -13.5694 19.4445 0.0007 0 -56.235 30 (v h 120) (s 7723.61 0.908495 1 129676) (f l 10) (c 0 12 379 0 1 392 2 2 0 0 9)) ((l 5) 17 0x1 -8.7196 -4.2034 0.307 -0.0416 -16.168 19 (v h 60) (s 7000.56 0.801842 1 129599) (f l 10) (c 0 20 340 0 1 361 3 2 0 0 6)) ((l 6) 7 0x1 -4.7117 4.5989 0.4073 0.2193 27.501 -25 (v h 60) (s 7096.08 0.904061 1 129504) (f l 10) (c 0 20 309 0 1 330 2 2 0 0 8)) ((l 7) 15 0x1 -1.881 -24.4327 0.0063 -0.0026 84.992 -25 (v h 120) (s 7270.65 0.879543 1 129729) (f l 10) (c 0 16 282 0 1 299 2 2 0 0 8)) ((l 8) 6 0x1 -1.6516 24.2592 0.0049 0.0012 -86.115 -15 (v h 120) (s 7216.56 0.85015 1 129783) (f l 10) (c 0 16 251 0 1 268 2 2 0 0 12)) ((l 9) 3 0x1 -1.6302 -28.2389 0 -0 85.584 -15 (v h 120) (s 8000 0.983479 1 129700) (f l 5) (c 0 9 227 0 1 237 2 2 0 0 16)) ((l 10) 11 0x1 -0.4046 -0.0536 -0 0 179.988 30 (v h 60) (s 8000 0.965419 1 130070) (c 0 6 199 0 1 206 3 2 0 0 0)) ((l 11) 16 0x1 -1.1759 -12.6884 0 0 85.298 20 (v h 60) (s 7908.71 0.969346 1 129753) (f l 10) (c 0 10 164 0 1 175 3 2 0 0 6)) ((r 1) 0 0x9 40.9819 1.0981 -0.0001 0 -87.985 -90 (v h 180) (s 8000 1 1 129802) (f r 11) (c 0 12 499 0 1 512 1 2 0 0 9)) ((r 2) 15 0x1 16.1943 4.7782 -0.0108 -0.0032 -73.725 -90 (v h 60) (s 7831.38 0.879543 1 129729) (f r 11) (c 0 17 433 0 1 451 3 1 0 0 7)) ((r 3) 5 0x1 16.2456 -3.3864 -0.0024 -0.0002 78.121 90 (v h 60) (s 7991.62 0.908495 1 129653) (f r 11) (c 0 14 405 0 1 420 3 2 0 0 7)) ((r 4) 4 0x1 15.8106 12.998 -0.0014 -0.0005 -80.211 -90 (v h 120) (s 7950.49 0.979394 1 129615) (f r 11) (c 0 15 373 0 1 389 2 2 0 0 9)) ((r 5) 11 0x1 16.0814 -14.9931 -0.0008 0.0001 46.849 90 (v h 120) (s 8000 0.965419 1 129734) (f r 11) (c 0 12 345 0 1 358 2 2 0 0 7)) ((r 6) 17 0x1 10.125 0 0 0 -90.387 -90 (v h 60) (s 8000 0.801842 1 130600) (f r 11) (c 0 0 325 0 1 326 3 2 0 0 9)) ((r 7) 6 0x1 10.8481 9.1235 -0 -0 -49.726 -90 (v h 60) (s 8000 0.85015 1 130114) (f r 11) (c 0 8 286 0 1 295 3 2 0 0 8)) ((r 8) 7 0x1 10.8254 -9.4647 0 0 49.009 90 (v h 60) (s 8000 0.904061 1 130036) (f r 11) (c 0 8 255 0 1 264 3 2 0 0 8)) ((r 9) 16 0x1 6.6687 22.0487 0 -0 -16.751 -90 (v h 120) (s 8000 0.969346 1 130200) (f r 11) (c 0 4 228 0 1 233 2 2 0 0 9)) ((r 10) 3 0x1 6.1831 -21.9342 0 0 16.103 90 (v h 120) (s 8000 0.983479 1 130200) (f r 11) (c 0 4 197 0 1 202 2 2 0 0 5)) ((r 11) 10 0x1 8.5269 -4.4187 -0 -0 62.533 90 (v h 60) (s 8000 0.943286 1 129957) (f r 6) (c 0 10 160 0 1 171 2 2 0 0 8)))"
# print(read_line2.parseString(rcg_line))

# plus 12
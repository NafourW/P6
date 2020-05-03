from threading import Thread
from parsers.rclParser import rclParsing
from parsers.rcgParser import rcgParsing
from pyparsing import ParseException
from math import sqrt
import heapq
import os
from math import sqrt
from time import sleep
from gensim.models import Word2Vec


class ReadWriteLogFiles:
    # .rcg variables
    t1_ball_possesion = []
    t2_ball_possesion = []
    ball_location_history = []

    # Word2Vec
    last_player_with_ball = -1
    next_player = -1
    success = []
    w2vList = []

    # parsers
    rcgParser = rcgParsing()
    rclParser = rclParsing()


    # global variables
    score_alarm = 0
    latest_player_possessing_ball = []
    score_player = None  # name of the player who got the latest goal
    scored_players = []
    scored_players_frames = []


    def multiThreadRWFiles(self, rcg_file, rcl_file):
        self.rcg_file = rcg_file
        self.rcl_file = rcl_file

        Thread(target = self.readLogFileRCL).start()
        Thread(target = self.readLogFileRCG).start()

    
    def inference_run(self, rcg_file, rcl_file):
        self.rcg_file = rcg_file
        self.rcl_file = rcl_file

        Thread(target = self.inferenceRCL).start()
        Thread(target = self.inferenceRCG).start()
        
        '''
        while int(self.rcgParser.current_frame) != int(self.rclParser.current_frame):
            if int(self.rcgParser.current_frame) > int(self.rclParser.current_frame):
                print("rcg is too fast")
            elif int(self.rcgParser.current_frame) < int(self.rclParser.current_frame):
                print("rcl is too fast")
        '''
        

    def readLogFileRCG(self):
        with open("logfiles/" + self.rcg_file, "r") as file:
            counter = 0
            line = file.readline()
            self.score_alarm = self.rcgParser.goal_alarm
            sleep(5)
            while True:

                if self.rcgParser.is_game_end == True:
                    break
                else:
                    try:
                        '''
                        while int(self.rcgParser.current_frame) != int(self.rclParser.current_frame):
                            if int(self.rcgParser.current_frame) > int(self.rclParser.current_frame):
                                print("rcg is too fast, rcg frame: " + self.rcgParser.current_frame + " rcl frame: " + self.rclParser.current_frame)
                            else:
                                break
                        '''

                        counter += 1
                        self.rcgParser.strParsing(line)

                        if (len(self.latest_player_possessing_ball) > 10):
                            self.latest_player_possessing_ball.remove(self.latest_player_possessing_ball[0])

                        # When goal detected
                        '''
                        if self.rcgParser.goal_alarm == True:
                            self.rcgParser.goal_alarm = False
                        '''

                        # If it is a frame save the location of the ball
                        if "show" in line:
                            ball_info = self.rcgParser.get_ball_info(line)
                            player_info = self.rcgParser.get_player_info(line)
                            
                            self.ball_possesion_statistics(ball_info, player_info)
                            '''
                            player_Ball = str(self.get_player_number_possesing_ball(ball_info, player_info))
                            print("Frame: " + self.rcgParser.current_frame + "  " + player_Ball + " has the ball!")
                            '''
                            # Find out whether the ball is on the left or right side of the playing field
                            if float(ball_info["pos_x"]) > 0:
                                self.ball_location_history.append("left")
                            elif float(ball_info["pos_x"]) < 0:
                                self.ball_location_history.append("right")
                        
                        # Every 1000 frames, print statistics
                        if counter % 100 == 0:
                            self.print_ball_possesion_statistics()
                            self.print_ball_location_statistics()
                        
                        # Detect for player scoring
                        if self.rcgParser.goal_alarm > self.score_alarm:
                            self.get_player_scored()

                    except ParseException as e:
                        print(e)
                        break

                    line = file.readline()

            # TRAINING
            with open('output.txt', 'w') as f:
                for index in ReadWriteLogFiles.w2vList:
                    f.write(str(index) + '\n')
            
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcg file"

            print(error_line)


    def readLogFileRCL(self):
        with open("logfiles/" + self.rcl_file, "r") as file:
            counter = 0
            line = file.readline()

            while True:
                if self.rclParser.is_game_end == True:
                    break
                else:
                    try:
                        '''
                        while int(self.rcgParser.current_frame) != int(self.rclParser.current_frame):
                            if int(self.rcgParser.current_frame) < int(self.rclParser.current_frame):
                                print("rcl is too fast, rcl frame: " + self.rclParser.current_frame + " rcg frame: " + self.rcgParser.current_frame)
                            else:
                                break
                        '''
                                
                        counter += 1
                        self.rclParser.strParsing(line)

                    except ParseException as e:
                        print(e)
                        break

                    line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcl file"
            print(error_line)


    def inferenceRCG(self):
        with open("logfiles/" + self.rcg_file, "r") as file:
            line = file.readline()
            
            while True:
                if self.rcgParser.is_game_end == True:
                    break
                else:
                    self.rcgParser.strParsing(line)

                    # If it is a frame save the location of the ball
                    if "show" in line:

                        ball_info = self.rcgParser.get_ball_info(line)
                        player_info = self.rcgParser.get_player_info(line)

                        player_Ball = self.get_player_number_possesing_ball(ball_info, player_info)
                        
                        # If the player with the ball is not the same as last frame
                        if player_Ball is not None and self.last_player_with_ball != player_Ball:

                            # If the player with the ball is the one W2V guessed 
                            if str(player_Ball) == self.next_player:
                                self.success.append(1)
                                print("Correct!")

                            print("Frame: " + str(self.rcgParser.current_frame))
                            print("Player: " + str(player_Ball) + " has the ball")

                            most_similar = self.w2v_most_similar(player_Ball)[0]
                            print("Most similar : " + str(most_similar))
                            self.next_player = most_similar[0]
                    
                        self.last_player_with_ball = player_Ball

                    line = file.readline()

    
    def inferenceRCL(self):
        with open("logfiles/" + self.rcl_file, "r") as file:
            line = file.readline()
            
            while True:
                if self.rclParser.is_game_end == True:
                    break
                else:
                    self.rclParser.strParsing(line)
                    line = file.readline()

    
    def print_ball_location_statistics(self):
        ball_location_history_size = len(self.ball_location_history)

        # Make sure not to divide by 0
        if ball_location_history_size != 0:
            print("Ball on Left side of field percentage: %.0f%%" 
                % float((self.ball_location_history.count("left") / ball_location_history_size * 100)))
            print("Ball on Right side of field percentage: %.0f%%" 
                % float((self.ball_location_history.count("right") / ball_location_history_size * 100)))
            print("")


    def print_ball_possesion_statistics(self):
        # Calculate the possesion statistics
        t1_ball_possesion_size = len(self.t1_ball_possesion)
        t2_ball_possesion_size = len(self.t2_ball_possesion)

        # Make sure not to divide by zero
        if t1_ball_possesion_size != 0 or t2_ball_possesion_size != 0:
            print("Team 1 ball possesion percentage: %.2f%%" % (float(t1_ball_possesion_size / (t1_ball_possesion_size + t2_ball_possesion_size)) * 100))
            print("Team 2 ball possesion percentage: %.2f%%" % (float(t2_ball_possesion_size / (t1_ball_possesion_size + t2_ball_possesion_size)) * 100))
            print("")


    def ball_possesion_statistics(self, ball_info, player_info):
        player_possesing = self.get_player_number_possesing_ball(ball_info, player_info)
        
        # Save who possesed the ball
        if player_possesing is not None:

            # If the player possesing the ball is from team 1
            if player_possesing <= 11:
                self.t1_ball_possesion.append("team1")
            elif player_possesing > 11:
                self.t2_ball_possesion.append("team2")


    def get_player_number_possesing_ball(self, ball_info, player_info):
        closest_distance = 3
        player_possesing = None

        # If the ball is not in the starting position
        if float(ball_info["pos_x"]) != 0 or float(ball_info["pos_y"]) != 0:
            
            # Find out which player is possesing the ball, if any
            for player_number in range(1, 23):
                
                pos_x_player = float(player_info[str(player_number)]["pos_x"])
                pos_y_player = float(player_info[str(player_number)]["pos_y"])

                pos_x_ball = float(ball_info["pos_x"])
                pos_y_ball = float(ball_info["pos_y"])

                pow1 = pow((pos_x_player - pos_x_ball), 2)
                pow2 = pow((pos_y_player - pos_y_ball), 2)

                # Distance from player to ball
                distance = sqrt(pow1 + pow2)
                
                # If a player is within 5 units of the ball and closer than any other
                if distance <= 2 and distance < closest_distance: 
                    closest_distance = distance
                    player_possesing = player_number
        
        # Store the player who last possessed the ball within a specific frame
        if player_possesing is not None:
            if int(player_possesing) > 11:
                self.latest_player_possessing_ball.append([self.rcgParser.current_frame, str(self.rclParser.team_name_r) + '_' + str(int(player_possesing) - 11)])
            elif int(player_possesing) < 12:
                self.latest_player_possessing_ball.append([self.rcgParser.current_frame, str(self.rclParser.team_name_l) + '_' + str(player_possesing)])

        return player_possesing


    def get_distance_from_player_to_team(self, player_number, player_info):
        distance = {}

        # Team 1
        if player_number <= 11:
            for compare_player_number in range(1, 12):

                # If the two players we are comparing are not the same
                if compare_player_number != player_number:

                    pos_x_player = float(player_info[str(player_number)]["pos_x"])
                    pos_y_player = float(player_info[str(player_number)]["pos_y"])

                    pos_x_compare = float(player_info[str(compare_player_number)]["pos_x"])
                    pos_y_compare = float(player_info[str(compare_player_number)]["pos_y"])

                    pow1 = pow(pos_x_player - pos_x_compare, 2)
                    pow2 = pow(pos_y_player - pos_y_compare, 2)

                    distance[compare_player_number] = sqrt(pow1 + pow2)
        # Team 2
        elif player_number > 11:
            for compare_player_number in range(1, 12):

                # If the two players we are comparing are not the same
                if compare_player_number != player_number:

                    pos_x_player = float(player_info[str(player_number)]["pos_x"])
                    pos_y_player = float(player_info[str(player_number)]["pos_y"])

                    pos_x_compare = float(player_info[str(compare_player_number)]["pos_x"])
                    pos_y_compare = float(player_info[str(compare_player_number)]["pos_y"])

                    pow1 = pow(pos_x_player - pos_x_compare, 2)
                    pow2 = pow(pos_y_player - pos_y_compare, 2)

                    distance[compare_player_number] = sqrt(pow1 + pow2)

        return distance


    def get_stamina_of_players(self, player_info):
        stamina = {}

        for player_number in range(1, 23):
            stamina[str(player_number)] = [
                player_info[str(player_number)]["stamina"], 
                player_info[str(player_number)]["stamina_capacity"]
            ]

        return stamina


    def get_player_scored(self):
        last_kicker = None

        if (len(self.rclParser.latest_player_kick) > 0) and (len(self.latest_player_possessing_ball) > 0):

            score_player_found = False
            while score_player_found == False:

                i = (len(self.rclParser.latest_player_kick) - 1)
                j = (len(self.latest_player_possessing_ball) - 1)

                if self.rclParser.latest_player_kick[i][0] == self.latest_player_possessing_ball[j][0]:
                    if self.rclParser.latest_player_kick[i][1] == self.latest_player_possessing_ball[j][1]:
                        self.score_player = self.latest_player_possessing_ball[j][1]
                        self.scored_players.append(self.score_player)
                        self.scored_players_frames.append(self.rcgParser.goal_frame)
                        #print("SCORE PLAYER: " + self.score_player + " (ALL GOOD)")
                        score_player_found = True
                        self.score_alarm += 1
                    else:
                        self.latest_player_possessing_ball.remove(self.latest_player_possessing_ball[j])
                else:
                    if int(self.rclParser.current_frame) >= int(self.rcgParser.goal_frame):
                        last_kicker = self.rclParser.latest_player_kick[i]
                        rcg_index = (len(self.latest_player_possessing_ball) - 1)
                        while rcg_index > 0:
                            if last_kicker[0] == self.latest_player_possessing_ball[rcg_index][0]:
                                if last_kicker[1] == self.latest_player_possessing_ball[rcg_index][1]:
                                    self.score_player = self.latest_player_possessing_ball[rcg_index][1]
                                    self.scored_players.append(self.score_player)
                                    self.scored_players_frames.append(self.rcgParser.goal_frame)
                                    #print("SCORE PLAYER: " + self.score_player)
                                    score_player_found = True
                                    self.score_alarm += 1
                                    rcg_index = 0
                                else:
                                    rcg_index -= 1
                            else:
                                rcg_index -= 1

                    if self.rclParser.latest_player_kick[i][0] < self.latest_player_possessing_ball[j][0]:
                        sleep(2)
                    elif self.rclParser.latest_player_kick[i][0] > self.latest_player_possessing_ball[j][0]:
                        print("score_player_found: " + str(score_player_found)) # cannot find any player who scored


    def Word2VecTextCorpus(self, ball_info, player_info, player_Ball):
        newList = []

        if player_Ball is None:
            pass
        else:
            n_player = self.get_distance_from_player_to_team(player_Ball, player_info)
            print("Frame: " + self.rcgParser.current_frame + "  " + str(player_Ball) + " has the ball!")
            # ReadWriteLogFiles.w2vList.append(player_Ball)
            # ReadWriteLogFiles.w2vList.append(heapq.nsmallest(3, n_player.values()))
            top3 = {k: n_player[k] for k in sorted(n_player, key=n_player.get)}

            newList.append(player_Ball)
            newList.append(list(top3.keys())[:3])
            ReadWriteLogFiles.w2vList.append(newList)
            #print(ReadWriteLogFiles.w2vList)
        '''
        with open('output.txt', 'w') as f:
            f.write(str(ReadWriteLogFiles.w2vList))
            for _list in mylist:
                for _string in _list:
                    #f.seek(0)
                    f.write(str(_string) + '\n')
        '''


    def w2v_most_similar(self, player_number):
        if player_number is not None:
            model = Word2Vec.load('trainedModel/word2vec.model')
            return model.wv.most_similar(str(player_number),topn=1)

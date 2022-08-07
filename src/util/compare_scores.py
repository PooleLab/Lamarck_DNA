
# Modified version of Needleman-Wunsch algorithm to compare differnt music-score text files

import numpy as np  # zero matrices, arrays, .max(), linspace

log_writer = None


def log_to_file(content):
    print(content)
    global log_writer
    if log_writer is None:
        log_writer = open("../output/scores/comparisons.log", "a")
    log_writer.write(content + "\n")


class CompareScores:

    def __init__(self, score_file_1, score_file_2, output_log_dir):
        self.score_file_1 = score_file_1
        self.score_file_2 = score_file_2
        self.output_log_dir = output_log_dir
        global log_writer
        log_writer = open(self.output_log_dir, "a")

    def get_scores_from_files(self):
        score_1_contents: str = ""
        score_2_contents: str = ""
        with open(self.score_file_1, "r") as score_1_tab:
            score_1_contents = score_1_tab.readline()

        with open(self.score_file_2, "r") as score_2_tab:
            score_2_contents = score_2_tab.readline()

        score_1_contents = score_1_contents.replace("\n", "")
        score_2_contents = score_2_contents.replace("\n", "")
        # print(score_1_contents)
        # print(score_2_contents)
        return score_1_contents, score_2_contents

    @staticmethod
    def compare(score_1, score_2):
        sequence_1 = score_1.split(",")
        sequence_2 = score_2.split(",")

        # Create Matrices
        main_matrix = np.zeros((len(sequence_1) + 1, len(sequence_2) + 1))
        match_checker_matrix = np.zeros((len(sequence_1), len(sequence_2)))

        # Providing the scores for match, mismatch and gap
        match_reward = 5
        near_match_reward = 3
        mismatch_penalty = 0
        gap_penalty = -2

        # Fill the match checker matrix according to match, near match or mismatch
        for i, note_1 in enumerate(sequence_1):
            note_details1 = note_1.split("-")
            for j, note_2 in enumerate(sequence_2):
                note_details2 = note_2.split("-")
                if (note_details1[0] == note_details2[0]) and (note_details1[1] == note_details2[1]):
                    match_checker_matrix[i][j] = match_reward
                elif (note_details1[0] == note_details2[0]) and (note_details1[1] != note_details2[1]):
                    match_checker_matrix[i][j] = near_match_reward
                else:
                    match_checker_matrix[i][j] = mismatch_penalty

        # print(match_checker_matrix)

        # Filling up the matrix using Needleman_Wunsch algorithm
        # STEP 1 : Initialisation
        for i in range(len(sequence_1) + 1):
            main_matrix[i][0] = i * gap_penalty
        for j in range(len(sequence_2) + 1):
            main_matrix[0][j] = j * gap_penalty

        # STEP 2 : Matrix Filling
        for i in range(1, len(sequence_1) + 1):
            for j in range(1, len(sequence_2) + 1):
                main_matrix[i][j] = max(main_matrix[i - 1][j - 1] + match_checker_matrix[i - 1][j - 1],
                                        main_matrix[i - 1][j] + gap_penalty,
                                        main_matrix[i][j - 1] + gap_penalty)

        # print(main_matrix)
        log_to_file("Score: " + str(main_matrix[-1][-1]))

        # STEP 3 : Traceback

        ti = len(sequence_1)
        tj = len(sequence_2)

        tab_spacing = "  "

        first_sequence = []
        second_sequence = []
        while ti > 0 and tj > 0:

            if (ti > 0 and tj > 0 and
                    main_matrix[ti][tj] == main_matrix[ti - 1][tj - 1] + match_checker_matrix[ti - 1][tj - 1]):

                first_sequence.append(sequence_1[ti - 1])
                second_sequence.append(sequence_2[tj - 1])

                ti = ti - 1
                tj = tj - 1

            elif ti > 0 and main_matrix[ti][tj] == main_matrix[ti - 1][tj] + gap_penalty:

                first_sequence.append(sequence_1[ti - 1])
                second_sequence.append("-")

                ti = ti - 1
            else:
                first_sequence.append("-")
                second_sequence.append(sequence_2[tj - 1])

                tj = tj - 1

        first_sequence.reverse()
        second_sequence.reverse()

        first_str = ""
        mid_bar = ""
        second_str = ""

        total_len = len(first_sequence)

        for i in range(total_len):
            first_note = first_sequence[i]
            second_note = second_sequence[i]
            element_details_1 = first_note.split("-")
            element_details_2 = second_note.split("-")
            bar_length = max(len(first_note), len(second_note))

            extra_space_1 = (bar_length - len(first_note)) * " "
            extra_space_2 = (bar_length - len(second_note)) * " "

            if (element_details_1[0] == element_details_2[0]) and (element_details_1[1] == element_details_2[1]):
                first_str += first_note + extra_space_1 + tab_spacing
                second_str += second_note + extra_space_1 + tab_spacing
                mid_bar += "|" + (" " * (bar_length-1)) + tab_spacing
            elif (element_details_1[0] == element_details_2[0]) and (element_details_1[1] != element_details_2[1]):
                first_str += first_note + extra_space_1 + tab_spacing
                second_str += second_note + extra_space_2 + tab_spacing
                mid_bar += "." + (" " * (bar_length - 1)) + tab_spacing
            else:
                first_str += first_note + extra_space_1 + tab_spacing
                second_str += second_note + extra_space_2 + tab_spacing
                mid_bar += (" " * bar_length) + tab_spacing

        log_to_file(first_str)
        log_to_file(mid_bar)
        log_to_file(second_str)

    def load_and_compare(self):
        scores = self.get_scores_from_files()

        # score_1 = "E5-0.5,D5-0.125,E5-0.5,D5-1.0".split(",")
        # score_2 = "E5-0.5,D5-0.125,D5-1.0".split(",")
        score_1 = scores[0].split(",")
        score_2 = scores[1].split(",")

        log_to_file("Comparing files: [" + self.score_file_1 + "] and [" + self.score_file_2 + "] ")

        # print(score_1)
        # print(score_2)

        CompareScores.compare(scores[0], scores[1])

import json

# Defining Commands
class Config:

    DNA_BUFFER_SIZE = 4
    POSSIBLE = 'AGCT'
    COMMANDS = ["generate-music", "generate-dna", "split-midi", "generate-tabs",
                "generate-midi", "mutation-wf", "synonymous-wf", "randomised-wf",
                "correct-midi", "compare-scores"]
    COMMAND_ARGS = ["-in", "-out", "-tempo", "-n"]

    def __init__(self):
        pass

    @staticmethod
    def load_dict():
        with open("configurations/config.json") as config_data:
            config_dict = json.load(config_data)

        return config_dict['data']



# Parent converter-class that can be inherited by all child-converter scripts
class Converter:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        print("Converting files {} -> {}", self.input_file, self.output_file)
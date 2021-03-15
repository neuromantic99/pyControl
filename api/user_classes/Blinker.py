from api.api import Api

class Blinker(Api):
    # API for the Blinker class demonstrating setting variables functionality.

    def __init__(self):
        self.i = 0

    def process_data_user(self, data):

        # Has the board transitioned into LED_off state?
        LED_off = any([state.name == 'LED_off' for state in data['states']])

        if LED_off:
            self.i = (self.i + 1) % 4
            self.set_variable('LED_n', self.i+1)


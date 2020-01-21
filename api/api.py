import matplotlib.pyplot as plt
import numpy as np

class Api():
    '''list of the function availble to api classes'''

    def __init__(self):
        pass
    
    def interface(self, board, print_to_log):
        # Connect Api with pyboard and gui.
        self.board = board
        self.print_to_log = print_to_log
        self.ID2name = self.board.sm_info['ID2name']

    def set_state_machine(self, sm_info):
        pass

    def run_start(self, recording):
        pass

    def run_stop(self):
        pass

    def update(self):
        pass

    def process_data(self, new_data):
        pass

    def set_variable(self, v_name, v_value):
        if v_name in self.board.sm_info['variables'].keys(): 
            self.board.set_variable(v_name, v_value)
        else:
            self.print_to_log('Variable {} not defined in task file {} so '
                              'cannot be set be API'
                              .format(v_name, self.board.sm_info['name']))

    def setup_figure(self):

        ''' Assign figure and ax attributes to api. A grid of subplots is built
            if called as part of an experiment with one plot for each setup '''

        if not hasattr(self, 'experiment_info'):  # API used as part of task
            self.figure = plt.figure()
            self.ax = self.figure.add_subplot(111)
            return

        subjects = self.experiment_info['subjects']

        n_plots = len(subjects)
        sr =  np.sqrt(n_plots)
        # Calculate a subplot arrangement for n_plots
        if np.ceil(sr) == np.floor(sr):
            n_rows = n_cols = sr
        else:
            n_cols = np.ceil(sr)
            n_rows = np.ceil(n_plots / n_cols)

        self.figure = plt.gcf()
        self.ax = self.figure.add_subplot(n_rows, n_cols, self.setup_idx+1)
        self.ax.set_title(list(subjects.values())[self.setup_idx])

    @classmethod
    def set_experiment_info(cls, experiment_info, setup_idx):
        ''' instantiate API superclass with experiment info
            if called from an experiment. Info available
            user class on init'''
        cls.experiment_info = experiment_info
        cls.setup_idx = setup_idx


    # Note:  get_variable functionality not implemented because board.get_variable method 
    # does not return variable value when framework is running, just causes it to be output
    # by the board as soon as possible.




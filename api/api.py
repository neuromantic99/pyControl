import matplotlib.pyplot as plt
import numpy as np

class Api():

    # ----------------------------------------------------------
    # Functions that the user can overwrite
    # ----------------------------------------------------------

    def __init__(self):
        ''' User Api class is initialised when the task is uploaded
        to the board
        '''
        pass
    
    def set_state_machine(self, sm_info):
        ''' Im not sure that we need this?
        The interface function gives access to board object
        which has sm_info
        '''
        pass

    def run_start(self):
        ''' Called once when the task is started'''
        pass

    def run_stop(self):
        ''' Called once when the task is stopped'''
        pass

    # GIVE ME A NEW NAME?
    def process_data_user(self, data):

        ''' Called whenever there is a state transition, event
        or printed line. Gives the user access to data dictionary

        data : a dictionary with keys 'states', 'events' and 'prints'
               and values a list of tuples in format
               (name of state or event / printed string, time)

        '''

        pass

    def update(self):
        ''' Called several times / second regardless of whether
        there is a state transition or event.

        The user should be cautious when overwriting this function
        as code that does not execute in sub-millisecond time will
        impact the performance of pyControl
        '''
        pass


    # ----------------------------------------------------------
    # User can call these functions
    # ----------------------------------------------------------

    def set_variable(self, v_name, v_value):

        ''' Call this function to change the value of a task
        variable.

        v_name : str
            name of variable to change
        v_value :
            value to change variable to

        '''

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
        # self.ax.set_title(list(subjects.values())[self.setup_idx])
        self.ax.set_title(list(subjects.keys())[self.setup_idx])

    # ----------------------------------------------------------
    # User should not overwrite or call these functions
    # ----------------------------------------------------------

    def interface(self, board, print_to_log):
        # Connect Api with pyboard and gui.
        self.board = board
        self.print_to_log = print_to_log
        self.ID2name = self.board.sm_info['ID2name']

    def process_data(self, new_data):
        ''' User doesnt call or overwrite this function. 
        Called by the gui 
        every time there is new data. Processes new_data from
        the board and processes it to a user friendly data
        structure. Then passes new data structure to
        process_data_user.

        Im not totally happy with this data structure
        because the user still needs to iterate through
        a list of tuples, could nested dictionaries or named
        tuples be better?
        '''


        data = {'states': [],
                'events': [],
                'prints': []
               }

        for nd in new_data:
            if nd[0] == 'P':
                data['prints'].append((nd[2], nd[1]))
            elif nd[0] == 'D':
                name = self.ID2name[nd[2]]
                if name in self.board.sm_info['states']:
                    data['states'].append((name, nd[1]))
                else:
                    data['events'].append((name, nd[1]))

        self.process_data_user(data)

    @classmethod
    def set_experiment_info(cls, experiment_info, setup_idx):

        ''' User should not overwrite this.
            Calling this function as a classmethod allows
            the gui to make available variables to the user
            before the user's class is instantiated.
            
            This provides information about the experiment to each
            setup.

            '''
        cls.experiment_info = experiment_info
        cls.setup_idx = setup_idx


    # Note:  get_variable functionality not implemented because board.get_variable method 
    # does not return variable value when framework is running, just causes it to be output
    # by the board as soon as possible.




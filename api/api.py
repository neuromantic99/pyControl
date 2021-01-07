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

        ''' Creates a figure for each setup and assigns figure 
        and ax attributes to user class api. 
        Sets the title of the figure to subject ID if called as
        part of an experiment
        '''

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

        # Set plot title to API used as part of experiment
        if hasattr(self, 'experiment_info'):  
            self.ax.set_title(self.subject_id)


    # ----------------------------------------------------------
    # User should not overwrite or call these functions
    # ----------------------------------------------------------

    def interface(self, board, print_to_log):
        ''' Called once when task is uploaded and api is initialised.
        Gives api access to board object and print_to_log method
        '''

        # Connect Api with pyboard and gui.
        self.board = board
        self.print_to_log = print_to_log
        self.ID2name = self.board.sm_info['ID2name']

    def process_data(self, new_data):
        ''' Called directly by the gui every time there is new data.
        Recieves new_data from the board and processes it to a user 
        friendly data structure. Then passes new data structure to
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

    def api_communication(self, APIs):
        ''' Gives the api class access to the other api 
        instantiations in an experiment. Allows for example
        one setup to change variables on another.
        '''
        self.other_APIs = APIs

    @classmethod
    def set_experiment_info(cls, experiment_info, setup_idx):

        ''' Gives the user access to info about the experiment
        upon instantiation of the user api class.
        '''
        # Info about the experiment, incuding other subjects
        cls.experiment_info = experiment_info
        # The index of this setup
        cls.setup_idx = setup_idx
        # The subject ID of this setup
        cls.subject_id = list(experiment_info['subjects']
                               .keys())[setup_idx]

    # Note:  get_variable functionality not implemented because board.get_variable method 
    # does not return variable value when framework is running, just causes it to be output
    # by the board as soon as possible.




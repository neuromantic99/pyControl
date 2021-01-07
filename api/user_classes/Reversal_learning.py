from api.api import Api
import matplotlib.pyplot as plt

plt.rcParams['toolbar'] = 'None'              # Disable Matplotlib figure toolbar.
plt.rc("axes.spines", top=False, right=False) # Disable top and right axis spines.

class Reversal_learning(Api):
    '''API for the reversal_learning task to demonstrate Matplotlib plotting.'''

    def __init__(self):
        self.mov_avs = [] # List to hold trial by trial choice moving average.
        # Setup plot figure.
        self.setup_figure()
        self.ax.set_ylim((0,1))
        self.ax.set_xlim(0.5,5.5)
        self.ax.set_xlabel('Trial Number')
        self.ax.set_ylabel('Moving Average of Choices')
        self.line = self.ax.plot([], [], '*-b')[0]
        plt.show()

    def run_start(self):
        self.print_to_log('\nUsing api to plot reversal learning moving average of choices')

    def process_data_user(self, data):
        '''If a trial summary print line is in the data, extract the 
        choice moving average and update_plot.'''

        # Printed line is trial summary.        
        trial_summary = [p[0] for p in data['prints'] if 'T#' in p[0]]

        if trial_summary:

            # Extract moving average.
            mov_ave = trial_summary[0].split(':')[-1]
            self.mov_avs.append(float(mov_ave))
            # Update the plot data and x axis limits.
            x = list(range(1,len(self.mov_avs)+1))
            self.line.set_data(x, self.mov_avs)
            self.ax.set_xlim(right=max(x[-1]+0.5, 5.5))
            self.figure.canvas.draw()


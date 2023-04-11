# imports

# module imports
from modules.AnalyticSolution import AnalyticSolutionKarman

def main():
    #dataloader = DataLoader()
    karman_analytic_streamlines = AnalyticSolutionKarman(a=5, b=0.5, Gamma=1)
    karman_analytic_streamlines.plot_steady_karman_streamlines()

# imports

# module imports
from modules.DataLoader import DataLoader
from modules.AnalyticSolution import AnalyticSolutionKarman

def main():
    #dataloader = DataLoader()
    karman_analytic_streamlines = AnalyticSolutionKarman(a=5, b=0.5, Gamma=1)
    karman_analytic_streamlines()

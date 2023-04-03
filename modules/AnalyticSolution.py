import matplotlib.pyplot as plt
import numpy as np

class AnalyticSolutionKarman():
    """
    Plotting the analytic solution of the Karman Vortex
    """
    def __init__(self, a=5, b=0.5, Gamma=1):
        self.a = a
        self.b = b
        self.Gamma = Gamma

    def plot_steady_karman_streamlines(self):
        a = self.a
        b = self.b
        Gamma = self.Gamma
        
        # Define the function for the net velocity potential
        def net_velocity_potential(z):
            zv1 = np.array([2*(n+1)*a+b*1j for n in range(-100, 101)]).reshape(1, 1, 201)
            zv2 = np.array([2*n*a-b*1j for n in range(-100, 101)]).reshape(1, 1, 201)
            return Gamma/(2*np.pi) * (np.sum(-1j/(z.reshape(N, N, 1)-zv1), axis=2) - np.sum(-1j/(z.reshape(N, N, 1)-zv2), axis=2))

        # Create a grid of complex numbers in the complex plane
        N = 1000
        x = np.linspace(-20, 20, N)
        y = np.linspace(-20, 20, N)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j*Y

        # Evaluate the net velocity potential at each point in the complex plane
        W = net_velocity_potential(Z)

        # Plot the magnitude and phase of the net velocity potential
        fig, ax = plt.subplots()
        ax.contourf(X, Y, np.abs(W), levels=50)
        ax.contour(X, Y, np.angle(W), levels=50)
        ax.set_xlabel('Real axis')
        ax.set_ylabel('Imaginary axis')
        plt.show()

import numpy as np
from map import Map
import sys
import time


class ParticleFilter:

    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.particles = np.zeros((num_particles, 3))
        self.weights = np.ones((num_particles, 1))/num_particles
    #print('initial weights = ', self.weights)
    # Experimental for ALL data
    def gaussian_noise_full(self, mu, sigma, rotation=False):
        if rotation == False:
            noise = np.zeros((self.num_particles, 3))
            for i in range(self.num_particles):
                for j in range(3):
                    noise[i][j] = np.random.normal(mu, sigma)
        else:
            noise = np.zeros(self.particles)
            for i in range(3):
                noise[i] = np.random.normal(mu, sigma)
        return noise

    def update_after_straight_line_full(self, D, mu, sigma_e, sigma_f):
        if self.particles.shape != (self.num_particles, 3):
            print("Something is wrong with the shape of self.particles.")
        else:
            noise_e = (sigma_e * np.random.randn(self.num_particles, 1) + mu).reshape(1, self.num_particles)[0]
            noise_f = (sigma_f * np.random.randn(self.num_particles, 1) + mu).reshape(1, self.num_particles)[0]
            self.particles[:, 0] += (D + noise_e) * np.cos(self.particles[:, 2])
            self.particles[:, 1] += (D + noise_e) * np.sin(self.particles[:, 2])
            self.particles[:, 2] += noise_f
        pass

    def update_after_rotation_full(self, rotation_angle, mu, sigma):
        if self.particles.shape != (self.num_particles, 3):
            print("Something is wrong with the shape of self.particles.")
        else:
            for i in range(self.num_particles):
                noise_g = np.random.normal(mu, sigma)
                self.particles[i][2] += rotation_angle + noise_g
        pass

    def estimate_position(self,x):
        x_mean = np.zeros((self.num_particles, 3))
        for i in range(self.num_particles):
            x_mean[i] += x[i]*self.weights[i]
        return np.sum(x_mean, axis=0)

    def estimate_position_from_particles(self):
        x_mean, y_mean, theta_mean = 0., 0., 0.
        for i in range(self.num_particles):
            x_mean += self.particles[i][0] * self.weights[i][0]
            y_mean += self.particles[i][1] * self.weights[i][0]
            theta_mean += self.particles[i][2] * self.weights[i][0]
            #print('particles = ', self.particles[i], 'weight = ', self.weights[i])
            #print('x_mean = ', x_mean, 'y mean = ', y_mean)
        #print('Sum of weights = ', round(np.sum(self.weights)), ', particle 1 = ', self.particles[0])
        state_mean = [x_mean, y_mean, theta_mean]
        return state_mean

    # Returns the closest wall as a list of [distance, Wall name]
    def find_closest_wall(self, x, y, theta, map):
        vertical_walls = ['a', 'c', 'e', 'g']
        horizontal_walls = ['b', 'd', 'f', 'h']
        vertices = map.get_vertices()
        # We set random values for the closest wall, with a big distance to be sure we find a closer one.
        closest_wall = [10000000., 'random wall']
        for wall in vertices:
            # m = Forward Distance to infinite wall passing through (Ax, Ay), (Bx, By)
            Ax = wall[0]
            Ay = wall[1]
            Bx = wall[2]
            By = wall[3]
            t1 = (By - Ay) * (Ax - x)
            t2 = (Bx - Ax) * (Ay - y)
            t3 = (By - Ay) * np.cos(theta)
            t4 = (Bx - Ax) * np.sin(theta)
            m = (t1 - t2) / (t3 - t4)
            # print("distance is ", m, " and wall is ",wall[4])
            # We compute the virtual hitting point to see if it is plausible with regards
            # to the wall vertices coordinates
            meeting_wall_coord = [x + (m * np.cos(theta)), y + (m * np.sin(theta))]
            # If the current wall is a horizontal one, we check that the x coordinate of the hitting point
            # is between the x coordinates of the wall
            if wall[4] in horizontal_walls:
                if (meeting_wall_coord[0] > min(Ax, Bx)) & (meeting_wall_coord[0] < max(Ax, Bx)):
                    if (0 < m) & (m < closest_wall[0]):
                        closest_wall = [m, wall[4]]
            # If the current wall is a vertical one, we check that the y coordinate of the hitting point
            # is between the y coordinates of the wall
            if wall[4] in vertical_walls:
                if (meeting_wall_coord[1] > min(Ay, By)) & (meeting_wall_coord[1] < max(Ay, By)):
                    if (0 < m) & (m < closest_wall[0]):
                        closest_wall = [m, wall[4]]
        return closest_wall

    def calculate_likelihood_full(self, map, z):
        likelihood = []
        for i in range(self.num_particles):
            x = self.particles[i][0]
            y = self.particles[i][1]
            theta = self.particles[i][2]
            likelihood.append(self.calculate_likelihood(x, y, theta, z, map))
        return likelihood

    # The probability of getting measurement z given that x_i represents the true state
    def calculate_likelihood(self, x, y, theta, z, map):
        # Find closest wall the the particule
        start_closest_wall = time.time()
        closest_wall = self.find_closest_wall(x, y, theta, map)
        duration_closest_wall = time.time() - start_closest_wall
        # print('It takes {0:.6f} seconds compute the closest wall.'.format(duration_closest_wall))
        # m = forward distance to the closest hitting point to a wall
        m = closest_wall[0]
        wall_name = closest_wall[1]
        # print("---------------------------")
        # print("Closest wall name = {1}, at distance = {0}, and sonar value is = {2}".format(m, wall_name, z))
        # print("---------------------------")

        # Likelihood should depend on the difference z m
        # Small difference validates particle, big difference weakens it
        # sigma_s is the s.d. of the uncertainty of sensor, K to compensate for constant garbage values
        sigma_s = 1
        K = 0.1
        t5 = (z - m)**2
        likelihood = np.exp((-t5) / (2 * sigma_s**2)) + K
        return likelihood

    # Normalises the weights
    def normalise_weights(self, weights):
        sum_of_weights = np.sum(weights)
        normalised_weights = weights/sum_of_weights
        return normalised_weights

    # Changes self.weights
    def update_weights(self, values):
        array = np.reshape(self.weights,(self.num_particles,1)) * np.reshape(values,(self.num_particles,1))
        self.weights = self.normalise_weights(array)
        #print('update weights', self.weights, 'values = ', values)

    def resampling(self):
        cummul_wgt = np.zeros((self.num_particles + 1, 1))
        c_wgt = 0
        for i in range(self.num_particles):
            c_wgt += self.weights[i]
            cummul_wgt[i+1] = c_wgt
        #print(cummul_wgt)

        new_sample = np.zeros((self.num_particles, 3))
        temp_sample = np.zeros((self.num_particles, 3))  # Temporary
        for i in range(self.num_particles):
            rand_number = np.random.random_sample()
            for j in range(1, self.num_particles):
                if (cummul_wgt[j-1][0] < rand_number) and (rand_number < cummul_wgt[j][0]) :
                    temp_sample[i][:] = self.particles[j-1][:]
        new_sample = temp_sample
	    #print("new sample is ",new_sample)
        self.particles = new_sample
        return self.particles

"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np

from mesa import Model, datacollection
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.modules import ChartModule
from numpy.core.fromnumeric import trace

from .boid import Boid

class BoidFlockers(Model):
    # ABOUT PAGE GOES HERE
    """
    Flocker model class. Handles agent creation, placement and scheduling.\n
\n
    How Illness works...\n 
    The lifecycle (from what we know) is where someone can truly be healthy, somehow pick up the virus and not know if they are infected unless symptoms show or a test is taken, and then after finding out that an individual might be infected, their behaviour changes to distance themselves from other. This can be visualized with this lifecycle:
    
    Healthy -> Unknowingly sick -> Knowingly sick -> Unknowingly Sick -> Healthy


    Other notes:

    Tried adding images to the custom built "SimpleContinuouosModule", apparently it does not take image paths...
    """

    def __init__(
        self,
        population=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
        # slider vars
        transmitDistance=5,
        unknownSickTime=5,
        sickTime=10,
        healthyButContaigious=2,
        timeToSusceptible=90,
        deathPercentage = .034
    ):
        """
        Create a new Flockers model.

        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives.        
        """
        self.population = population
        self.vision = np.rint(transmitDistance * .65)
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        #self.transmitDistance = transmitDistance
        self.unknownSickTime = unknownSickTime
        self.sickTime = sickTime
        self.healthyButContaigious = healthyButContaigious
        self.timeToSusceptible = timeToSusceptible
        self.deathPercentage = deathPercentage
        

        self.make_agents()
        self.redCount = 0
        self.yellowCount = 1
        self.greenCount = population - 1
        self.yellowCount2 = 0
        self.greenCount2 = 0
        self.ded = 0
        self.running = True
        self.datacollector = datacollection.DataCollector(
            {
                "Boids": lambda m: m.schedule.get_agent_count(),
                "infected": lambda m: m.redCount,
                "unkowingly_contaigious": lambda m:m.yellowCount,
                "Healthy": lambda m: m.greenCount,
                "Died": lambda m: m.ded,
                "unknowingly_contaigious-recovering": lambda m: m.yellowCount2,
                "Recovered": lambda m: m.greenCount2,
            }
        )


    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        for i in range(self.population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            # this just makes the first node infected.
            if i == 1:
                boid = Boid(
                    i,                   # unique id
                    2,                   # color, 1 = green/healthy, and 2 = yellow/contaigious, 3 = red/sick
                    self,                # model
                    pos,                 # pos
                    self.speed,          # speed
                    velocity,            # velocity
                    self.vision,         # self.vision
                    self.separation,     # separation
                    self.unknownSickTime, # time before the host understands they are sick (yellow)
                    self.sickTime,
                    self.healthyButContaigious,
                    self.timeToSusceptible,
                    **self.factors       # cohere, separate, match
                )
            else:
                boid = Boid(
                    i,
                    1,
                    self,
                    pos,
                    self.speed,
                    velocity,
                    self.vision,
                    self.separation,
                    self.unknownSickTime,
                    self.sickTime,
                    self.healthyButContaigious,
                    self.timeToSusceptible,
                    **self.factors
                )
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


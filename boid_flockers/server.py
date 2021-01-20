from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import SocketHandler
from mesa.visualization.modules import ChartModule
from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement
import subprocess

class DisplayText(TextElement):
    def __init__(self):
        pass
    def render(self,model):
        return "ContainerID: " + subprocess.check_output(["hostname"]).decode('UTF-8')

def boid_draw(agent):
    portrayal = {}

    if agent.color == 1:
        return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Green"}
    elif agent.color == 2 or agent.color == 4:
        return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "#DFDF00"}
    elif agent.color == 5:
        return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "#0000AA"}
    elif agent.color == 6:
        return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "#000000"}
    else: # agent.color == 3
        return {"Shape": "circle", "r": 3, "Filled": "true", "Color": "Red"}


boid_canvas = SimpleCanvas(boid_draw, 500, 500)
chart_stuff = ChartModule([{"Label": "Healthy", "Color": "#00AA00"},
                           {"Label": "unkowingly_contaigious", "Color": "#AAAA00"},
                           {"Label": "infected", "Color": "#AA0000"},
                           {"Label": "unkowingly_contaigious-recovering", "Color": "#AAAA00"},
                           {"Label": "Recovered", "Color": "#0000AA"},
                           {"Label": "Died", "Color": "#000000"}])

model_params = {
    "population": 100,
    "width": 100,
    "height": 100,
    "speed": 5,
    "vision": 10,
    "separation": 2,
    "transmitDistance": UserSettableParameter("slider", "Distance of transmittance (feet)", 5, 2, 10),
    "unknownSickTime": UserSettableParameter("slider", "Time till host awareness (days)", 5, 1, 20),
    "sickTime": UserSettableParameter("slider", "illness duration (days)",10, 5, 100),
    "healthyButContaigious": UserSettableParameter("slider", "Healthy but contaigious time (days)", 4, 0, 100),
    "timeToSusceptible": UserSettableParameter("slider", "Duration of Antibody Defense (days)", 90, 7, 180),
    "deathPercentage": UserSettableParameter("slider", "Mortality Rate (%)", 3.4, 1,15.0) 
}

class SocketHandler(SocketHandler):
    def check_origin(self, origin):
        return True


server = ModularServer(BoidFlockers, [boid_canvas,chart_stuff,DisplayText()], "Covid-19", model_params, )

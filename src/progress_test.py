from builtins import range
import MalmoPython
import os
import sys
import time
import json
from collections import Counter
import takess
import predict
import random

MINECRAFT_WORLDS = "C:\\Malmo2\\Minecraft\\run\\saves\\"

MODEL_NAME = 'conv_network_full.h5'  # this should stay the same
INPUT_FOLDER = "C:\\Malmo2\\CS175_Homework\\Data_Miners\\src\\Test"  # change this to your own location


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)

x_value = '''"''' + str(random.randint(1,50000)) + '''"'''
y_value = '''"90"'''
z_value = '''"''' + str(random.randint(1,50000)) + '''"'''


def create_mission(biome):
    missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

                  <About>
                    <Summary>Biome Classification</Summary>
                  </About>

                  <ServerSection>
                    <ServerInitialConditions>
                      <Time>
                          <StartTime>1000</StartTime>
                          <AllowPassageOfTime>false</AllowPassageOfTime>
                      </Time>
                      <Weather>clear</Weather>
                    </ServerInitialConditions>
                    <ServerHandlers>
                      <FileWorldGenerator src="''' + MINECRAFT_WORLDS + biome + '''"/>
                    </ServerHandlers>
                  </ServerSection>

                  <AgentSection mode="Creative">
                    <Name>Data_Miner</Name>
                    <AgentStart>
                        <Placement x='''+x_value+''' y='''+y_value+''' z='''+z_value+'''/> 
                    </AgentStart>
                    <AgentHandlers>
                      <ChatCommands/>
                      <MissionQuitCommands/>
                      <AbsoluteMovementCommands/>
                      <ObservationFromSystem/>
                      <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
    return missionXML

def delete_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory,file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)


def run_mission(biome):
    my_mission = MalmoPython.MissionSpec(create_mission(biome), True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:",e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission running ", end=' ')


    delete_directory(INPUT_FOLDER)
    time.sleep(4)
    for i in range(8):
        world_state = agent_host.getWorldState()
        agent_host.sendCommand("setPitch 0")
        agent_host.sendCommand("turn 0.5")
        time.sleep(0.5)
        agent_host.sendCommand("turn 0")
        takess.simg("Test//test_" + str(i))
        time.sleep(0.5)


    biome_prediction = predict.predict(MODEL_NAME, INPUT_FOLDER)
    print(biome_prediction)
    agent_host.sendCommand("chat " + "Biome guess: " + str(biome_prediction))
    time.sleep(1)
    agent_host.sendCommand("quit")
    while world_state.is_mission_running:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission ended")

possible_biomes = ["IcePlains", "IceMountains", "ColdTaiga", "ColdTaigaHills"]
run_mission(possible_biomes[random.randint(0,3)])
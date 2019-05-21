from builtins import range
import MalmoPython
import os
import sys
import time
import json
from collections import Counter
import takess
import predict

MINECRAFT_WORLDS = "C:\\Malmo2\\Minecraft\\run\\saves\\"

MODEL_NAME = 'conv_network.h5'  # this should stay the same
INPUT_FOLDER = "C:\\Malmo2\\CS175_Homework\\Data_Miners\\src\\Test"  # change this to your own location


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)


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
                    </AgentStart>
                    <AgentHandlers>
                      <MissionQuitCommands/>
                      <AbsoluteMovementCommands/>
                      <ObservationFromGrid>
                        <Grid name="observation">
                            <min x="-25" y="-25" z="-25"/>
                            <max x="24" y="24" z="24"/>
                        </Grid>
                      </ObservationFromGrid>
                      <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                  </AgentSection>
                </Mission>'''
    return missionXML

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

    time.sleep(4)
    for i in range(8):
        agent_host.sendCommand("setPitch 0")
        agent_host.sendCommand("turn 0.5")
        time.sleep(0.5)
        agent_host.sendCommand("turn 0")
        takess.simg("Test//test_" + str(i))
        time.sleep(0.5)


    print("Classifying screenshots...")
    biome_prediction = predict.predict(MODEL_NAME, INPUT_FOLDER)
    agent_host.sendCommand("quit")
    while world_state.is_mission_running:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission ended")

run_mission("IceMountains")
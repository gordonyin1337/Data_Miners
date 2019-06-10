from builtins import range
import MalmoPython
import os
import sys
import time
import json
from collections import Counter
import takess
import random

MINECRAFT_WORLDS = "C:\\Malmo2\\Minecraft\\run\\saves\\"
RECORDINGS = "C:\\Malmo2\\CS175_Homework\\Data_Miners\\Recordings"

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)

def create_mission(biome):
    x_value = '''"''' + str(random.randint(1, 50000)) + '''"'''
    y_value = '''"90"'''
    z_value = '''"''' + str(random.randint(1, 50000)) + '''"'''

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


def get_biome_data(biome):
    # Attempt to start a mission:
    my_mission = MalmoPython.MissionSpec(create_mission(biome), True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission(my_mission, my_mission_record)
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

    counter = 0

    if not os.path.exists("Screenshots//" + biome):
        os.mkdir("Screenshots//" + biome)
    for x in range(10):
        for z in range(10):
            world_state = agent_host.peekWorldState()
            teleport_x = random.randint(1,80000)
            teleport_z = random.randint(1,80000)
            tp_command = "tp " + str(teleport_x)+ " 90 " + str(teleport_z)
            print("Sending command: " + tp_command)
            agent_host.sendCommand(tp_command)
            time.sleep(4)
            agent_host.sendCommand("setPitch 0")
            takess.simg("Screenshots//" + biome + "//" + biome + "_" + str(counter))
            counter += 1
            for i in range(7):
                agent_host.sendCommand("turn 0.5")
                time.sleep(0.5)
                agent_host.sendCommand("turn 0")
                takess.simg("Screenshots//" + biome + "//" + biome + "_" + str(counter))
                counter += 1
                time.sleep(0.5)

    # Loop until mission ends:
    agent_host.sendCommand("quit")
    while world_state.is_mission_running:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission ended")
    # Mission has ended.

missions_biomes = ["MegaTaiga", "ForestHills", "TaigaHills", "JungleHills", "BirchForestHills", "MegaTaigaHills"]
for b in missions_biomes:
    get_biome_data(b)
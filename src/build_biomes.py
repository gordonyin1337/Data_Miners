from builtins import range
import MalmoPython
import os
import sys
import time
import json
from collections import Counter

MINECRAFT_WORLDS = "C:\\Malmo2\\Minecraft\\run\\saves\\"
RECORDINGS = "C:\\Malmo2\\CS175_Homework\\Data_Miners\\Recordings"

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
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
                  <FileWorldGenerator src="C:\\Malmo2\\Minecraft\\run\\saves\\Desert"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Creative">
                <Name>MalmoTutorialBot</Name>
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

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
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

counting_dict = None
for x in range(10):
    for z in range(10):
        world_state = agent_host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            obs = json.loads(world_state.observations[-1].text)
            obs_list = obs["observation"]
            obs_list = [value for value in obs_list if value != "air"]
            list(filter(lambda x: x == "air", obs_list))
            counting = dict(Counter(obs_list))
            print(counting)
        teleport_x = x * 1000 + 0.5
        teleport_z = z * 1000 + 0.5
        tp_command = "tp " + str(teleport_x)+ " 90 " + str(teleport_z)
        time.sleep(1)
        print("Sending command: " + tp_command)
        agent_host.sendCommand(tp_command)

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


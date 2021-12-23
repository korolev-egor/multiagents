from time import sleep
from asyncio import sleep as async_sleep
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from random import randint, random
from spade.agent import Agent
from spade import quit_spade


class MyAgent(Agent):
    class MyBehaviour(CyclicBehaviour):
        def __init__(self, name, neighbours, values):
            super().__init__()
            self.name = name
            self.neighbours = neighbours
            self.values = values


        async def run(self):
            if str(self.name) == agent_jid[0]:
                global CYCLES
                CYCLES += 1
                print(f'Cycle = {CYCLES}')
            for neighbor in self.neighbours:
                msg = Message(to=neighbor)
                msg.body = str(self.values)
                await self.send(msg)
                print(f'{self.name} sent message to {neighbor}')          
            msg = await self.receive()
            if msg is not None:
                self.values.update(eval(msg.body))
            if len(self.values) == len(adj_list):
                print(f'\nValues: {values}')
                print(f'Computed mean: {sum(self.values.values()) / len(adj_list)}')
                print(f'True mean: {sum(values)/n}')
                print(f'Number of cycles: {CYCLES}')
                print('Topology:\n')
                for k, v in adj_list.items():
                    print(k, v)
                global ANSWER_FOUND
                ANSWER_FOUND = True
                raise SystemExit
            print(self.values)


    async def setup(self):
        self.b = self.MyBehaviour(self.jid, self.neighbours, self.values)
        self.add_behaviour(self.b)
        await async_sleep(1)

    def __init__(self, name, password, neighbours, value):
        super().__init__(name, password)
        self.neighbours = neighbours
        self.values = {name:value}


def generate_list():
    def try_list():
        adj_list = dict()
        for jid in agent_jid:
            temp = []
            for i in range(n):
                if round(random() + CHANCE - 0.5) == 1 and agent_jid[i] != jid:
                    temp.append(agent_jid[i])
            if temp == []:
                raise Exception
            adj_list[jid] = temp
        return adj_list
    def is_connected():
        visited, stack = [], [list(adj_list.keys())[0]]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                stack.extend(set(adj_list[vertex]) - set(visited))
        if len(visited) == len(adj_list):
            return True
        return False
    while True:
        try:
            adj_list = try_list()
            if is_connected():
                return adj_list
            else:
                continue
        except Exception:
            continue
            

if __name__ == "__main__":
    ANSWER_FOUND = False
    CYCLES = 0
    CHANCE = 0.5
    agent_jid = ['arst1@01337.io', 'arst2@01337.io', 'arst3@01337.io', 'arst4@01337.io', 'arst5@01337.io']
    n = len(agent_jid)
    values = [randint(1, 100) for _ in range(n)]
    adj_list = generate_list()  # Список смежности
    agent1 = MyAgent(agent_jid[0], 'arst', adj_list[agent_jid[0]], values[0])
    agent2 = MyAgent(agent_jid[1], 'arst', adj_list[agent_jid[1]], values[1])
    agent3 = MyAgent(agent_jid[2], 'arst', adj_list[agent_jid[2]], values[2])
    agent4 = MyAgent(agent_jid[3], 'arst', adj_list[agent_jid[3]], values[3])
    agent5 = MyAgent(agent_jid[4], 'arst', adj_list[agent_jid[4]], values[4])
    agent1.start()
    agent2.start()
    agent3.start()
    agent4.start()
    agent5.start()
    while not ANSWER_FOUND:
        try:
            sleep(1)
        except SystemExit:
            break
        except KeyboardInterrupt:
            break
    quit_spade()

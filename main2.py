from time import sleep
from asyncio import sleep as async_sleep
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from random import randint, random
from spade.agent import Agent
from spade import quit_spade


class MyAgent(Agent):
    class MyBehaviour(CyclicBehaviour):
        def __init__(self, name, neighbors, number):
            super().__init__()
            self.name = name
            self.neighbors = neighbors
            self.number = number
            self.neighbors_visited = []
            self.messages = []
            self.delayed = []
    
    
        async def run(self):
            global free_agents, visited_all, CYCLES
            await async_sleep(1)
            for m in self.delayed.copy():
                if m[0] == CYCLES:
                    free_agents[m[1]] = False
                    await self.send(m[2])
                    self.delayed.remove(m)
            for neighbor in self.neighbors:
                if (neighbor not in self.neighbors_visited) and free_agents[neighbor] == 1:
                    msg=Message(to=neighbor, body=str(self.number + self.number*(random()-0.5)/100))  # помехи
                    self.neighbors_visited.append(neighbor)
                    if random() < 0.01:  # сообщение с задержкой
                        self.delayed.append((CYCLES+1, neighbor, msg))
                        await async_sleep(0.1)
                        continue
                    if random() < 0.01:  # сообщение теряется
                        await async_sleep(0.1)
                        continue
                    free_agents[neighbor] = False
                    await self.send(msg)
            rec = await self.receive()
            if rec:
                free_agents[self.name] = True
                self.messages.append(rec.body)
            if len(self.neighbors_visited) == len(self.neighbors):
                visited_all[self.name] = True
            if 0 not in visited_all.values():
                await async_sleep(1)
                self.number = self.number + ALPHA * sum(float(m) - self.number for m in self.messages)
                if str(self.name) == agent_jid[0]:
                    CYCLES += 1
                    print(f'Cycle number: {CYCLES}')
                    visited_all = {a_jid: 0 for a_jid in agent_jid}
                    free_agents = {a_jid: 1 for a_jid in agent_jid}
                self.messages = []
                self.neighbors_visited = []
                print(self.name, round(self.number, 2))
                await async_sleep(1)


    async def setup(self):
        self.b = self.MyBehaviour(str(self.jid), self.neighbors, self.number)
        self.add_behaviour(self.b)
        await async_sleep(2)

    
    def __init__(self, name, password, neighbors, number):
        super().__init__(name, password)
        self.neighbors = neighbors
        self.number = number


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
    CYCLES = 0
    CHANCE = 0.5
    agent_jid = ['arst1@01337.io', 'arst2@01337.io', 'arst3@01337.io', 'arst4@01337.io', 'arst5@01337.io']
    free_agents = {a_jid: 1 for a_jid in agent_jid}
    visited_all = {a_jid: 0 for a_jid in agent_jid}
    n = len(agent_jid)
    ALPHA = 1/n
    values = [randint(1, 100) for _ in range(n)]
    print(sum(values)/n)
    print(values)
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
    while True:
        try:
            sleep(1)
        except SystemExit:
            break
        except KeyboardInterrupt:
            break
    print(values)
    print(sum(values)/n)
    print('Topology:')
    for k, v in adj_list.items():
        print(k, v)
    quit_spade()

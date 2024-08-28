import simpy
import numpy as np
import random

NUM_EMPLOYEES: int = 2
AVG_SUPPORT_TIME: int = 5
CUSTOMER_INTERVAL: int = 2
SIM_TIME: int = 120

customers_handled: int = 0

class CallCenter:
    def __init__(self, env: simpy.Environment, num_employees: int, suppor_time: int) -> None:
        self.env: simpy.Environment = env
        self.staff: int = simpy.Resource(env, num_employees)
        self.support_time: int = suppor_time
    
    def support(self, customer: str):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Suppor finished for {customer} as {self.env.now:.2f}")

def customer(env: simpy.Environment, name: str, call_center: CallCenter):
    global customers_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}")
    with call_center.staff.request() as request:
        yield request
        print(f"Customer {name} enters call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        print(f"Customer {name} enters call at {env.now:.2f}")
        customers_handled += 1

def setup(env: simpy.Environment, num_employees: int, support_time: int, customer_interval: int):
    call_center: CallCenter = CallCenter(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))
    
    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center))

print("Starting call center simulation")
env: simpy.Environment = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
env.run(SIM_TIME)

print(f"Customers Handled: {customers_handled}")
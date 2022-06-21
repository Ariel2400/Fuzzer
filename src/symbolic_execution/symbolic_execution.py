import time
import angr
import claripy
import threading
import random

BITS_IN_BYTE = 8

class SymbolicExecutionProperties:
    
    def __init__(self, len_symbolic_bytes, load_dynamic_libaries):
        self.load_dynamic_libaries = load_dynamic_libaries
        self.len_symbolic_bytes = len_symbolic_bytes

class State:

    def __init__(self, angrState, satisfiable):
        self.angrState = angrState
        self.satisfiable = satisfiable        

class SymbolicExecution:

    def __init__(self, symbolic_execution_properties: SymbolicExecutionProperties, target, command_line_args = []):
        self.target = target
        self.command_line_args = command_line_args
        self.proj = angr.Project(target, auto_load_libs=symbolic_execution_properties.load_dynamic_libaries)
        self.states = {}        # array maps entry address of basic block to angr state
        self.symbolic_execution_properties = symbolic_execution_properties
        self.statesLock = threading.Lock()
        self.stop = False
    
    #returning target input to reach a random basic block
    def getTargetInput(self):
        input_sym_chars = [claripy.BVS('input_%d', BITS_IN_BYTE) for i in range(self.symbolic_execution_properties.len_symbolic_bytes)]
        input_sym = claripy.Concat(*input_sym_chars)
        entry_state = self.proj.factory.entry_state(args=[self.target] + self.command_line_args, add_options=angr.options.unicorn , stdin=input_sym) 
        addStatesThread = threading.Thread(target=self.addStates, args=(entry_state,))
        addStatesThread.start()
        self.states[entry_state.addr] = State(entry_state, entry_state.satisfiable())
        
        #eval satisfied input for random basic block
        while True and not self.stop:
            state = self.getRandomSatisfiableState()
            satisfied_data = state.angrState.solver.eval(input_sym, cast_to=bytes)
            yield satisfied_data
            self.addConstraintToStates(satisfied_data, input_sym, state)


        addStatesThread.join()

    def addStates(self, entry_state):
        simgr = self.proj.factory.simgr(entry_state)
        print("start")
        while len(simgr.active) > 0 and not self.stop:
            #check if add state to states dict
            for angrActiveState in simgr.active:
                self.statesLock.acquire()
                if angrActiveState.addr not in self.states:
                    self.states[angrActiveState.addr] = State(angrActiveState, angrActiveState.satisfiable())
                self.statesLock.release()

            #step every state in one basic block
            simgr.step()
        print("done")

    def addConstraintToStates(self, satisfied_data, input_sym, state):
        self.statesLock.acquire()
        '''for stateAddr in self.states:
            if(self.states[stateAddr].satisfiable):
                self.states[stateAddr].angrState.solver.add(input_sym != satisfied_data) #Adding a constraint that will not be returned to the same input
                self.states[stateAddr].satisfiable = self.states[stateAddr].angrState.satisfiable()'''
        state.angrState.solver.add(input_sym != satisfied_data)
        state.satisfiable = state.angrState.satisfiable()
        self.statesLock.release()



    def getRandomSatisfiableState(self):
        isSatisfiableState = False
        while not isSatisfiableState:
            self.statesLock.acquire()
            random_basic_block_addr = random.choice(list(self.states.keys()))
            if self.states[random_basic_block_addr].satisfiable:
                satisfableState = self.states[random_basic_block_addr]
                self.statesLock.release()
                isSatisfiableState = True
        return satisfableState

    def stopProcessing(self):
        self.stop = True




if __name__ == '__main__':
    symbolicExecutionProperties = SymbolicExecutionProperties(4, False)
    #symbolicExecution = SymbolicExecution(symbolicExecutionProperties, '/usr/bin/jq', ['.'])
    symbolicExecution = SymbolicExecution(symbolicExecutionProperties, '/home/tomer/code/a.out', ['flag1'])
    generator = symbolicExecution.getTargetInput()
    print(next(generator), '\n')
    time.sleep(5)
    print("timer done")
    for _ in range(100):
        print(next(generator), '\n')
    symbolicExecution.stopProcessing()
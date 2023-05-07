# Ready: can add new process
# Configuring: changing type
# Processing: processing a patch    
State = ["Ready", "Configuring", "Processing"]
Unit_By_Litter = [1,3] # Exchange rate

Phase_2_Reconfig = (
    (0, 3, 3, 4, 4, 4),
    (3, 0, 3, 4, 4, 4),
    (3, 3, 0, 4, 4, 4),
    (4, 4, 4, 0, 3, 3),
    (4, 4, 4, 3, 0, 3),
    (4, 4, 4, 3, 3, 0)
)


class MachinePhase1:
    def __init__(self, capacity: int, time : int) -> None:
        self.time = time
        self.count :int = 0
        self.capacity = self.capacity
        self.reconfig = 2
        self.config_time : int = 0
        self.config = -1
        self.state = State[0]

    def process(self) -> int:
        """ Run the machine for a Quantum time
        If configuring: set time down to 
        Else produce the batch
        Return value is in Litter
        """
        if self.state == State[1]:
            self.config_time -=1
            if self.config_time ==0:
                self.state =State[2]
                self.count = self.time
        elif self.state == State[2]:
            self.count -=1
            if self.count == 0:
                self.counter = self.time
                return self.capacity 
        return 0

    def assign(self, job: int) -> None:
        """
            Assign job to the machine
            Args: 
                job (int): job id
            Return: None
        """
        if self.config == -1:
            self.config = job
            self.count = self.time
            self.state = State[2]
        elif self.config != job:
            self.config = job
            self.config_time = self.reconfig
            self.state = State[1]
        else:
            pass


class MachinePhase2:
    def __init__(self, capacity: int) -> None:
        self.count :int = 0
        self.capacity = self.capacity
        self.reconfig = 0
        self.config_time : int = 0
        self.config = -1
        self.state = State[0]

    def process(self, input: int) -> int:
        """Process ammount of goods
            Args: 
                input: quantity to be produce (in L)
            Return:
                ammount processed upto its capacity or input (in Units)
        """
        if self.state== State[1]:
            self.config_time -=1
            if self.config_time == 0:
                self.state = State[2]
        elif self.state == State[2]:
            return min(input, self.capacity) * Unit_By_Litter[self.config//3] # Majik number aka problem requirement
        return 0
    
    def assign(self, job: int) -> None:
        """
            Assign job to the machine
            Args: 
                job (int): job id
            Return: None
        """
        if self.config == -1:
            self.config = job
            self.state = State[2]
        elif self.config != job:
            self.config_time = Phase_2_Reconfig[self.config][job]
            self.config = job
            self.state = State[1]
        else:
            pass


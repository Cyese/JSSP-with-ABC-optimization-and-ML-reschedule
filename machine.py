bottle_per_liter = [1, 3]  # 1 unit -> big, 3 unit -> small


class Machine:
    # Ready: can add new process
    # Configuring: changing type
    # Processing: processing a patch
    State = ["Ready", "Configuring", "Processing"]

    Mix_change = [[2 for _ in range(6)] for _ in range(6)]  # Constant

    # Change-over matrix set Change over matrix[i][j]: change time from i -> j
    Change_over = (
        (0, 3, 3, 4, 4, 4),
        (3, 0, 3, 4, 4, 4),
        (3, 3, 0, 4, 4, 4),
        (4, 4, 4, 0, 3, 3),
        (4, 4, 4, 3, 0, 3),
        (4, 4, 4, 3, 3, 0)
    )

    Job_Description = {
        "Mixing": Mix_change,
        "Bottling": Change_over
    }

    def __init__(self, capacity: int, time: int):
        if time > 1:
            self.counter = 0
        #(variable) time: time per batch
        self.time = time
        # @variable : quantity per batch
        self.capacity = capacity  
        # @variable : pending configuration time
        self.config_time :int = 0  
        # @variavble : Current configuration
        self.type_config = -1 
        # @variable : Machine current state
        self.state = Machine.State[0]
        # @variable : change over time between 2 different config
        self.change_over : list

    # Activity to be done in a quantum time
    # def process(self, quantity: int = 0)


class MixingMachine(Machine):
    def __init__(self, capacity: int, time: int):
        """Create a new machine for the job

        Args:
            capacity (int) : batch size
            time (int): time per batch
        Returns:
            MixingMachine: machine created
        """
        super().__init__(capacity, time)
        self.change_over = Machine.Job_Description["Mixing"]

    def process(self):
        if self.state == Machine.State[1]:
            self.config_time -= 1
            if self.config_time == 0:
                self.state = Machine.State[2]
                self.counter = 2
        elif self.state == Machine.State[2]:
            self.counter -= 1
            if self.counter == 0:
                self.state = Machine.State[0]
                self.counter = self.time
                return self.capacity
        return 0

    def assign(self, _type: int):
        if self.type_config != _type:
            self.config_time = self.change_over[self.type_config][_type]
            self.state = Machine.State[1]
            return 1
        return 0


class BottlingMachine(Machine):
    def __init__(self, capacity : int, time:int = 0):
        """Create a new machine for the job

        Args:
            capacity (int) : batch size
        Returns:
            BottlingMachine: machine created
        """
        super().__init__(capacity, time)
        self.change_over = Machine.Job_Description["Bottling"]

    def process(self, quantity: int):
        if self.state == Machine.State[1]:
            if self.state == Machine.State[1]:
                self.config_time -= 1
                if self.config_time == 0:
                    self.state = Machine.State[2]
        elif self.state == Machine.State[2]:
            return min(quantity, self.capacity)
        return 0

    def assign(self, _type: int):
        if self.type_config != _type:
            self.config_time = self.change_over[self.type_config][_type]
            return 1
        return 0

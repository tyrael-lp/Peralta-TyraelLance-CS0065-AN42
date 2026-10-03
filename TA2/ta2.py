import agentpy as ap
import random


# Ask the user for a valid room condition
def ask_room_condition(room_name):
    while True:
        condition = input(
            f"Is Room {room_name} Dirty or Clean? "
        ).strip().lower()

        if condition in ["dirty", "clean"]:
            return condition

        print("Please enter only 'Dirty' or 'Clean'.")


# Get user input
room_a = ask_room_condition("A")
room_b = ask_room_condition("B")
room_c = ask_room_condition("C")
num_steps = int(input("\nHow many steps should the agent run? "))


# Agent Definition
class RoomCleaner(ap.Agent):

    def setup(self):
        self.current_room = "A"
        self.actions = 0

    def step(self):
        self.actions += 1
        room_status = self.model.rooms[self.current_room]

        if room_status == "dirty":
            print(
                f"\n\nStep {self.actions}: "
                f"Room {self.current_room} is dirty. Cleaning it."
            )

            self.model.rooms[self.current_room] = "clean"

        else:
            old_room = self.current_room

            # Select another room randomly
            possible_rooms = [
                room for room in self.model.rooms
                if room != self.current_room
            ]

            self.current_room = random.choice(possible_rooms)

            print(
                f"\n\nStep {self.actions}: "
                f"Room {old_room} is clean. "
                f"Moving to Room {self.current_room}."
            )
        


# Model Definition
class Rooms(ap.Model):

    def setup(self):
        self.rooms = {
            "A": room_a,
            "B": room_b,
            "C": room_c
        }

        # Create one RoomCleaner agent
        self.cleaner = RoomCleaner(self)

        print("\nInitial Room Conditions:")
        print(f"Room A: {self.rooms['A']}")
        print(f"Room B: {self.rooms['B']}")
        print(f"Room C: {self.rooms['C']}")
        print(f"Agent starts in Room A.\n")

    def step(self):
        self.cleaner.step()
        print(f"Agent current position:")
        print( "[   A   |   B   |   C   ]")
        print(f"[ {self.rooms['A']} | {self.rooms['B']} | {self.rooms['C']} ]")
        if self.cleaner.current_room == 'A':
            print( "[   0   |   -   |   -   ]")

        elif self.cleaner.current_room == 'B':
            print( "[   -   |   0   |   -   ]")

        elif self.cleaner.current_room == 'C':
            print( "[   -   |   -   |   0   ]")


    def end(self):
        print("\n\nSimulation Finished.")
        print("Final Room Conditions.")
        print(f"[ A - {self.rooms['A']}| B - {self.rooms['B']} | C - {self.rooms['C']} ]")
        print(f"Agent's final location: Room {self.cleaner.current_room}")


# Simulation parameters
parameters = {
    "steps": num_steps
}


# Create and run the model
model = Rooms(parameters)
model.run()
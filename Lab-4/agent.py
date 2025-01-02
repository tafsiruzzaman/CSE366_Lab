import numpy as np

class Agent:
    def __init__(self, id, availability, preferences):
        """
        Initialize the agent with an id, availability, preferences, and schedule.
        """
        self.id = id  # Unique identifier for each student
        self.availability = availability  # Availability matrix (0 = unavailable, 1 = available)
        self.preferences = preferences  # Preference for each slot (1-5 scale)
        self.schedule = []  # The schedule this agent (student) will follow

    def assign_classes(self, class_assignments):
        """
        Assign classes to this agent (student) based on availability and preferences.
        """
        self.schedule = []  # Reset schedule before assigning
        for class_id, (student, slot) in enumerate(class_assignments):
            if student == self.id and self.availability[slot] == 1:
                # Assign the class to the student if the student is available
                self.schedule.append((class_id, slot))

    def reset_schedule(self):
        """
        Clear the current schedule for the agent (student) to allow re-scheduling.
        """
        self.schedule = []  # Clear all classes from the student's schedule

    def get_fitness(self, environment):
        """
        Calculate the fitness score of the current schedule.
        Fitness is calculated based on:
        1. Conflict Minimization: Penalize if a class is scheduled in an unavailable time slot.
        2. Preference Alignment: Reward schedules aligning with the student's preferred time slots.
        """
        conflict_penalty = 0
        preference_penalty = 0

        for class_id, slot in self.schedule:
            # Penalize for conflicts
            if self.availability[slot] == 0:
                conflict_penalty += 1

            # Penalize based on preference alignment
            if self.preferences[slot] > 0:
                preference_penalty += 1 / self.preferences[slot]
            else:
                preference_penalty += 1  # Maximum penalty for missing preference data

        # Total fitness score is the sum of conflict and preference penalties
        return conflict_penalty + preference_penalty
import copy

# A class to represent a host in the network
class Host:
    def __init__(self, name, value, connected_to):
        self.name = name
        self.value = value
        self.connected_to = list(connected_to)  
        self.is_compromised = False  # True if the attacker has taken over this host
        self.is_patched = False      # True if the host has been patched by the defender
        self.is_isolated = False     # True if all network connections have been severed

    def __repr__(self): # check/change later
        return f"{self.name}(val={self.value}, comp={self.is_compromised}, patch={self.is_patched}, iso={self.is_isolated})"

    def clone(self):
        h = copy.copy(self) # Create a shallow copy of the Host instance
        h.connected_to = self.connected_to[:]  # Make a shallow copy of the list to avoid shared references
        return h

# A class to represent the state of the game and control the game logic
class GameState:
    def __init__(self):
        # Define the 10 hosts in the network with their asset values and connections
        self.hosts = {
            "H0": Host("H0", 0,   ["H1", "H2"]),
            "H1": Host("H1", 10,  ["H0", "H3", "H4"]),
            "H2": Host("H2", 15,  ["H0", "H4"]),
            "H3": Host("H3", 30,  ["H1", "H5", "H6"]),
            "H4": Host("H4", 10,  ["H1", "H2", "H6"]),
            "H5": Host("H5", 100, ["H3", "H7"]),
            "H6": Host("H6", 60,  ["H3", "H4", "H7"]),
            "H7": Host("H7", 25,  ["H5", "H6", "H8"]),
            "H8": Host("H8", 20,  ["H7", "H9"]),
            "H9": Host("H9", 40,  ["H8"])
        }

        # Initial state: H0 is compromised. Every other host is clean, unpatched and connected.
        self.hosts["H0"].is_compromised = True

        self.current_player = "Attacker"   # The attacker moves first, then players alternate
        self.ply_count = 0                 # Number of plies taken so far (max 10 plies)
        self.defender_budget = 10          # Defender starts with a defence budget of 10
        self.attacker_has_zero_day = True  # Attacker holds one zero-day usable once per game
        self.exfiltrated = False           # True once the attacker exfiltrates from H5

    def __repr__(self):
        return f"GameState(ply={self.ply_count}, player={self.current_player}, budget={self.defender_budget}, zero_day={self.attacker_has_zero_day}, exfiltrated={self.exfiltrated})"

    def clone(self):
        s = copy.copy(self) # Create a shallow copy of the GameState instance
        s.hosts = {k: v.clone() for k, v in self.hosts.items()} # Create a new dictionary with cloned Host instances to avoid shared references
        return s

    def is_terminal(self): # Return True if the game has ended (either exfiltration occurred or 10 plies have been played)
        return self.exfiltrated or self.ply_count >= 10

    def utility(self):
        # Defender's utility U:
        # U = -(sum of asset values of compromised hosts at the end) - (total defence cost spent) - 100 * I
        # where I = 1 if exfiltration occurred, and I = 0 otherwise.
        # The attacker's utility is -U (Defender maximizes U, Attacker minimizes U).
        
        compromised_value = sum(h.value for h in self.hosts.values() if h.is_compromised)
        cost_spent = 10 - self.defender_budget
        exfil_penalty = 100 if self.exfiltrated else 0
        return -compromised_value - cost_spent - exfil_penalty
        
    def get_legal_actions(self):
        # Return a list of legal actions for the current player in the current state
        if self.is_terminal():
            return []

        legal_actions = []

        if self.current_player == "Attacker":
            for host in self.hosts.values():
                # Spread only from compromised, non-isolated hosts
                if not host.is_compromised or host.is_isolated:
                    continue

                for neighbour_name in host.connected_to:
                    neighbour = self.hosts[neighbour_name]

                    # Exploit(h): h is clean, unpatched, not isolated, and adjacent
                    if (not neighbour.is_compromised and not neighbour.is_patched and not neighbour.is_isolated and ("Exploit", neighbour_name) not in legal_actions):
                        legal_actions.append(("Exploit", neighbour_name))

                    # ZeroDay(h): Same as Exploit, except h is patched. Usable once per game.
                    if (self.attacker_has_zero_day and not neighbour.is_compromised and neighbour.is_patched and not neighbour.is_isolated and ("ZeroDay", neighbour_name) not in legal_actions):
                        legal_actions.append(("ZeroDay", neighbour_name))

            # Exfiltrate: H5 is compromised and not isolated
            h5 = self.hosts["H5"]
            if h5.is_compromised and not h5.is_isolated:
                legal_actions.append(("Exfiltrate", None))

            # Pass is always legal
            legal_actions.append(("Pass", None))

        elif self.current_player == "Defender":
            for host in self.hosts.values():
                # H0 can never be patched, isolated, or restored
                if host.name == "H0":
                    continue

                # Patch(h): cost 2 — h is clean and unpatched
                if (not host.is_compromised and not host.is_patched and self.defender_budget >= 2):
                    legal_actions.append(("Patch", host.name))

                # Isolate(h): cost 8 — h is not already isolated
                if (not host.is_isolated and self.defender_budget >= 8):
                    legal_actions.append(("Isolate", host.name))

                # Restore(h): cost 5 — h is compromised
                if (host.is_compromised and self.defender_budget >= 5):
                    legal_actions.append(("Restore", host.name))

            # Pass is always legal (cost 0)
            legal_actions.append(("Pass", None))

        return legal_actions

    def apply_action(self, action):
        # Apply the given action to the current game state and return the resulting new state. The action is assumed to be legal.
        action_type, target_host_name = action
        target_host = self.hosts[target_host_name] if target_host_name else None

        if self.current_player == "Attacker":
            if action_type == "Exploit":
                target_host.is_compromised = True

            elif action_type == "ZeroDay":
                target_host.is_compromised = True
                self.attacker_has_zero_day = False

            elif action_type == "Exfiltrate":
                self.exfiltrated = True

            # "Pass" — nothing changes (cost 0)

            self.current_player = "Defender"
            

        elif self.current_player == "Defender":
            if action_type == "Patch":
                target_host.is_patched = True
                self.defender_budget -= 2

            elif action_type == "Isolate":
                for neighbour_name in list(target_host.connected_to):
                    neighbour = self.hosts[neighbour_name]
                    if target_host_name in neighbour.connected_to:
                        neighbour.connected_to.remove(target_host_name)
                target_host.connected_to.clear()
                target_host.is_isolated = True
                self.defender_budget -= 8

            elif action_type == "Restore":
                target_host.is_compromised = False
                target_host.is_patched = True
                self.defender_budget -= 5

            # "Pass" — nothing changes (cost 0)

            self.current_player = "Attacker"
        
        self.ply_count += 1
        return self
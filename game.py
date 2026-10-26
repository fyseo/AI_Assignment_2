import copy

# Represents one host in the network.
class Host:
    def __init__(self, name, value, connected_to):
        self.name = name
        self.value = value
        self.connected_to = list(connected_to)
        self.is_compromised = False  # Attacker controls the host.
        self.is_patched = False      # Defender has patched the host.
        self.is_isolated = False     # Host has no network connections.

    def __repr__(self):
        return f"{self.name}(value={self.value}, compromised={self.is_compromised}, patch={self.is_patched}, isolated={self.is_isolated})"

    def clone(self):
        h = copy.copy(self)  # Copy the host.
        h.connected_to = self.connected_to[:]  # Copy the connection list.
        return h

# Stores the network and game rules.
class GameState:
    def __init__(self):
        # Create hosts with their values and connections.
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

        # H0 is the initial attacker entry point.
        self.hosts["H0"].is_compromised = True

        self.current_player = "Attacker"   # Attacker moves first.
        self.ply_count = 0                 # Number of moves taken.
        self.defender_budget = 10          # Defender's starting budget.
        self.attacker_has_zero_day = True  # One use per game.
        self.exfiltrated = False           # True after H5 exfiltration.

    def __repr__(self):
        return f"GameState(plies used={self.ply_count}, current player={self.current_player}, defender budget={self.defender_budget}, zero_day available={self.attacker_has_zero_day}, target exfiltrated={self.exfiltrated})"

    def clone(self):
        s = copy.copy(self)  # Copy the game state.
        s.hosts = {k: v.clone() for k, v in self.hosts.items()}  # Copy each host.
        return s

    def is_terminal(self):
        # Stop after exfiltration or 10 moves.
        return self.exfiltrated or self.ply_count >= 10

    def utility(self):
        # Defender utility:
        # U = -compromised asset value - defence cost - exfiltration penalty.
        # The Defender maximizes U; the Attacker minimizes U.
        compromised_value = sum(h.value for h in self.hosts.values() if h.is_compromised)
        cost_spent = 10 - self.defender_budget
        exfil_penalty = 100 if self.exfiltrated else 0
        return -compromised_value - cost_spent - exfil_penalty
        
    def get_legal_actions(self):
        # Return actions available to the current player.
        if self.is_terminal():
            return []

        legal_actions = []

        if self.current_player == "Attacker":
            for host in self.hosts.values():
                # Only compromised hosts can spread.
                if not host.is_compromised or host.is_isolated:
                    continue

                for neighbour_name in host.connected_to:
                    neighbour = self.hosts[neighbour_name]

                    # Exploit clean, unpatched neighbors.
                    if (not neighbour.is_compromised and not neighbour.is_patched and not neighbour.is_isolated and ("Exploit", neighbour_name) not in legal_actions):
                        legal_actions.append(("Exploit", neighbour_name))

                    # Use the zero-day against patched neighbors.
                    if (self.attacker_has_zero_day and not neighbour.is_compromised and neighbour.is_patched and not neighbour.is_isolated and ("ZeroDay", neighbour_name) not in legal_actions):
                        legal_actions.append(("ZeroDay", neighbour_name))

            # Exfiltrate only from an active H5.
            h5 = self.hosts["H5"]
            if h5.is_compromised and not h5.is_isolated:
                legal_actions.append(("Exfiltrate", None))

            # Passing is always allowed.
            legal_actions.append(("Pass", None))

        elif self.current_player == "Defender":
            for host in self.hosts.values():
                # H0 cannot be defended.
                if host.name == "H0":
                    continue

                # Patch a clean host for 2 budget.
                if (not host.is_compromised and not host.is_patched and self.defender_budget >= 2):
                    legal_actions.append(("Patch", host.name))

                # Isolate an active host for 8 budget.
                if (not host.is_isolated and self.defender_budget >= 8):
                    legal_actions.append(("Isolate", host.name))

                # Restore a compromised host for 5 budget.
                if (host.is_compromised and self.defender_budget >= 5):
                    legal_actions.append(("Restore", host.name))

            # Passing costs nothing.
            legal_actions.append(("Pass", None))

        return legal_actions

    def apply_action(self, action):
        # Apply a legal action, switch turns, and return this state.
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

            # Pass does not change the state.

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

            # Pass does not change the state.

            self.current_player = "Attacker"
        
        self.ply_count += 1
        return self
import math

# Search statistics used when comparing the algorithms in the report.
expanded_nodes = 0
pruned_nodes = 0


def evaluate(state):
    # Estimate non-terminal states from the Defender's perspective.
    # The base utility captures the actual score so far; the bonuses and
    # penalties estimate threats that may occur beyond the search depth.
    score = state.utility()
    h5 = state.hosts["H5"]

    # Isolating H5 prevents access to the most valuable asset.
    if h5.is_isolated:
        score += 40
    # A compromised, non-isolated H5 is close to an exfiltration opportunity.
    elif h5.is_compromised:
        score -= 80

    # H3 and H7 are adjacent routes to H5, so their compromise is dangerous.
    if state.hosts["H3"].is_compromised or state.hosts["H7"].is_compromised:
        score -= 25

    # Patching H5 reduces the chance that it can be exploited later.
    if h5.is_patched:
        score += 15

    return score


def order_actions(actions):
    # Search decisive actions first so Alpha-Beta can find useful bounds early.
    # The original order of actions within each group is preserved.
    ordered_actions = []

    # Exfiltration is the most urgent Attacker action.
    for action in actions:
        if action[0] == "Exfiltrate":
            ordered_actions.append(action)

    # Search all active actions before allowing either player to pass.
    for action in actions:
        if action[0] not in ("Exfiltrate", "Pass"):
            ordered_actions.append(action)

    # Pass is searched last because it does not change the state.
    for action in actions:
        if action[0] == "Pass":
            ordered_actions.append(action)

    return ordered_actions


def minimax(state, depth=None):
    # Use minimax(state) for full search until the game ends.
    # Use minimax(state, depth=3) for depth-limited search.
    global expanded_nodes

    # Terminal states have an exact utility and require no further action.
    if state.is_terminal():
        return state.utility(), None

    # At the depth limit, estimate the non-terminal state heuristically.
    if depth == 0:
        return evaluate(state), None

    expanded_nodes += 1
    # Keep None for full search; otherwise reduce the remaining search depth.
    next_depth = None if depth is None else depth - 1
    actions = order_actions(state.get_legal_actions())

    # The Defender maximizes defender utility.
    if state.current_player == "Defender":
        best_value = -math.inf
        best_action = None
        for action in actions:
            # Clone before applying an action so each branch is independent.
            value, _ = minimax(state.clone().apply_action(action), next_depth)
            if value > best_value:
                best_value = value
                best_action = action
        return best_value, best_action

    # The Attacker minimizes defender utility.
    best_value = math.inf
    best_action = None
    for action in actions:
        value, _ = minimax(state.clone().apply_action(action), next_depth)
        if value < best_value:
            best_value = value
            best_action = action
    return best_value, best_action


def alpha_beta(state, depth=3, alpha=-math.inf, beta=math.inf):
    # Use alpha_beta(state) for the default depth-3 search.
    # Pass depth=None for full search until the game ends.
    # Pass another depth, such as depth=5, for a different depth limit.

    global expanded_nodes, pruned_nodes

    # These are the same base cases as Minimax, but Alpha-Beta also
    # receives the bounds accumulated by its ancestors.
    if state.is_terminal():
        return state.utility(), None
    if depth == 0:
        return evaluate(state), None

    expanded_nodes += 1
    # Keep None for full search; otherwise reduce the remaining search depth.
    next_depth = None if depth is None else depth - 1
    actions = order_actions(state.get_legal_actions())

    # Defender node: keep the highest value and improve the alpha bound.
    if state.current_player == "Defender":
        best_value = -math.inf
        best_action = None
        for index, action in enumerate(actions):
            value, _ = alpha_beta(state.clone().apply_action(action), next_depth, alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)

            # No Attacker ancestor would choose a branch this good for the
            # Defender once alpha reaches or exceeds beta.
            if alpha >= beta:
                pruned_nodes += len(actions) - index - 1
                break
        return best_value, best_action

    # Attacker node: keep the lowest value and improve the beta bound.
    best_value = math.inf
    best_action = None
    for index, action in enumerate(actions):
        value, _ = alpha_beta(state.clone().apply_action(action), next_depth, alpha, beta)
        if value < best_value:
            best_value = value
            best_action = action
        beta = min(beta, best_value)

        # No Defender ancestor would choose a branch this bad for the
        # Defender once beta is at or below alpha.
        if alpha >= beta:
            pruned_nodes += len(actions) - index - 1
            break
    return best_value, best_action

SECURITY_STATES = {"healthy", "compromised", "impacted"}
CONNECTIVITY_STATES = {"connected", "host_isolated", "communication_interrupted"}


def initial_states(hosts):
    return {h["hostname"]: "healthy" for h in hosts}


def initial_connectivity(hosts):
    return {h["hostname"]: "connected" for h in hosts}


def apply_event(states, event):
    if event.event_type in {"E01", "E02", "E03", "E04"}:
        states[event.target_host] = "compromised"
    elif event.event_type == "E05":
        states[event.target_host] = "impacted"
    return states


def apply_response(connectivity, response):
    if response.action == "host_isolate" and response.target_host:
        connectivity[response.target_host] = "host_isolated"
    elif response.action == "communication_interrupt" and response.target_host:
        connectivity[response.target_host] = "communication_interrupted"
    return connectivity


def action_viable(action, connectivity):
    return (
        connectivity.get(action.source_host, "connected") == "connected"
        and connectivity.get(action.target_host, "connected") == "connected"
    )

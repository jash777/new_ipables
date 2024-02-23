# rule.py

from iptc import Table, Chain, Rule, Match, Target
import logging
import iptc

logging.basicConfig(filename='Agent.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def add_iptables_rule(protocol, destination_port, action):
    try:
        rule = iptc.Rule()
        rule.protocol = protocol
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

        # Create the target based on the action
        target = rule.create_target(action.upper())

        # Create the match based on protocol
        match = None
        if protocol.lower() == 'tcp':
            match = rule.create_match("tcp")
        elif protocol.lower() == 'udp':
            match = rule.create_match("udp")
        # Add more conditions for other protocols if necessary

        # Set the destination port
        if match:
            match.dport = str(destination_port)
        
        # Insert the rule into the chain
        chain.insert_rule(rule)
        
        logging.info("Iptables rule added successfully.")
    except iptc.IPTCError as e:
        logging.error(f"IPTCError: {e}")
        # Handle IPTC specific errors
    except Exception as e:
        logging.error(f"Error adding iptables rule: {e}")
        raise  # Re-raise the exception for error handling in the caller

def block_port(port):
    # Create a new rule
    rule = iptc.Rule()
    rule.protocol = "tcp"
    rule.target = iptc.Target(rule, "DROP")
    match = rule.create_match("tcp")
    match.sport = str(port)
    rule.add_match(match)

    # Insert the rule at the beginning of the INPUT chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)
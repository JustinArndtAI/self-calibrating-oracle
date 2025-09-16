from src.simulator import Simulator
import time

# --- Configuration ---
GROUND_TRUTH_FRICTION = 0.9  # The "real" hidden value we want the oracle to find.
ORACLE_START_FRICTION = 0.2  # The oracle's incorrect starting guess.
SIMULATION_STEPS = 150       # How many steps to run the simulation for.
IMPULSE_TO_APPLY = (10000, 0) # The force applied to the boxes.

def run_phase_1():
    """
    Demonstrates the core problem: a model with incorrect parameters (the Oracle)
    will produce results that diverge from reality (the Ground Truth).
    """
    print("--- Phase 1: Demonstrating Simulation Divergence ---")
    
    # 1. Instantiate two separate simulation worlds.
    ground_truth_sim = Simulator(friction=GROUND_TRUTH_FRICTION)
    csm_oracle_sim = Simulator(friction=ORACLE_START_FRICTION)
    
    print(f"Ground Truth Friction: {GROUND_TRUTH_FRICTION}")
    print(f"Oracle's Initial Guess for Friction: {ORACLE_START_FRICTION}\n")

    # 2. Add an identical object to the same starting position in both worlds.
    ground_truth_sim.add_dynamic_box()
    csm_oracle_sim.add_dynamic_box()

    # 3. Apply the *exact same* force to both objects.
    ground_truth_sim.apply_impulse(IMPULSE_TO_APPLY)
    csm_oracle_sim.apply_impulse(IMPULSE_TO_APPLY)

    # 4. Run both simulations for the same amount of time.
    print(f"Running simulations for {SIMULATION_STEPS} steps...")
    for _ in range(SIMULATION_STEPS):
        ground_truth_sim.step()
        csm_oracle_sim.step()

    # 5. Get the final state (position) of the object in each world.
    ground_truth_pos = ground_truth_sim.get_object_state()
    oracle_pos = csm_oracle_sim.get_object_state()

    print("\n--- Simulation Complete ---")
    print(f"Final position in 'Ground Truth' world:  X = {ground_truth_pos[0]:.2f}")
    print(f"Final position in 'Oracle's' world:      X = {oracle_pos[0]:.2f}")
    
    error = abs(ground_truth_pos[0] - oracle_pos[0])
    print(f"\nResulting Error (Divergence): {error:.2f} units")
    print("--------------------------------------------------")


if __name__ == "__main__":
    run_phase_1()
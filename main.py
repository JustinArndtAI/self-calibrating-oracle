from src.simulator import Simulator
from src.engine import CalibrationEngine
import time
import matplotlib.pyplot as plt
import os

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
    
    ground_truth_sim = Simulator(friction=GROUND_TRUTH_FRICTION)
    csm_oracle_sim = Simulator(friction=ORACLE_START_FRICTION)
    
    print(f"Ground Truth Friction: {GROUND_TRUTH_FRICTION}")
    print(f"Oracle's Initial Guess for Friction: {ORACLE_START_FRICTION}\n")

    ground_truth_sim.add_dynamic_box()
    csm_oracle_sim.add_dynamic_box()

    ground_truth_sim.apply_impulse(IMPULSE_TO_APPLY)
    csm_oracle_sim.apply_impulse(IMPULSE_TO_APPLY)

    print(f"Running simulations for {SIMULATION_STEPS} steps...")
    for _ in range(SIMULATION_STEPS):
        ground_truth_sim.step()
        csm_oracle_sim.step()

    ground_truth_pos = ground_truth_sim.get_object_state()
    oracle_pos = csm_oracle_sim.get_object_state()

    print("\n--- Simulation Complete ---")
    print(f"Final position in 'Ground Truth' world:  X = {ground_truth_pos[0]:.2f}")
    print(f"Final position in 'Oracle's' world:      X = {oracle_pos[0]:.2f}")
    
    error = abs(ground_truth_pos[0] - oracle_pos[0])
    print(f"\nResulting Error (Divergence): {error:.2f} units")
    print("--------------------------------------------------\n")
    
    # We return the "real" outcome so Phase 2 knows what to aim for.
    return ground_truth_pos[0]


def run_phase_2(ground_truth_final_x):
    """
    Uses the CalibrationEngine to find the correct friction parameter.
    """
    # 1. Initialize the engine with our simulation parameters.
    engine = CalibrationEngine(
        simulation_steps=SIMULATION_STEPS,
        impulse_to_apply=IMPULSE_TO_APPLY
    )

    # 2. Run the calibration process.
    final_friction_guess = engine.calibrate(ground_truth_final_x)

    # 3. Print the results.
    print("\n--- Calibration Results ---")
    print(f"True Friction Value was:      {GROUND_TRUTH_FRICTION:.4f}")
    print(f"Calibrated Friction Value is: {final_friction_guess:.4f}")
    
    final_error = abs(GROUND_TRUTH_FRICTION - final_friction_guess)
    print(f"Final Error in Friction:      {final_error:.4f}")
    print("-----------------------------")
    
    # 4. Return the entire engine so we can access its history for plotting.
    return engine


def run_phase_3(engine):
    """
    Visualizes the calibration process by plotting the error over iterations.
    """
    print("\n--- Phase 3: Visualizing Calibration Convergence ---")
    
    history = engine.calibration_history
    if not history:
        print("No calibration history to plot.")
        return

    # Extract data from the history for plotting
    iterations = [item['iteration'] for item in history]
    errors = [item['error'] for item in history]

    # Create the plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, errors, marker='o', linestyle='-', color='b')
    
    # Add titles and labels for clarity, making it suitable for the paper
    plt.title('Calibration Convergence: Positional Error vs. Iteration')
    plt.xlabel('Iteration Number')
    plt.ylabel('Positional Error (units)')
    plt.grid(True)
    plt.xticks(iterations) # Ensure we have clean integer ticks for each iteration

    # Ensure the figures directory exists inside the paper folder
    figures_dir = 'paper/figures'
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)
        print(f"Created directory: {figures_dir}")
        
    # Save the plot to a file
    plot_path = os.path.join(figures_dir, 'calibration_convergence.png')
    plt.savefig(plot_path)

    print(f"Convergence plot saved to: {plot_path}")
    print("This plot can now be included in the LaTeX paper.")
    print("--------------------------------------------------")


if __name__ == "__main__":
    # Run Phase 1 to see the problem
    ground_truth_outcome = run_phase_1()
    
    # Add a small pause so it's easy to read the output
    time.sleep(1) 
    
    # Run Phase 2 to solve the problem and get the engine instance back
    calibration_engine = run_phase_2(ground_truth_outcome)
    
    # Run Phase 3 to visualize the results from the engine
    run_phase_3(calibration_engine)
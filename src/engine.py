from src.simulator import Simulator

class CalibrationEngine:
    """
    Manages the process of self-calibration by adjusting a simulation's
    parameters to match observed outcomes from a "ground truth" source.
    """
    def __init__(self, simulation_steps, impulse_to_apply):
        """
        Initializes the calibration engine.

        Args:
            simulation_steps (int): The number of steps each trial runs for.
            impulse_to_apply (tuple): The impulse force to apply in each trial.
        """
        self.simulation_steps = simulation_steps
        self.impulse = impulse_to_apply
        self.calibration_history = [] # To store results from each iteration

    def _run_trial(self, friction_guess):
        """
        Runs a single simulation with a given friction parameter.

        Args:
            friction_guess (float): The friction value to test.

        Returns:
            float: The final X position of the object in the trial simulation.
        """
        trial_sim = Simulator(friction=friction_guess)
        trial_sim.add_dynamic_box()
        trial_sim.apply_impulse(self.impulse)
        
        for _ in range(self.simulation_steps):
            trial_sim.step()
            
        final_state = trial_sim.get_object_state()
        return final_state[0] # We only care about the final X position

    def calibrate(self, ground_truth_x_pos, max_iterations=10, tolerance=1.0):
        """
        Runs the calibration loop to find the friction parameter that results
        in a final position matching the ground_truth_x_pos.

        This implementation uses a binary search algorithm.

        Args:
            ground_truth_x_pos (float): The target final X position to match.
            max_iterations (int): The maximum number of guesses to make.
            tolerance (float): The acceptable error margin to stop calibrating.

        Returns:
            float: The best guess for the friction parameter.
        """
        print("--- Phase 2: Starting Calibration Loop ---")
        
        # We assume friction is between 0.0 and 1.0 for the search
        low_bound = 0.0
        high_bound = 1.0
        best_guess = -1

        for i in range(max_iterations):
            # Guess the midpoint of our current search range
            current_guess = (low_bound + high_bound) / 2
            
            # Run a simulation with that guess
            trial_result_x = self._run_trial(current_guess)
            
            error = abs(trial_result_x - ground_truth_x_pos)

            # Store history for later analysis/plotting
            self.calibration_history.append({
                'iteration': i + 1,
                'guess': current_guess,
                'error': error
            })
            
            print(f"Iteration {i+1:02d}: Guess={current_guess:.4f}, Error={error:.2f}")

            # Check for success
            if error <= tolerance:
                print(f"\nCalibration successful! Converged within tolerance.")
                best_guess = current_guess
                break

            # --- Binary Search Logic ---
            # If our trial object went farther than the real one, it means
            # our friction guess was too LOW. So, we need to search in the
            # upper half of the current range.
            if trial_result_x > ground_truth_x_pos:
                low_bound = current_guess
            # Otherwise, our friction guess was too HIGH, and the object
            # didn't travel far enough. We need to search in the lower half.
            else:
                high_bound = current_guess
            
            best_guess = current_guess

        if error > tolerance:
             print(f"\nCalibration finished after max iterations.")

        print("------------------------------------------")
        return best_guess
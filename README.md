## Project Structure

This repository implements the reproducible framework for driving-simulator experiments. The folder layout is organised as follows:

- **main.py**  
  Entry point of the framework. Runs the automated pipeline that generates a full experiment design.  
  - Automatically generates experiments as per user-specified parameters, including:  
    - Geometrical design (lanes, on-ramp length, main freeway length).  
    - CAV setup (number of vehicles, their positions, assigned controllers, etc.).  
    - Additional experimental configuration options.  
  - Calls helper modules in `GenerateExperiment/` to build road geometry, vehicles, and experiment logic.  
  - Produces the final Webots world file (`ExperimentDesign.wbt`) inside `worlds/`.


- **GenerateExperiment/**  
  Backend modules used by `main.py`. Contains Python code for:
  - `constants.py` – shared constants (lane width, defaults, etc.).  
  - `geometry.py` – road geometry builders.  
  - `cars.py` – vehicle prototypes and placement.  
  - Other utilities supporting experiment generation.  

- **controllers/**  
  Vehicle controllers written in Python or C. Includes:
  - Manual driver controller for participant vehicle.  
  - Automated controllers for CAVs in the merge area and downstream.  
  - Supporting controllers for auxiliary vehicles (e.g., surrounding traffic).
  - Traffic lights used in the experiment

- **worlds/**  
  Stores the generated Webots world files.  
  - Main output is `GenerateExperiment.wbt`, representing the complete reproducible driving-simulator experiment.

- **protos/**  
  Custom Webots PROTO definitions used in the experiment. Includes:
  - Vehicle prototypes.  
  - Traffic-light and other infrastructure models.  

- **textures/**  
  Image textures used by road segments, scenery, and objects.  

---

### Workflow
1. Run `main.py` with experiment parameters.  
2. `main.py` uses `GenerateExperiment/` modules to construct geometry and logic.  
3. A world file is created in `worlds/`.  
4. Controllers in `controllers/` execute vehicle behaviours during the simulation.  
5. PROTOs and textures provide reusable models and appearance definitions.  

This modular structure ensures that experiments are transparent, parameterised, and reproducible.

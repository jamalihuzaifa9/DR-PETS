# DR-PETS: A Distributionally Robust Extension of PETS

**DR-PETS** builds on the Probabilistic Ensembles with Trajectory Sampling (PETS) algorithm, a popular model-based reinforcement learning (MBRL) method known for its uncertainty-aware planning using probabilistic ensembles. However, PETS lacks robustness guarantees against epistemic uncertainty, which limits its reliability in real-world settings.

To address this, DR-PETS introduces a distributionally robust framework that models uncertainty via ambiguity sets and optimizes for the worst-case expected return. By reformulating the planning problem into a tractable convex optimization and integrating it as a regularized cost in PETS’s loop, DR-PETS achieves certified robustness. Experiments on pendulum and cart-pole tasks show consistent performance under adversarial perturbations where PETS fails.

## Setup

This codebase was tested on the following environment:
- **OS**: Ubuntu 18.04  
- **CUDA**: 9.0  
- **Python**: 3.6

You can set up the Python environment using either the `requirements.txt` file or the provided `conda_env.yml` file in the repository.

### MuJoCo Installation

Before running the code, make sure to install **MuJoCo 1.30**:

1. Download MuJoCo 1.30 from the [official website](https://www.roboti.us/index.html).
2. Extract the contents to `~/.mujoco/mujoco130`.
3. Place your MuJoCo license file (`mjkey.txt`) in the `~/.mujoco` directory.
4. Add the MuJoCo binaries to your library path:

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.mujoco/mujoco130/bin


# Runs both EvalN and EvalD
# Produces: D_results.csv, N_results.csv, n.png, d.png

from eval.EvalN import startN
from eval.EvalD import startD

# run EvalN
startN()

# run EvalD
startD()
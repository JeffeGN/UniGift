import matplotlib
matplotlib.use("Agg")

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*FigureCanvasAgg.*")

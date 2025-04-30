GA_MODEL_FILE: str = "vehicular_fuel_efficiency_equation"

GA_STOP_FLAG_FILE: str = "to_safely_stop_genetic_learner.deleteme"

GA_POPULATION_SIZE: int = 8
GA_GENERATION_GOAL: int = 1000000
GA_FITNESS_GOAL: float = 3
GA_NUMBER_OF_PARENTS: int = 4
GA_NUMBER_OF_GENES_TO_MUTATE: int = 1
GA_NUMBER_OF_THREADS: int = 5 # number of threads/processes to use for GA
GENES_PER_VARIABLE: int = 40
NUMBER_OF_VARIABLES: int = 9
GA_CHROMOSOME_LENGTH: int = GENES_PER_VARIABLE * NUMBER_OF_VARIABLES

DATA_FILE_PATH: str = "K:/Downloads/Toyota Corolla Automatic 2009.csv"

SOLUTION_FIGURE_SAVE_DIRECTORY: str = "solution_figure/"
SOLUTION_FIGURE_SAVE_NAME_PREFIX: str = "solution_"
SOLUTION_FIGURE_SIZE_INCHES: tuple[float, float] = (18.0, 18.0)
SOLUTION_FIGURE_RESOLUTION_DPI: float = 200

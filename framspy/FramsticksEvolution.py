import argparse
import csv
import multiprocessing
import os
import random
import shutil
import sys
import tempfile
import time
import numpy as np
import frams
from deap import creator, base, tools, algorithms
from FramsticksLib import FramsticksLib

# Note: this may be less efficient than running the evolution directly in Framsticks, so if performance is key, compare both options.


FITNESS_VALUE_INFEASIBLE_SOLUTION = -999999.0  # DEAP expects fitness to always be a real value (not None), so this special value indicates that a solution is invalid, incorrect, or infeasible. [Related: https://github.com/DEAP/deap/issues/30 ]. Using float('-inf') or -sys.float_info.max here causes DEAP to silently exit. If you are not using DEAP, set this constant to None, float('nan'), or another special/non-float value to avoid clashing with valid real fitness values, and handle such solutions appropriately as a separate case.


def genotype_within_constraint(genotype, dict_criteria_values, criterion_name, constraint_value):
	REPORT_CONSTRAINT_VIOLATIONS = False
	if constraint_value is not None:
		actual_value = dict_criteria_values[criterion_name]
		if actual_value > constraint_value:
			if REPORT_CONSTRAINT_VIOLATIONS:
				print('Genotype "%s" assigned a special ("infeasible solution") fitness because it violates constraint "%s": %s exceeds the threshold of %s' % (genotype, criterion_name, actual_value, constraint_value))
			return False
	return True


def frams_evaluate(frams_lib, individual):
	FITNESS_CRITERIA_INFEASIBLE_SOLUTION = [FITNESS_VALUE_INFEASIBLE_SOLUTION] * len(OPTIMIZATION_CRITERIA)  # this special fitness value indicates that the solution should not be propagated via selection ("that genotype is invalid"). The floating point value is only used for compatibility with DEAP. If you implement your own optimization algorithm, instead of a negative value in this constant, use a special value like None to properly distinguish between feasible and infeasible solutions.
	genotype = individual[0]  # individual[0] because we can't (?) have a simple str as a DEAP genotype/individual, only list of str.
	data = frams_lib.evaluate([genotype])
	# print("Evaluated '%s'" % genotype, 'evaluation is:', data)
	valid = True
	try:
		first_genotype_data = data[0]
		evaluation_data = first_genotype_data["evaluations"]
		default_evaluation_data = evaluation_data[""]
		fitness = [default_evaluation_data[crit] for crit in OPTIMIZATION_CRITERIA]
		if OPTIMIZATION_CRITERIA == ["vertpos"] and default_evaluation_data["vertpos"] <= 0:
			fitness = [-0.001 / (1 + default_evaluation_data["numjoints"])]
	except (KeyError, TypeError) as e:  # the evaluation may have failed for an invalid genotype (such as X[@][@] with "Don't simulate genotypes with warnings" option), or because the creature failed to stabilize, or for some other reason
		valid = False
		print('Problem "%s" so could not evaluate genotype "%s", hence assigned it a special ("infeasible solution") fitness value: %s' % (str(e), genotype, FITNESS_CRITERIA_INFEASIBLE_SOLUTION))
	if valid:
		default_evaluation_data['numgenocharacters'] = len(genotype)  # add one new key to the dictionary for consistent constraint checking below
		valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numparts', parsed_args.max_numparts)
		valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numjoints', parsed_args.max_numjoints)
		valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numneurons', parsed_args.max_numneurons)
		valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numconnections', parsed_args.max_numconnections)
		valid &= genotype_within_constraint(genotype, default_evaluation_data, 'numgenocharacters', parsed_args.max_numgenochars)
	if not valid:
		fitness = FITNESS_CRITERIA_INFEASIBLE_SOLUTION
	return fitness


def frams_crossover(frams_lib, individual1, individual2):
	geno1 = individual1[0]  # individual[0] because we can't (?) have a simple str as a DEAP genotype/individual, only list of str.
	geno2 = individual2[0]  # individual[0] because we can't (?) have a simple str as a DEAP genotype/individual, only list of str.
	individual1[0] = frams_lib.crossOver(geno1, geno2)
	individual2[0] = frams_lib.crossOver(geno1, geno2)
	return individual1, individual2


def frams_mutate(frams_lib, individual):
	individual[0] = frams_lib.mutate([individual[0]])[0]  # individual[0] because we can't (?) have a simple str as a DEAP genotype/individual, only list of str.
	return individual,


def frams_getsimplest(frams_lib, genetic_format, initial_genotype):
	return initial_genotype if initial_genotype is not None else frams_lib.getSimplest(genetic_format)


def is_feasible_fitness_value(fitness_value: float) -> bool:
	assert isinstance(fitness_value, float), f"feasible_fitness({fitness_value}): argument is not of type 'float', it is of type '{type(fitness_value)}'"  # since we are using DEAP, we unfortunately must represent the fitness of an "infeasible solution" as a float...
	return fitness_value != FITNESS_VALUE_INFEASIBLE_SOLUTION  # ...so if a valid solution happens to have fitness equal to this special value, such a solution will be considered infeasible :/


def is_feasible_fitness_criteria(fitness_criteria: tuple) -> bool:
	return all(is_feasible_fitness_value(fitness_value) for fitness_value in fitness_criteria)


def select_feasible(individuals):
	"""
	Filters out only feasible individuals (i.e., with fitness different from FITNESS_VALUE_INFEASIBLE_SOLUTION).
	"""
	# for ind in individuals:
	#	print(ind.fitness.values, ind)
	feasible_individuals = [ind for ind in individuals if is_feasible_fitness_criteria(ind.fitness.values)]
	count_all = len(individuals)
	count_infeasible = count_all - len(feasible_individuals)
	if count_infeasible != 0:
		print("Selection: ignoring %d infeasible solution%s in a population of size %d" % (count_infeasible, 's' if count_infeasible > 1 else '', count_all))
	return feasible_individuals


def selTournament_only_feasible(individuals, k, tournsize):
	return tools.selTournament(select_feasible(individuals), k, tournsize=tournsize)


def selNSGA2_only_feasible(individuals, k, toolboxclone):
	feasible = select_feasible(individuals)
	# tools.selNSGA2() is unfortunately unable to select more (k) from less (len(feasible)).
	# It assumes it receives at least k individuals as an argument, and only shrinks the input.
	# If it receives fewer than k individuals, the population gets permanently smaller and the k argument here decreases accordingly.
	# To prevent this, we duplicate the set of feasible individuals until it has at least k individuals:
	while len(feasible)<k:
		feasible = feasible + [toolboxclone(ind) for ind in feasible] # must copy (clone) individuals so we have independent instances in population, not multiple references to the same individuals
	return tools.selNSGA2(feasible, k)


def prepareToolbox(frams_lib, OPTIMIZATION_CRITERIA, tournament_size, genetic_format, initial_genotype):
	if not hasattr(creator, "FitnessMax"):
		creator.create("FitnessMax", base.Fitness, weights=[1.0] * len(OPTIMIZATION_CRITERIA))
	if not hasattr(creator, "Individual"):
		creator.create("Individual", list, fitness=creator.FitnessMax)  # would be nice to have "str" instead of unnecessary "list of str"

	toolbox = base.Toolbox()
	toolbox.register("attr_simplest_genotype", frams_getsimplest, frams_lib, genetic_format, initial_genotype)  # "Attribute generator"
	# (failed) struggle to have an individual which is a simple str, not a list of str
	# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_frams)
	# https://stackoverflow.com/questions/51451815/python-deap-library-using-random-words-as-individuals
	# https://github.com/DEAP/deap/issues/339
	# https://gitlab.com/santiagoandre/deap-customize-population-example/-/blob/master/AGbasic.py
	# https://groups.google.com/forum/#!topic/deap-users/22g1kyrpKy8
	toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_simplest_genotype, 1)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)
	toolbox.register("evaluate", frams_evaluate, frams_lib)
	toolbox.register("mate", frams_crossover, frams_lib)
	toolbox.register("mutate", frams_mutate, frams_lib)
	if len(OPTIMIZATION_CRITERIA) <= 1:
		# toolbox.register("select", tools.selTournament, tournsize=tournament_size) # without explicitly filtering out infeasible solutions - eliminating/discriminating infeasible solutions during selection would only rely on their relatively poor fitness value
		toolbox.register("select", selTournament_only_feasible, tournsize=tournament_size)
	else:
		# toolbox.register("select", selNSGA2) # without explicitly filtering out infeasible solutions - eliminating/discriminating infeasible solutions during selection would only rely on their relatively poor fitness value
		toolbox.register("select", selNSGA2_only_feasible, toolboxclone=toolbox.clone)
	return toolbox


def parseArguments():
	parser = argparse.ArgumentParser(description='Run this program with "python -u %s" if you want to disable buffering of its output.' % sys.argv[0])
	parser.add_argument('-path', type=ensureDir, required=True, help='Path to Framsticks library without trailing slash.')
	parser.add_argument('-lib', required=False, help='Library name. If not given, "frams-objects.dll" (or .so or .dylib) is assumed depending on the platform.')
	parser.add_argument('-sim', required=False, default="eval-allcriteria.sim", help="The name of the .sim file with settings for evaluation, mutation, crossover, and similarity estimation. If not given, \"eval-allcriteria.sim\" is assumed by default. Must be compatible with the \"standard-eval\" expdef. If you want to provide more files, separate them with a semicolon ';'.")

	parser.add_argument('-genformat', required=False, help='Genetic format for the simplest initial genotype, for example 4, 9, or B. If not given, f1 is assumed.')
	parser.add_argument('-initialgenotype', required=False, help='The genotype used to seed the initial population. If given, the -genformat argument is ignored.')

	parser.add_argument('-opt', required=True, help='optimization criteria: vertpos, velocity, distance, vertvel, lifespan, numjoints, numparts, numneurons, numconnections (or other as long as it is provided by the .sim file and its .expdef). For multiple criteria optimization, separate the names by the comma.')
	parser.add_argument('-popsize', type=int, default=50, help="Population size, default: 50.")
	parser.add_argument('-generations', type=int, default=5, help="Number of generations, default: 5.")
	parser.add_argument('-stagnation', type=int, default=None, help="Stop after this many generations without improving the Hall of Fame. Default: disabled.")
	parser.add_argument('-runs', type=int, default=1, help="Number of independent evolutionary runs, default: 1.")
	parser.add_argument('-workers', type=int, default=1, help="Number of processes used for independent runs, default: 1.")
	parser.add_argument('-output_prefix', default='evolution_results', help="Prefix for generated CSV files.")
	parser.add_argument('-seed', type=int, default=None, help="Base random seed. Run number is added to this value.")
	parser.add_argument('-dynamic_mutation_schedule', action='store_true', help="Start with structural f1 mutations and transition to neural fine-tuning.")
	parser.add_argument('-tournament', type=int, default=5, help="Tournament size, default: 5.")
	parser.add_argument('-pmut', type=float, default=0.9, help="Probability of mutation, default: 0.9")
	parser.add_argument('-pxov', type=float, default=0.2, help="Probability of crossover, default: 0.2")
	parser.add_argument('-hof_size', type=int, default=10, help="Number of genotypes in Hall of Fame. Default: 10.")
	parser.add_argument('-hof_savefile', required=False, help='If set, Hall of Fame will be saved in the Framsticks file format (recommended extension *.gen).')

	parser.add_argument('-max_numparts', type=int, default=None, help="Maximum number of Parts. Default: no limit")
	parser.add_argument('-max_numjoints', type=int, default=None, help="Maximum number of Joints. Default: no limit")
	parser.add_argument('-max_numneurons', type=int, default=None, help="Maximum number of Neurons. Default: no limit")
	parser.add_argument('-max_numconnections', type=int, default=None, help="Maximum number of Neural connections. Default: no limit")
	parser.add_argument('-max_numgenochars', type=int, default=None, help="Maximum number of characters in genotype (including the format prefix, if any). Default: no limit")
	return parser.parse_args()


def ensureDir(string):
	if os.path.isdir(string):
		return string
	else:
		raise NotADirectoryError(string)


def save_genotypes(filename, OPTIMIZATION_CRITERIA, hof):
	from framsfiles import writer as framswriter
	with open(filename, "w") as outfile:
		for ind in hof:
			keyval = {}
			for i, k in enumerate(OPTIMIZATION_CRITERIA):  # construct a dictionary with criteria names and their values
				keyval[k] = ind.fitness.values[i]  # TODO it would be better to save in Individual (after evaluation) all fields returned by Framsticks, and get these fields here, not just the criteria that were actually used as fitness in evolution.
			outfile.write(framswriter.from_collection({"_classname": "org", "genotype": ind[0], **keyval}))
			outfile.write("\n")
	print("Saved '%s' (%d)" % (filename, len(hof)))


def set_dynamic_mutation_probabilities(generation):
	"""Move from body-shape exploration to neural fine-tuning over 60 generations."""
	if generation <= 30:
		progress = generation / 30.0
		start = (0.25, 0.12, 0.18, 0.12, 0.02, 0.04, 0.05, 0.2, 0.03)
		end = (0.15, 0.06, 0.10, 0.12, 0.03, 0.08, 0.10, 0.7, 0.05)
	elif generation <= 60:
		progress = (generation - 30) / 30.0
		start = (0.15, 0.06, 0.10, 0.12, 0.03, 0.08, 0.10, 0.7, 0.05)
		end = (0.05, 0.02, 0.03, 0.08, 0.03, 0.10, 0.12, 1.5, 0.08)
	else:
		return
	values = [first + progress * (last - first) for first, last in zip(start, end)]
	for parameter, value in zip(
		('f1_smX', 'f1_smJunct', 'f1_smComma', 'f1_smModif', 'f1_nmNeu', 'f1_nmConn', 'f1_nmProp', 'f1_nmWei', 'f1_nmVal'),
		values,
	):
		setattr(frams.GenMan, parameter, value)


def run_evolution(task):
	"""Run one independent experiment in the current process."""
	arguments, run_id = task
	global parsed_args, OPTIMIZATION_CRITERIA
	parsed_args = argparse.Namespace(**arguments)
	OPTIMIZATION_CRITERIA = parsed_args.opt.split(",")
	if parsed_args.seed is not None:
		seed = parsed_args.seed + run_id
		random.seed(seed)
		np.random.seed(seed)

	FramsticksLib.DETERMINISTIC = False
	worker_home = tempfile.mkdtemp(prefix='framsticks-home-')
	framsLib = FramsticksLib(parsed_args.path, parsed_args.lib, parsed_args.sim, home_dir=worker_home)
	if parsed_args.dynamic_mutation_schedule:
		set_dynamic_mutation_probabilities(0)
	print("\n---------------------------> f9 mutation intensity =", frams.GenMan.f9_mut)
	mutation_intensity = float(frams.GenMan.f9_mut._value())
	print("Run %d: f9 mutation intensity = %s" % (run_id, mutation_intensity), flush=True)
	toolbox = prepareToolbox(framsLib, OPTIMIZATION_CRITERIA, parsed_args.tournament, '1' if parsed_args.genformat is None else parsed_args.genformat, parsed_args.initialgenotype)
	pop = toolbox.population(n=parsed_args.popsize)
	hof = tools.HallOfFame(parsed_args.hof_size)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	filter_feasible_for_function = lambda function, values: function(list(filter(is_feasible_fitness_criteria, values))) if any(map(is_feasible_fitness_criteria, values)) else [float('nan')] * len(OPTIMIZATION_CRITERIA)
	stats.register("avg", lambda values: filter_feasible_for_function(np.mean, values))
	stats.register("stddev", lambda values: filter_feasible_for_function(np.std, values))
	stats.register("min", lambda values: filter_feasible_for_function(np.min, values))
	stats.register("max", lambda values: filter_feasible_for_function(np.max, values))

	def statistic_value(record, name, index):
		values = np.asarray(record[name])
		return float(values) if values.ndim == 0 else values[index]

	start_time = time.perf_counter()
	rows = []
	best_so_far = None
	stagnant_generations = 0

	def evaluate_and_record(generation):
		nonlocal best_so_far, stagnant_generations
		invalid_individuals = [ind for ind in pop if not ind.fitness.valid]
		fitnesses = toolbox.map(toolbox.evaluate, invalid_individuals)
		for individual, fitness in zip(invalid_individuals, fitnesses):
			individual.fitness.values = fitness
		hof.update(pop)
		record = stats.compile(pop)
		row = {
			'run': run_id,
			'generation': generation,
			'genetic_format': parsed_args.genformat or '1',
			'mutation_intensity': mutation_intensity,
		}
		for index, criterion in enumerate(OPTIMIZATION_CRITERIA):
			row['best_' + criterion] = statistic_value(record, 'max', index)
			row['avg_' + criterion] = statistic_value(record, 'avg', index)
			row['stddev_' + criterion] = statistic_value(record, 'stddev', index)
		rows.append(row)
		if generation == 0 or generation % 10 == 0:
			print('Run %d: generation %d/%d, best %s=%s, stagnant=%d' % (run_id, generation, parsed_args.generations, OPTIMIZATION_CRITERIA[0], row['best_' + OPTIMIZATION_CRITERIA[0]], stagnant_generations), flush=True)
		current_best = tuple(hof[0].fitness.values) if hof else None
		if current_best != best_so_far:
			best_so_far = current_best
			stagnant_generations = 0
		else:
			stagnant_generations += 1

	evaluate_and_record(0)
	for generation in range(1, parsed_args.generations + 1):
		if parsed_args.stagnation is not None and stagnant_generations >= parsed_args.stagnation:
			break
		if parsed_args.dynamic_mutation_schedule:
			set_dynamic_mutation_probabilities(generation)
		offspring = toolbox.select(pop, len(pop))
		offspring = list(map(toolbox.clone, offspring))
		offspring = algorithms.varAnd(offspring, toolbox, parsed_args.pxov, parsed_args.pmut)
		pop[:] = offspring
		evaluate_and_record(generation)

	duration = time.perf_counter() - start_time
	summary = {
		'run': run_id,
		'genetic_format': parsed_args.genformat or '1',
		'mutation_intensity': mutation_intensity,
		'generations_completed': rows[-1]['generation'],
		'duration_seconds': duration,
		'hof_genotype': hof[0][0] if hof else '',
	}
	for index, criterion in enumerate(OPTIMIZATION_CRITERIA):
		summary['hof_' + criterion] = hof[0].fitness.values[index] if hof else float('nan')
	if parsed_args.hof_savefile is not None:
		root, extension = os.path.splitext(parsed_args.hof_savefile)
		if '{run}' in parsed_args.hof_savefile:
			filename = parsed_args.hof_savefile.replace('{run}', str(run_id + 1))
		else:
			filename = parsed_args.hof_savefile if parsed_args.runs == 1 else '%s.run%d%s' % (root, run_id, extension)
		save_genotypes(filename, OPTIMIZATION_CRITERIA, hof)
	shutil.rmtree(worker_home, ignore_errors=True)
	return rows, summary


def write_csv(filename, rows):
	if not rows:
		return
	with open(filename, 'w', newline='') as output:
		writer = csv.DictWriter(output, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)
	print("Saved '%s' (%d rows)" % (filename, len(rows)))


def main():
	parsed_args = parseArguments()
	print("Argument values:", ", ".join(['%s=%s' % (arg, getattr(parsed_args, arg)) for arg in vars(parsed_args)]))
	if parsed_args.runs < 1 or parsed_args.workers < 1:
		raise ValueError('-runs and -workers must be positive')
	tasks = [(vars(parsed_args), run_id) for run_id in range(parsed_args.runs)]
	if parsed_args.workers == 1:
		results = [run_evolution(task) for task in tasks]
	else:
		with multiprocessing.Pool(processes=parsed_args.workers) as pool:
			results = pool.map(run_evolution, tasks)
	rows = [row for run_rows, _ in results for row in run_rows]
	summaries = [summary for _, summary in results]
	write_csv(parsed_args.output_prefix + '_generations.csv', rows)
	write_csv(parsed_args.output_prefix + '_runs.csv', summaries)
	print('Best individuals:')
	for summary in summaries:
		print('Run %d: %s\t<--\t%s' % (summary['run'], summary['hof_' + parsed_args.opt.split(',')[0]], summary['hof_genotype']))


if __name__ == "__main__":
	main()

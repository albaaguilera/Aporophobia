import argparse
import multiprocessing as mp
from itertools import chain, combinations
from model import CityModel, lista_distritos, dummy_norms

parser = argparse.ArgumentParser(description="Run a sample of models.")
parser.add_argument('-N', default=100, type=int, help="number of agents")
parser.add_argument('-T', default=100, type=int, help="number of time steps")
parser.add_argument('-M', default=100, type=int, help="number of samples per \
                    norm configuration")

args = parser.parse_args()
N, T, M = args.N, args.T, args.M


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def run_model(I):
    process_id = mp.current_process().pid
    print(process_id)

    for index, norm_config in enumerate(powerset(dummy_norms)):
        for i in range(I):
            barcelona = CityModel('Barcelona', lista_distritos, N, norm_config)
            # for _ in range(T):
            #     barcelona.step()
            
            # collect and save data
            run_id = f"{process_id}_{index}_{i}"
            # model_vars_df = barcelona.datacollector.get_model_vars_dataframe()
            # agent_vars_df = barcelona.datacollector.get_agent_vars_dataframe()
            # model_vars_df.to_csv(f"results/model_vars_{run_id}.csv", sep=';')
            # agent_vars_df.to_csv(f"results/agent_vars_{run_id}.csv", sep=';')


if __name__ == '__main__':

    n_cpus = mp.cpu_count()
    print(n_cpus)
    load_per_core = M // n_cpus

    pool = mp.Pool(n_cpus)
    _ = pool.starmap(run_model, [(load_per_core,)]*n_cpus)
    pool.close()

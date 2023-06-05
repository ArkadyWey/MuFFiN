import subprocess
import argparse

def main(path_start, initialisation, num_nodes, r_max, alph=1.0, beta=0.01):
    """
    """
    reps = range(r_max+1)
    for r in reps:

        print("Running for r-{} of r_max-{}".format(r,r_max))

        # Build parameters
        path_add_sim="/init-{}/N-{}".format(initialisation,num_nodes)
        path_add_rep="/r-{}".format(r) 

        path_sim=path_start+path_add_sim
        path_rep=path_start+path_add_sim+path_add_rep

        # Execute inner script
        #subprocess.run(["python3","run_preprocess_2D.py",        "--path_results", path_rep, "--initialisation", initialisation, "--num_nodes", str(num_nodes)]) 
        subprocess.run("python3    run_preprocess_2D.py           --path_results " + path_rep + " --num_nodes " + str(num_nodes) + " --initialisation " + initialisation + " --alph " + str(alph) + " --beta " + str(beta), shell=True)

    print("Calculating statistics...")

    #subprocess.run(["python3", "run_ensemble-preprocess-stats.py", "--path_results", path_sim, "--num_nodes", str(num_nodes), "--initialisation", initialisation, "--r_max", str(r_max), "--alph", alph, "--beta", beta])
    subprocess.run("python3 run_ensemble-preprocess-stats.py --path_results " + path_sim + " --num_nodes " + str(num_nodes) + " --initialisation " + initialisation + " --r_max " + str(r_max), shell=True)


if __name__ == "__main__":

    # Parameters 
    parser = argparse.ArgumentParser()
    parser.add_argument("-pr",    "--path_results",   type=str, help="Path to results")
    parser.add_argument("-rm",    "--r_max",          type=int, help="Number of repeated simulations")
    parser.add_argument("-N",     "--num_nodes",      type=int,   help="Number of nodes in cell")
    parser.add_argument("-init",  "--initialisation", type=str,   help="Structure of cell")
    parser.add_argument("-a",     "--alph",           type=float,   help="alpha")
    parser.add_argument("-b",     "--beta",           type=float,   help="beta")
    args = parser.parse_args()

    path_start     = args.path_results
    initialisation = args.initialisation
    num_nodes      = args.num_nodes
    r_max          = args.r_max 
    alph           = args.alph 
    beta           = args.beta 
    
    main(path_start=path_start, 
         initialisation=initialisation, 
         num_nodes=num_nodes, 
         r_max=r_max, 
         alph=alph, 
         beta=beta)


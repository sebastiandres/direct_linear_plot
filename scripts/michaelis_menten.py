import pandas as pd
import numpy as np
import itertools

def solver(df):
    """
    Obtains the parameters Vmax and Km from the Michaelis Menten model
    using data values and the direct linear plot - aka estimation by the medians.
    """
    # Get the data
    s = df["s"]
    v = df["v"]
    # Define the equations
    coef_Km = -v
    coef_Vmax = s
    rhs = s * v
    # Obtain all the possible combinations
    indexing = np.arange(len(s))
    combinations = itertools.combinations(indexing, 2)
    # Solve the equations and store the results
    Km_estimations = []
    Vmax_estimations = []
    for i, j in combinations:
        A = np.array([[coef_Km[i], coef_Vmax[i]], [coef_Km[j], coef_Vmax[j]]])
        #print(np.linalg.det(A))
        b = np.array([rhs[i], rhs[j]])
        Km_ij, Vmax_ij = np.linalg.solve(A, b)
        Km_estimations.append(Km_ij)
        Vmax_estimations.append(Vmax_ij)
    # Obtain the median of the estimations
    Km_DLP = np.median(Km_estimations)
    Vmax_DLP = np.median(Vmax_estimations)
    # Obtain the linear regression
    A = np.array([coef_Km, coef_Vmax]).T
    Km_LR, Vmax_LR = np.linalg.lstsq(A, rhs, rcond=None)[0]
    # Auxiliar print
    solution = {}
    solution["direct_linear_plot"] = {"Vmax": Vmax_DLP, "Km": Km_DLP}
    solution["linear_regression"] = {"Vmax": Vmax_LR, "Km": Km_LR}
    return solution


def error_analysis(Vmax, Km, mu, sigma, N):
    """
    Compares Direct Linear Plot (DLP) and Linear Regression (LR) 
    using N experiments for parameter estimations.
    """
    s_min = 1
    s_max = 10
    # Generate the base experiment (true s and v) with no error
    s = s_generation(s_min, s_max, n_s=10)
    v = v_generation(Vmax, Km, s)
    df = data_generation(s, v)
    # Add perturbations to the data
    DLP = {"Vmax": [], "Km": []}
    LR = {"Vmax": [], "Km": []}
    data = []
    for i in range(N):
        df_i = df.copy()
        df_i["v"] = data_perturbation(df_i["v"], mu, sigma)
        # Obtain the estimations
        solution = solver(df_i)
        # Store the data
        data.append(df_i)
        # Store the results
        DLP["Vmax"].append(solution["direct_linear_plot"]["Vmax"])
        DLP["Km"].append(solution["direct_linear_plot"]["Km"])
        LR["Vmax"].append(solution["linear_regression"]["Vmax"])
        LR["Km"].append(solution["linear_regression"]["Km"])
    # Convert to dataframe
    DLP = pd.DataFrame(DLP)
    LR = pd.DataFrame(LR)        
    # Return the results
    return data, DLP, LR


def sensitivity_analysis(Vmax, Km, mu, sigma, N, e_index, e_min, e_max, n_e=20):
    """
    Compares Direct Linear Plot (DLP) and Linear Regression (LR) 
    using N experiments for parameter estimations.
    """
    s_min = 0.2
    s_max = 2.0
    # Generate the base experiment (true s and v) with no error
    s = s_generation(s_min, s_max, n_s=10)
    v = v_generation(Vmax, Km, s)
    df = data_generation(s, v)
    # Create the error vector
    e = np.linspace(e_min, e_max, n_e)
    # Add perturbations to the data
    DLP = {}
    LR = {}
    for i in range(N):
        DLP[i] = {"Vmax": [], "Km": [], "Error": []}
        LR[i] = {"Vmax": [], "Km": [], "Error": []}
        df_i = df.copy()
        df_i["v"] = data_perturbation(df_i["v"], mu, sigma, e_index) # Perturbate all with the same error, except e_index
        for error in e:
            df_i_error = df_i.copy()
            df_i_error.loc[e_index, "v"] = df_i_error.loc[e_index, "v"] + error # Perturbate e_index with the error
            # Obtain the estimations
            solution = solver(df_i_error)
            # Store the results
            DLP[i]["Vmax"].append(solution["direct_linear_plot"]["Vmax"])
            DLP[i]["Km"].append(solution["direct_linear_plot"]["Km"])
            DLP[i]["Error"].append(error)
            LR[i]["Vmax"].append(solution["linear_regression"]["Vmax"])
            LR[i]["Km"].append(solution["linear_regression"]["Km"])
            LR[i]["Error"].append(error)
    # Return the results
    return DLP, LR


def data_perturbation(v, mu, sigma, e_index=None):
    """
    Returns random values from a normal distribution
    for the given mean and standard deviation, and adds it
    to the known value of v.
    """
    v_error = np.random.normal(mu, sigma, len(v))
    if e_index is not None:
        v_error[e_index] = 0 # We don't perturbate this value in particular
    return v + v_error

def s_generation(s_min, s_max, n_s=10):
    """
    How to generate the s values?
    """
    # Generate the data
    s = np.linspace(s_min, s_max, n_s)
    return s

def v_generation(Vmax, Km, s):
    """
    Generates data for the Michaelis Menten model
    asuming known parameters Vmax and Km.
    """
    v = Vmax * s / (Km + s)
    return v

def data_generation(s,v):
    # Pack the data
    df = pd.DataFrame({"s": s, "v": v})
    return df

if __name__=="__main__":
    df = data_generation(1, 1, 0.1, 10, n=100, perturbation=0.01)
    df.to_excel("Michaelis_Menten.xlsx", index=False)
    #print(df)
    Vmax, Km = solver(df)
    print(Vmax, Km)
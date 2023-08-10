import pandas as pd
import numpy as np
import itertools

def data_generation(Vmax, Km, s_min, s_max, n=10, perturbation=0.1):
    """
    Generates data for the Michaelis Menten model
    asuming known parameters Vmax and Km.
    """
    # Generate the data
    s = np.linspace(s_min, s_max, n)
    v = Vmax * s / (Km + s)
    # Add some noise
    v = v + perturbation * np.random.randn(n)
    s = s + perturbation * np.random.randn(n)
    # Pack the data
    df = pd.DataFrame({"s": s, "v": v})
    return df

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
        print(np.linalg.det(A))
        b = np.array([rhs[i], rhs[j]])
        Km_ij, Vmax_ij = np.linalg.solve(A, b)
        Km_estimations.append(Km_ij)
        Vmax_estimations.append(Vmax_ij)
    # Obtain the median of the estimations
    Km = np.median(Km_estimations)
    Vmax = np.median(Vmax_estimations)
    # Auxiliar print
    #print("Using the average", np.mean(Km_estimations), np.mean(Vmax_estimations))
    return Vmax, Km

if __name__=="__main__":
    df = data_generation(1, 1, 0.1, 10, n=100, perturbation=0.01)
    df.to_excel("Michaelis_Menten.xlsx", index=False)
    #print(df)
    Vmax, Km = solver(df)
    print(Vmax, Km)
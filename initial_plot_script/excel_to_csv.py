import pandas as pd

def main():

    data_xls = pd.read_excel("measures-of-state-inc-ineq.xls")
    data_xls.to_csv("ineq_data.csv", encoding="utf-8")

if __name__ == "__main__":
    main()
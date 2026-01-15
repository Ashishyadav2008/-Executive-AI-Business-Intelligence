import pandas as pd

def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    # -------- AUTO DATE DETECTION --------
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except:
                pass

    # -------- FORCE NUMERIC CLEAN --------
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df

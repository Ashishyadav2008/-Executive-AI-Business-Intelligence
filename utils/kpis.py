def kpis(df):
    num = df.select_dtypes(include="number")
    return (
        len(df),
        df.shape[1],
        round(num.sum().sum(), 2) if not num.empty else 0,
        round(num.mean().mean(), 2) if not num.empty else 0
    )

def process_query(query, df):
    q = query.lower()

    if "total sales" in q:
        return f"Total Sales: ₹{df['Sales'].sum()}"

    if "profit" in q and "total" in q:
        return f"Total Profit: ₹{df['Profit'].sum()}"

    if "region" in q:
        return df.groupby("Region")["Sales"].sum().to_string()

    if "product" in q and "highest" in q:
        p = df.groupby("Product")["Profit"].sum().idxmax()
        return f"Highest profit product: {p}"

    if "why" in q or "reason" in q:
        trend = df.groupby("Date")["Sales"].sum()
        if trend.iloc[-1] < trend.iloc[0]:
            return "Sales trend is declining. Possible reasons: seasonal drop, pricing issues, or low demand."
        else:
            return "Sales trend is stable or increasing."

    return "Question samajh nahi aaya. Try: total sales, region wise sales, highest profit product."

def get_category_rule_based(text):
    text = text.lower()

    if any(word in text for word in ["ai", "machine learning", "data", "robot"]):
        return "Technology"
    if any(word in text for word in ["stock", "market", "finance", "investment"]):
        return "Finance"
    if any(word in text for word in ["movie", "music", "song", "trailer"]):
        return "Entertainment"
    if any(word in text for word in ["education", "student", "college", "course"]):
        return "Education"
    if any(word in text for word in ["election", "government", "policy", "minister"]):
        return "Politics"

    return "General"


def apply_category(df):
    df["category"] = df["post"].astype(str).apply(get_category_rule_based)
    return df

import google.generativeai as genai

genai.configure(api_key="AIzaSyBQh_Wb9mpt09l1QbqEVYbI0c_xqBJM6Bw")

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_insights(df, platform_name,account_id=None):
    summary = df["post"].head(10).to_list()

    prompt = f"""
    Analyze the following social media posts from {platform_name}.
    Provide:
    1. Overall sentiment
    2. Common topics
    3. User engagement nature

    Posts:
    {summary}
    """

    response = model.generate_content(prompt)
    return response.text

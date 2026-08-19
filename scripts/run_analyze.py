
from app.services.analyze import analyze_review

def test_analyze_review():
    review_text = "The company has a great culture and supportive management, but the compensation could be better."
    result = analyze_review(review_text)
    return result


if __name__ == "__main__":
    print("\n- Running test_analyze_review()...")
    result =test_analyze_review()
    print("\n- Result:", result)
    print("\n -Test completed.")


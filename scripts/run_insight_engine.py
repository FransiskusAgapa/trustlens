from app.services.insight_engine import InsightEngine

if __name__ == "__main__":
    print("\n> Start Testing Insight Engine...")

    engine = InsightEngine()
    ranked_themes = engine.run()
    print("\n> Ranked Themes by Department:")
    for department, themes in ranked_themes.items():
        print(f"- Department : {department}")
        for theme in themes:
            print(f"  - Theme: {theme[0]}, Count: {theme[1]}")

    print("\n> Finish Insight Engine...")
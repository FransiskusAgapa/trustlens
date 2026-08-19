from app.services.processor import ReviewProcessor

if __name__ == "__main__":
    # create ReviewProcessor instance
    processor = ReviewProcessor()

    print("\n> Starting processor...")
    # call def run from the class
    processor.run()
    print("\n> Processor finished.")
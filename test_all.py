from testing import test_generate_dates as tgd

def run_all_tests():
    try:
        tgd.test_monday()
        tgd.test_tuesday()
        tgd.test_wednesday()
        tgd.test_thursday()
        tgd.test_friday()
        tgd.test_saturday()
        tgd.test_sunday()
        print("✅ All weekday tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    run_all_tests()

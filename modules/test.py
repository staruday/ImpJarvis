from wake_word_engine import start_wake_listener


def test_trigger():
    print("🔥 Wake word triggered!")


start_wake_listener(test_trigger)
input("Running... press Enter to stop\n")

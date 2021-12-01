from infection_monkey.master.automated_master import AutomatedMaster

def test_terminate_without_start():
    m = AutomatedMaster(None, None, None)

    # Test that call to terminate does not raise exception
    m.terminate()

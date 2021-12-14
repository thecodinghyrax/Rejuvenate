from tests.test_controller_established import TestControllerEstablished
from tests.test_controller_initial import TestControllerInitial
from tests.test_contoller import TestController
from tests.test_addon import TestAddon



if __name__ =='__main__':
    # I dont understand why I can't run all these tests at the same
    # time but when I try, it will only run the first test and 
    # skip the rest. I still have so much to learn about testing :(
        
    # initial test can be ran in the ini file is original and will only 
    # work on my (drews) local machine  
    # initial_test = TestControllerInitial()
    # initial_test.run_tests()

    # established_test can be ran after the ini file was updated
    # established_tests = TestControllerEstablished()
    # established_tests.run_tests()

    # controller_tests = TestController()
    # controller_tests.run_tests()

    addon_tests = TestAddon()
    addon_tests.run_tests()

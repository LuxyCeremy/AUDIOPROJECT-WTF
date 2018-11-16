import launchpad_py
launchpad = launchpad_py.Launchpad()
# launchpad.ListAll()

launchpad.Open()
launchpad.LedCtrlString("123456",3,3,-1)
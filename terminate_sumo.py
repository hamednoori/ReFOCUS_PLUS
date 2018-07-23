def terminate_sumo(sumo):
    if sumo.returncode == None:
        os.kill(sumo.pid, signal.SIGTERM)
        time.sleep(0.5)
        if sumo.returncode == None:
            print os.__file__
            #os.kill(sumo.pid, signal.SIGKILL)
            time.sleep(1)
            if sumo.returncode == None:
                time.sleep(10)
    
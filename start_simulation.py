def start_simulation(sumo, scenario, network, begin, end, interval, output):
    logging.debug("Finding unused port")
    print("Finding unused port")
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()
    print("remote_port:{0}" .format(remote_port))
    logging.debug("Port %d was found" % remote_port)
    logging.debug("Starting SUMO as a server")
    sumo = subprocess.Popen(["...\\PATH\\Yoursumo.exe", "-c", "...\\PATH\\Your.sumo.cfg", "--tripinfo-output", output,"--device.emissions.probability", "1.0",  "--remote-port", str(remote_port)], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()
    try:     
        traci.init(remote_port)    
        run(network, begin, end, interval)
    except Exception:
        logging.exception("Something bad happened")
    finally:
        logging.exception("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()
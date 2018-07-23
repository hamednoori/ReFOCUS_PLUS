def main():
    # Option handling
    parser = OptionParser(conflict_handler="resolve")#parser = OptionParser()
    parser.add_option("-c", "--command", dest="command", default="sumo", help="The command used to run SUMO [default: %default]", metavar="COMMAND")
    parser.add_option("-s", "--scenario", dest="scenario", default="Your.sumo.cfg", help="A SUMO configuration file [default: %default]", metavar="FILE")
    parser.add_option("-n", "--network", dest="network", default="Your.net.xml", help="A SUMO network definition file [default: %default]", metavar="FILE")    
    parser.add_option("-b", "--begin", dest="begin", type="int", default=800, action="store", help="The simulation time (s) at which the re-routing begins [default: %default]", metavar="BEGIN")
    parser.add_option("-a", "--additional-files", dest="additional", default="Your.add.xml", help="Generate edge-based dump instead of ""lane-based dump. This is the default.", metavar="FILE")
    parser.add_option("-a", "--additional-files", dest="additional", default="Your.add.xml", help="Generate edge-based dump instead of ""lane-based dump. This is the default.", metavar="FILE")
    parser.add_option("-e", "--edge-based-dump", dest="edge_based_dump", action="store_true", default="True", help="Generate edge-based dump instead of ""lane-based dump. This is the default.", metavar="FILE")
    parser.add_option("-e", "--end", dest="end", type="int", default=72000, action="store", help="The simulation time (s) at which the re-routing ends [default: %default]", metavar="END")
    parser.add_option("-i", "--interval", dest="interval", type="int", default=600, action="store", help="The interval (s) at which vehicles are re-routed [default: %default]", metavar="INTERVAL")
    parser.add_option("-o", "--output", dest="output", default="Your.xml", help="The XML file at which the output must be written [default: %default]", metavar="FILE")
    parser.add_option("-l", "--logfile", dest="logfile", default=os.path.join(tempfile.gettempdir(), "SUMO_ReFOCUS.log"), help="log messages to logfile [default: %default]", metavar="FILE")
    (options, args) = parser.parse_args()
    logging.basicConfig(filename=options.logfile, level=logging.DEBUG)
    logging.debug("Logging to %s" % options.logfile)
    if args:
        logging.warning("Superfluous command line arguments: \"%s\"" % " ".join(args))
    start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.output)
if __name__ == "__main__":
    main()    
    
 
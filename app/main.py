from app import App
import argparse
import configparser
import os



#Load and validate the config file
def load_config(config_file, required_conf):
    #Check if the config file exists - if not raised an error
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found")
    
    
    config = configparser.ConfigParser() #Create a config parser object
    config.read(config_file) #Read the config file

    #If the 'database' section in missing in the config file raise an error
    if 'database' not in config:
        raise ValueError("Missing 'database' section in the configuration file")
    

    #Check for missing configurations and raise an error if there is any missing conf
    missing_conf = [conf for conf in required_conf if conf not in config['database']]
    if len(missing_conf) > 0:
        raise ValueError(f"Missing required configurations: {', '.join(missing_conf)}")
    
    return config['database'] #Return the configuration

#Main func
def main():
    parser = argparse.ArgumentParser(description="Run the Flask server.") #Create a parser object to be able to get args
    parser.add_argument('conf_file', type=str, help='Configuration file path') #Add new arg to parse the conf file path 
    args = parser.parse_args() #Parse the args

    #Create a list of required configurations
    required_conf = [
        "host",
        "database",
        "port",
        "user",
        "password"
    ]
    
    #Load the config file
    app_config = load_config(args.conf_file,required_conf)
    
    #Start the Flask app
    web_app = App(app_config)
    web_app.run()

#Start the main function and avoid to run directly the loaded modules
if __name__ == "__main__":
    main()
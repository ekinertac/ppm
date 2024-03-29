A small tool managing python packages.

### Do not take this project seriously
it's just a `pip install` command with some features for personal needs.

#### Installation

    pip install pip-ppm

#### requirements.json file initialization
    
    ppm init
    
`ppm init` command creates a file contains:

    {
      "name": "test",
      "version": "1.0.0",
      "description": "",
      "author": "",
      "license": "ISC",
    }

#### Install a package and save to the requirements.json file
    
    ppm install flask --save
    ppm install flask==1 --save
    ppm install flask ipython --save


When you use `ppm install` command with `--save` flag, 
it's saving installed packages to the `requirements.json` file
    
    {   
        ...
        "requirements": {
	        "django": "2",
            "djangorestframework": ""
        }
    }


#### Install packages pre-defined in requirements.json file
    
    ppm install
    ...
    Successfully installed django-2.0 djangorestframework-3.10.3

#### Available commands
    
    Usage: ppm [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.
    
    Commands:
      init       Initializes requirements.json file
      install    Installs given package[s]
      uninstall  Uninstalls given package[s]
      dump       Dumps requirements.json file to `pip freeze` format


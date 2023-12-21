"""
Application package Build from Source post-installation script

:: Features
- Import configuration file
    - YAML
    - JSON
"""
import os
import sys
import json
import ruamel.yaml as ruamel_yaml

def display_header():
    print("build-from-source base installation manager")

def display_help():
    """
    Display Help options
    """
    # Initialize Variables
    msg = "Help:\n"

    for k,v in menu_Opts.items():
        # Get key and function description
        menu_key_Name = k
        menu_Description = v["summary"]

        # Append current message
        msg += "\t{} = {}\n".format(menu_key_Name, menu_Description)

    print(msg)

class Recipe():
    """
    Recipe configuration file handler class
    """
    def __init__(self, recipe_file="recipe.yaml"):
        self.recipe_file = recipe_file
        self.recipe_Skeleton = """
# Installation setup script definitions and recipe file
# 
# [Structure]
# - version: "[version-number]"
#
# - settings: Specify your system configuration settings/definitions here
#    - Type: List
#    - Sub-values:
#        - TBC
#
# - applications: Specify your application/package configuration and definitions here
#    - Type: List
#        - [application-name]: Specify the name of the application/package here
#            - Type: Dictionary
#            - Sub-key values:
#                - dependencies:   Place all dependencies and package requirements here
#                    - Type: List
#                - pre-requisites: Place all pre-requisites system shellscript commands here to execute
#                    - Type: List
#                - installation:   Place all installation system commands here to execute
#                    - Type: List

version: "version-number"

settings:
    ## Specify your system configuration settings/definitions here
    ## - Settings still in planning stages

applications:
    ## Specify your application/package configuration and definitions here
    application-name: # Specify the name of the application/package here
        dependencies:
            # Place all dependencies and package requirements here
            # - [package-dependencies-name]
        pre-requisites:
            # Place all pre-requisites system shellscript commands here to execute
            # - "command-executable {options} <arguments> ..."
        installation:
            # Place all installation system commands here to execute
            # - "command-executable {options} <arguments> ..."
"""
    def generate_Recipe(self, recipe_file="recipe.yaml"):
        """
        Generate and write a skeleton/template recipe file for editing

        :: Params
        - recipe_file : The target recipe file containing the instructions and settings for an application/project
            Type: String
            Default: recipe.yaml

        :: Output
        - error_Msg : The estimated error if recipe failed to import
            Type: String
        """
        # Initialize Variables
        error_Msg:str = ""

        # Check if file exists
        if os.path.isfile(recipe_file):
            # File exists
            error_Msg = "File exists"
        else:
            try:
                with open(recipe_file, "w+") as write_Recipe:
                    # Write recipe skeleton to file
                    write_Recipe.write(self.recipe_Skeleton)

                    # Close after usage
                    write_Recipe.close()
            except Exception as ex:
                error_Msg = str(ex)

        return error_Msg

    def import_Recipe(self, recipe_file="recipe.yaml") -> list:
        """
        Import the target application's recipe file into the system as a dictionary (Key-value) mapping

        :: Params
        - recipe_file : The target recipe file containing the instructions and settings for an application/project
            Type: String
            Default: recipe.yaml

        :: Output
        - recipe_Contents : The contents of the recipe file imported and mapped as a editable/readable dictionary object
            Type: Dictionary

        - error_Msg : The estimated error if recipe failed to import
            Type: String
        """
        # Initialize Variables
        recipe_Contents:dict = {}
        error_Msg:str = ""

        # Check if file exists
        if os.path.isfile(recipe_file):
            # File exists
            try:
                with open(recipe_file, "r") as read_Recipe:
                    # Try to import the recipe
                    yaml_Obj = yaml.load(read_Recipe)

                    for k,v in yaml_Obj.items():
                        # Check if there is value
                        if v != None:
                            # Check if type is CommentedMap
                            if type(v) == "ruamel.yaml.comments.CommentedMap":
                                # Convert CommentedMap object to Dictionary
                                recipe_Contents[k] = dict(v).copy()
                            else:
                                recipe_Contents[k] = v
                        else:
                            # None
                            recipe_Contents[k] = ""

                    # Close file after usage
                    read_Recipe.close()
            except Exception as ex:
                error_Msg = str(ex)
        else:
            error_Msg = "File does not exist"

        # Replace currently-opened contents with the newly-read content
        self.recipe_Contents = recipe_Contents

        return [recipe_Contents, error_Msg]

    def list_Recipe(self, recipe_Contents=None):
        """
        Display and list currently-imported recipe

        :: Params
        - recipe_Contents : The contents of the recipe file imported and mapped as a editable/readable dictionary object
            Type: Dictionary
        """
        # Initialize Variables
        k_old, v_old = "", ""
        k_new, v_new = "", ""

        # Check if recipe dictionary contains data
        if recipe_Contents != None:
            # Loop and list all key-values
            for k,v in recipe_Contents.items():
                print("{} = {}".format(k,v))
                # Check if value type is a list
                if isinstance(v,list):
                    while isinstance(v, list):
                        # Loop through and dig further down

                        # Set current depth/value to the previous key
                        v_new = v

                        for v in v_new:
                            print("\t{}".format(v))

                # Check if value type is a dictionary
                if isinstance(v, dict):
                    while isinstance(v, dict):
                        # Loop through and dig further down

                        # Set current depth/value to the previous key
                        v_new = v

                        for k,v in v_new.items():
                            print("\t{} = {}".format(k,v))

class MenuBuilder():
    """
    Menu option builder class
    """
    def __init__(self):
        """
        Class Constructor

        :: Params
        - menu_Opts : Dictionary (Key-Value) mappings of your menu options
            Type: Dictionary
            Format:
                "option-input-name" : {
                   "args" : ["-shortform", "--long-form"], # Contains the CLI option arguments; [0] = Short Form, [1] = Long Form
                   "summary" : "Description/summary of option", # Contains the description/summary of this option
                   "mapping" : ["function", "arguments"], # Contains the function containing the statements to execute for this option mapped to its arguments
                }
        """
        self.menu_Opts = {}

    def add_new_Opt(self, menu_opt_Name, menu_opt_Args=None, menu_opt_Summary="", menu_opt_Mappings=None):
        """
        New menu option keyword (name)

        :: Params
        - menu_opt_Name : Specify the keyword of the menu option
            Type: String

        - menu_opt_Args : Optional; List containing the elements [0] = short form and [1] = long form of the optional arguments
            Type: List

        - menu_opt_Summary : Optional; String containing a summary/description of what the option does
            Type: String

        - menu_opt_Mappings : Optional; List containing the elements [0] = The function to execute and [1] = The parameters to parse into the function
            Type: List
        """
        # Check if the option is in the Menu
        if not (menu_opt_Name in self.menu_Opts):
            self.menu_Opts[menu_opt_Name] = {"args" : [], "summary" : "", "mapping" : []}

        # Check if any of the settings are parsed
        if menu_opt_Args != None:
            self.map_opt_Args(menu_opt_Name, menu_opt_Args)

        if menu_opt_Summary != "":
            self.map_opt_Summary(menu_opt_Name, menu_opt_Summary)

        if menu_opt_Mappings != None:
            self.map_opt_Function(menu_opt_Name, menu_opt_Mappings)

    def map_opt_Args(self, menu_opt_Name, map_opt_Args=None):
        """
        Map menu option CLI arguments (long form and short form)
                   
        :: Params
        - menu_opt_Name : Specify the keyword of the menu option
            Type: String
        - menu_opt_Args : List containing the elements [0] = short form and [1] = long form of the optional arguments
            Type: List
            - short_form : The short form of the optional argument (i.e. '-s')
                - Type: String
            - long_form : The long form of the optional argument (i.e. '--long-form')
                - Type: String
        """
        # Check if the option is in the Menu
        self.add_new_Opt(menu_opt_Name)

        # Map function and argument mapping to the menu option
        self.menu_Opts[menu_opt_Name]["args"] = map_opt_Args

    def map_opt_Summary(self, menu_opt_Name, summary):
        """
        Map menu option's description/summary
                   
        :: Params
        - menu_opt_Name : Specify the keyword of the menu option
            Type: String
        - summary : Specify the summary/description of what this option does
            Type: String
        """
        # Check if the option is in the Menu
        self.add_new_Opt(menu_opt_Name)

        # Map function and argument mapping to the menu option
        self.menu_Opts[menu_opt_Name]["summary"] = summary

    def map_opt_Function(self, menu_opt_Name, map_opt_Function):
        """
        Map menu option to function and parameters

        :: Params
        - menu_opt_Name : Specify the keyword of the menu option
            Type: String

        - menu_opt_Function : List containing the elements [0] = The function to execute and [1] = The parameters to parse into the function
            Type: List
        """
        # Check if the option is in the Menu
        self.add_new_Opt(menu_opt_Name)

        # Map function and argument mapping to the menu option
        self.menu_Opts[menu_opt_Name]["mapping"] = map_opt_Function

    def open_Menu(self, user_input_Msg="Which option?: ", help_Func=None):
        """
        Create a menu to loop and process what application to run

        :: Params
        - user_input_Msg : Specify custom user input query message
            Type: String
            Default Value: "Which option?: "
        """
        # Initialize Variables
        menu_Opts = self.menu_Opts.copy()

        while True:
            if help_Func != None:
                # Print out menu
                help_Func()

            # Try to get user's input
            try:
                u_Option = input(user_input_Msg)

                # Get Key-value mappings
                opt_Values = menu_Opts[u_Option]
                opt_Arguments = opt_Values["args"]
                opt_Description = opt_Values["summary"]
                opt_Mappings = opt_Values["mapping"]

                if u_Option == "exit":
                    # Break condition
                    break
                else:
                    """
                    Process and check option mappings
                    """
                    # Get mapping command/function
                    opt_map_Func = opt_Mappings[0]

                    # Check number of elements
                    if len(opt_Mappings) == 1:
                        opt_map_Func()
                    elif len(opt_Mappings) > 1:
                        opt_map_Args = opt_Mappings[1:]

                        # Check if arguments are found
                        if opt_map_Args != None:
                            opt_map_Func(*opt_map_Args)
            except Exception as ex:
                print("Invalid option selection: [{}]".format(ex))

            # Print new line
            print("")

class Menu():
    """
    Custom Override Functions
    """
    def list_Recipe(self):
        # List currently-imported recipe settings
        print("")
        print("=======================================================")
        print("Print currently imported recipe configuration/settings:")
        print("=======================================================")
        recipe.list_Recipe(recipe_Contents)

    def display_Help(self):
        # Display help menu
        print("")
        print("================")
        print("Print Help Menu:")
        print("================")
        display_help()

    def reload_Recipe(self):
        # Reload/Reimport the recipe configuration file
        print("")
        print("================")
        print("Reloading recipe")
        print("================")
        recipe.import_Recipe(recipe.recipe_file)

    def generate_Recipe(self):
        ## Check if recipe is imported
        print("")
        print("=================")
        print("Generating recipe")
        print("=================")
        error_msg = recipe.generate_Recipe(recipe.recipe_file)
        if len(error_msg) > 0:
            print("Error generating recipe: {}".format(error_msg))

    def print_Menu(self):
        """
        Display full menu
        """
        print("")
        print("================")
        print("Print Full Menu:")
        print("================")
        for k,v in menu_Opts.items():
            # Get subkey-values
            curr_args = v["args"]
            curr_summary = v["summary"]
            curr_maps = v["mapping"]
            print("{}:".format(k))
            print("\tArguments : {}".format(curr_args))
            print("\tSummary   : {}".format(curr_summary))
            print("\tMappings  : {}".format(curr_maps))

def init():
    """
    Perform pre-initialization functions
    """
    global yaml, recipe, menu_Builder, menu_Opts

    # Initialize Classes
    yaml = ruamel_yaml.YAML()
    recipe = Recipe()
    menu_Builder = MenuBuilder()
    menu = Menu()

    # Build menu
    menu_Builder.add_new_Opt("exit", ["-e", "--exit"], "Exit/Quit the menu")
    menu_Builder.add_new_Opt("generate-recipe", ["-g", "--generate-recipe"], "Generate new recipe configuration/settings file", [menu.generate_Recipe])
    menu_Builder.add_new_Opt("help", ["-h", "--help"], "Display this help menu", [menu.display_Help])
    menu_Builder.add_new_Opt("list-recipe", ["-l", "--list-recipe"], "List currently-imported recipe settings", [menu.list_Recipe])
    menu_Builder.add_new_Opt("list-menu", ["--list-menu"], "List/print full menu", [menu.print_Menu])
    menu_Builder.add_new_Opt("reload", ["-r", "--reload"], "Reload/Reimport the recipe configuration file", [menu.reload_Recipe])

    # Global Variables
    menu_Opts = menu_Builder.menu_Opts.copy()

def setup():
    """
    Perform pre-requisite setup functions
    """
    # Global Variables
    global recipe_Contents

    # Initialize Local Variables
    recipe_fname = "recipe.yaml"

    # Import configuration files and recipe
    ## Import recipe contents
    recipe_Contents, error_Msg = recipe.import_Recipe(recipe_fname)

    ## Check if recipe is imported
    if len(recipe_Contents) <= 0:
        print("Error importing recipe {} : {}".format(recipe_fname, error_Msg))
        
        # Quit if issue encountered when importing recipe configuration
        exit(1)

def main():
    # Display opening header
    display_header()

    """
    Begin processing and main body operations
    """
    # Open Menu
    menu_Builder.open_Menu("Which option would you like to execute?: ", display_help)

if __name__ == "__main__":
    init()
    setup()
    main()


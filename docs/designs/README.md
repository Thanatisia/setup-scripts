# Application Setup CLI utility

## Information
### Summary
```
A 'Build-from-Source' Application/package Setup CLI utility designed to use a recipe file corresponding to a target application,
in which, contains specifications for how to build the project/applications according to the maintainer's rules.

The goal of this CLI utiltiy is to simplify and streamline the package management instructions into a "rulebook"/"playbook" which will be placed in a repository for easy retrieval.

The user just has to
    1. Retrieve the recipe file (default named 'recipe.yaml') from a repository
    2. Import into the package manager/source builder
    3. Execute the instructions accordingly
```

### Features and Functions for Setup Script
- Import YAML recipe/configuration file
- List/Print currently-imported recipe and application configurations
- Actions
    - setup   : Perform pre-requisite setup functions
    - `install {options} <arguments> [target]` : Begin installation of specified targets
        - Targets
            + app          : Begin installation of target application (Default)
            + dependencies : Install all dependencies only
    - `list {options} <arguments> [target]`  : List the specified target
        - Targets
            + dependencies : List all dependencies

## Setup
### Dependencies
### Pre-Requisites

## Documentations
### Synopsis/Syntax
```console
setup-script-name {global-options} <global-arguments> [actions {local-options} <local-arguments> ...]
```
### Parameters
#### Positionals
- Actions
    - setup   : Perform pre-requisite setup functions
    - import  : Import the specified configuration file name (Default: recipe.yaml)
    - `install {options} <arguments> [target]` : Begin installation of specified targets
        - Targets
            + app          : Begin installation of target application (Default)
            + dependencies : Install all dependencies only
    - `list {options} <arguments> [target]`  : List the specified target
        - Targets
            + all          : List all information
            + dependencies : List all dependencies

#### Optionals
- With Arguments
    + `-c | --configuration-file [custom-system-config-file]` : Specify custom configuration file name
    + `-i | --import-recipe [custom-application-recipe]`      : Specify custom application recipe to import
- Flags
    + -h | --help : Display help message

### Usage
- Default installation with custom recipe
    ```console
    setup-script-name -i custom-recipe.yaml import setup install
    ```

- List currently-specific recipe information
    ```console
    setup-script-name list dependencies
    ```

## Resources

## References

## Remarks


#!/bin/env bash
: "
Script for setting up tmux basic configurations
"

# Initialize Variables
CFG_FOLDER=~/.tmux
CFG_FILE=~/.tmux.conf

: "
General Utilities
"
display_help()
{
    : "
    Display help menu
    "
    help_msg="$(cat <<EOF
# Help Menu

## Setup

### Pre-Requisites

### Dependencies
+ tmux
+ git : For tpm

## Documentations

### Synopsis/Syntax
./setup.sh {options} 

### Parameters
- Positionals
- Optionals
    + -a | --all : Run all setup
    + -h | --help : Display this help menu with detailed usage
    + -r | --reload-tmux : Reload tmux configuration file
    + --my-recommendations : Setup according to my recommendations
    + --tmux-config : Setup tmux configuration file
    + --tpm : Setup Tmux plugin manager

### Usage
EOF
)"
    echo -e "$help_msg"
}

create_folders()
{
    : "
    Dynamically create all folders specified.
    "
    folders=("$@")
    num_of_Folders="${#folders[@]}"

    ## Loop through all folders
    for i in ${!folders[@]}; do
        # Get current folder
        curr_folder="${folders[$i]}"

        if [[ ! -d "$curr_folder" ]]; then
            # Folder doesnt exist
            mkdir -p "$curr_folder" && \
                echo -e "Folder [$curr_folder] has been created successfully." || \
                echo -e "Error creating folder [$curr_folder]."
        else
            echo -e "Folder [$curr_folder] already exists."
        fi
    done
}

create_files()
{
    : "
    Dynamically create all files specified.
    "
    files=("$@")
    num_of_Files="${#files[@]}"

    ## Loop through all files
    for i in ${!files[@]}; do
        # Get current file
        curr_file="${files[$i]}"

        if [[ ! -f "$curr_file" ]]; then
            # File doesnt exist
            touch $curr_file && \
                echo -e "File [$curr_file] has been created successfully." || \
                echo -e "Error creating file [$curr_file]."
        else
            echo -e "File [$curr_file] already exists."
        fi
    done
}

: "
Setup Functions
"
setup_recommendations()
{
    : "
    Setup according to my recommendations

    :: Place your custom recommendation steps here
    "
    # Initialize Variables
    CFG_FOLDER=~/config/tmux

    ## Begin
    setup_tmux_config # Setup default tmux configuration
    
    create_folders "$CFG_FOLDER"

    setup_tpm # Setup Tmux package manager
}

setup_tmux_config()
{
    : "
    Setup Tmux configuration file
    "
    # Check if tmux default configuration file exists
    create_files "$CFG_FILE"
    create_folders "$CFG_FOLDER"
}

setup_tpm()
{
    : " 
    Setup Tmux Plugin Manager (TPM)

    URL: https://github.com/tmux-plugins/tpm
    "
    REPO_URL="https://github.com/tmux-plugins/tpm"
    DST_FOLDER=~/.tmux/plugins/tpm

    ## Check if repository exists in destination
    if [[ ! -d "$DST_FOLDER" ]]; then
        # Folder doesnt exist
        ## Clone repository URL to configuration folder
        git clone $REPO_URL $DST_FOLDER
    fi

    ## Append TPM into tmux configuration file (~/.tmux.conf | $XDG_CONFIG_HOME/tmux/tmux.conf)
    tpm_str=$(cat <<EOF
# List of plugins
## Place your plugins here 
## GitHub : set -g @plugin 'github_username/plugin-name'
## Other git repository hub : set -g @plugin 'git@repository_URL:username/plugin-name'
set -g @plugin 'tmux-plugins/tpm'

# Initialize TMUX plugin manager (keep this line at the very bottom of .tmux.conf)
run '~/.tmux/plugins/tpm/tpm'
EOF
)
    echo -e "$tpm_str" | tee -a ~/.tmux.conf

    # Completed
    echo -e "\n\tPlease press '[Prefix] + I (capital i) to install all new plugins specified in the configuration file. The plugins will be cloned to ~/.tmux/plugins and sourced\n"
}

reload_tmux()
{
    : "
    Reload tmux configuration file from within
    "
    tmux source $CFG_FILE
}

main()
{
    argv=("$@")
    argc="${#argv[@]}"

    if [[ "$argc" -gt 0 ]]; then
        while [[ "$1" != "" ]]; do
            case "$1" in
                "-a" | "--all")
                    # Run all setup
                    setup_tmux_config
                    setup_tpm
                    reload_tmux
                    shift 1
                    ;;
                "-h" | "--help")
                    # Display help
                    display_help
                    shift 1
                    ;;
                "-r" | "--reload-tmux")
                    # Reload tmux configuration file
                    reload_tmux
                    shift 1
                    ;;
                "--tmux-config")
                    # Setup tmux configuration file
                    setup_tmux_config
                    shift 1
                    ;;
                "--tpm")
                    # Setup tmux plugin manager
                    setup_tpm
                    shift 1
                    ;;
                *)
                    # Invalid options
                    echo -e "Invalid Option : $1"
                    shift 1
                    ;;
            esac
        done
    else
        echo -e "No arguments provided."
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi



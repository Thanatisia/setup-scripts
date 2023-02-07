#!/bin/env bash
: "
sxhkd preparation and setup script

Target Base System: ArchLinux 
"

# Configuration Files Info
declare -A DEFAULT_CONF=(
    # Default configuration file locations
    # [filename]="/default/path/to/config/file(s)"
    ["sxhkdrc"]="/usr/local/share/doc/bspwm/examples/"
)
declare -A CONFIG_DIR=(
    # Configuration file directory location
    # [filename]="/default/path/to/custom/configs"
    ["sxhkdrc"]=~/.config/sxhkd/
)
declare -A CONFIG_FILES=(
    # Configuration file names
    # [filename]="config file name"
    ["sxhkdrc"]="sxhkdrc"
)
declare -A FILE_CONTENTS=(
    # File contents to write
    # [filepath/name]="contents"
)

# Package Information
PKG_AUTHOR="baskerville"
PKG_NAME="sxhkd"
SRC_URL="https://github.com/$PKG_AUTHOR/$PKG_NAME"

# Functions
prepare()
{
    : "
    Prepare all files and folders required to setup
    "
    # Make configuration directories
    for cfg_filename in "${!CONFIG_DIR[@]}"; do
        # Get directory to create
        home_dirname=${CONFIG_DIR[$cfg_filename]}

        # Check if directory exists
        if [[ ! -d "$home_dirname" ]]; then
            # Directory does not exist
            # Create directory
            mkdir -p "$home_dirname" && \
                echo -e "[+] Directory '$home_dirname' has been created" || \
                echo -e "[-] Error creating directory '$home_dirname'"
        else
            # Directory exists
            echo -e "[+] Directory '$home_dirname' already exists"
        fi
    done
}

setup()
{
    : "
    Begin setup of application and installation of configurations
    "
    # Copy files from default configuration file into custom home configuration file
    for conf_file in "${!DEFAULT_CONF[@]}"; do
        # Get default configuration path
        default_conf_dir="${DEFAULT_CONF[$conf_file]}"

        # Get target home directory for the file
        target_home_dir="${CONFIG_DIR[$conf_file]}"

        # Check if target file exists
        if [[ -f "$default_conf_dir/$conf_file" ]]; then
            # File does not exists
            # Copy configuration file from default path to target home config directory
            cp "$default_conf_dir/$conf_file" "$target_home_dir" && \
                echo -e "[+] Target file $conf_file has been copied to '$target_home_dir' successfully." || \
                echo -e "[-] Error copying Target file $conf_file to '$target_home_dir'"

            # Change permission of configuration file to executable
            chmod u+x "$target_home_dir/$conf_file" && \
                echo -e "[+] Permission of $target_home_dir/$conf_file has been set to 'user + executable'" || \
                echo -e "[-] Error setting permission of $target_home_dir/$conf_file to 'user + executable'"
        else
            echo -e "Target file $default_conf_dir/$conf_file does not exists."
        fi
    done

    # Append file contents into the files
    for file_names in "${!FILE_CONTENTS[@]}"; do
        file_msg="${FILE_CONTENTS[$file_names]}"

        if [[ "$file_msg" != "" ]]; then
            echo -e "Writing message [$file_msg] >> File [$file_names]"
            echo -e "$file_msg" > "$file_names"
        fi
    done
}

clean()
{
    : "
    Uninstall and revert back to pre-installation settings by
    removing applied global configuration settings
    "
}

main()
{
    prepare
    setup

    # clean && \
    #    echo -e "[+] Cleanup Successful." || \
    #    echo -e "[-] Cleanup Error."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

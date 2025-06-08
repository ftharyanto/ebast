#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project root directory
cd "$SCRIPT_DIR" || exit 1

# Conda environment name
CONDA_ENV="django"
# Path to conda.sh - update this if conda is installed in a different location
CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"

# Path to the manage.py file
MANAGE_PY="$SCRIPT_DIR/manage.py"

# Create a temporary crontab file
CRON_TEMP=$(mktemp)

# Add the current crontab to the temp file
crontab -l > "$CRON_TEMP" 2>/dev/null || true

# Add our new cron job (runs daily at 3 AM)
CRON_JOB="0 3 * * * . $CONDA_SH && conda activate $CONDA_ENV && cd $SCRIPT_DIR && python $MANAGE_PY delete_expired_papan_klip_records"

# Check if the cron job already exists
if ! grep -Fxq "$CRON_JOB" "$CRON_TEMP"; then
    echo "Adding cron job..."
    echo "# Clean up expired Papan Klip entries" >> "$CRON_TEMP"
    echo "$CRON_JOB" >> "$CRON_TEMP"
    
    # Install the new crontab
    crontab "$CRON_TEMP"
    echo "Cron job has been installed successfully!"
    echo "The following job has been added:"
    echo "$CRON_JOB"
else
    echo "Cron job already exists. No changes were made."
fi

# Clean up
rm -f "$CRON_TEMP"

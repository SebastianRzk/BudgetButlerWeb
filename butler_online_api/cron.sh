#!/bin/bash

# Start the run once job.
echo "BudgetButlerWeb Cron container has been started";

# Setup a cron schedule
echo "
5 0 * * * /app/cron
# This extra line makes it a valid cron" > scheduler.txt;

echo "initial checkout"
./cron
echo "checkup finished"

crontab scheduler.txt;
cron -f;


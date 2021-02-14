#!/usr/bin/env bash
export GITHUB_TOKEN=    
export FRESHDESK_TOKEN=
python3 -m api_transfer --gh_user vanpelt --fd_subdomain
echo DONE
read -p "Press Enter to complete" </dev/tty


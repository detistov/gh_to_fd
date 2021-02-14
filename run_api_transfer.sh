#!/usr/bin/env bash
export export GITHUB_TOKEN=    
export FRESHDESK_TOKEN=
python3 -m api_transfer --gh_user vanpelt --fd_subdomain newaccount1613193603063
echo DONE
read -p "Press Enter to complete" </dev/tty


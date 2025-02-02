#ORDER
SPACESHIP_PROMPT_ORDER=(
    venv
    time           # Time stamps section
    user           # Username section
    dir            # Current directory section
    host           # Hostname section
    git            # Git section (git_branch + git_status)
    node           # Node.js section
    python         # Python section
    docker         # Docker section
    docker_compose # Docker section
    exec_time      # Execution time
    async          # Async jobs indicator
    line_sep       # Line break
    exit_code      # Exit code section
    sudo           # Sudo indicator
    char           # Prompt character
)

#ERROR
SPACESHIP_ASYNC_SYMBOL='' # Solve permanatly dispalyed tree dots at the end of command prompt

SPACESHIP_PROMPT_FIRST_PREFIX_SHOW=true
SPACESHIP_PROMPT_DEFAULT_PREFIX=''
SPACESHIP_PROMPT_DEFAULT_SUFFIX=' '

#USER
SPACESHIP_USER_SHOW='false'

#DIR
SPACESHIP_DIR_PREFIX=''
SPACESHIP_DIR_TRUNC=0
SPACESHIP_DIR_TRUNC_PREFIX='../'

SPACESHIP_PROMPT_ASYNC=false

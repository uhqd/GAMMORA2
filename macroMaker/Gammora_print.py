def _gammora_ascii():

    #print("######      ###    ##     ## ##     ##  #######  ########     ###")
    #print("##    ##    ## ##   ###   ### ###   ### ##     ## ##     ##   ## ##")  
    #print("##         ##   ##  #### #### #### #### ##     ## ##     ##  ##   ##") 
    #print("##   #### ##     ## ## ### ## ## ### ## ##     ## ########  ##     ##")
    #print("##    ##  ######### ##     ## ##     ## ##     ## ##   ##   #########")
    #print("##    ##  ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##")
    #print(" ######   ##     ## ##     ## ##     ##  #######  ##     ## ##     ##")

    print("             ███████  ███████ ███    ███ ███    ███  ██████  ██████  ███████")
    print("             ██       ██   ██ ████  ████ ████  ████ ██    ██ ██   ██ ██   ██")
    print("             ██   ███ ███████ ██ ████ ██ ██ ████ ██ ██    ██ ██████  ███████")
    print("             ██    ██ ██   ██ ██  ██  ██ ██  ██  ██ ██    ██ ██   ██ ██   ██")
    print("              ██████  ██   ██ ██      ██ ██      ██  ██████  ██   ██ ██   ██")

def _title(string):
    print()
    print("* "+ string)
    print()

def _title2(string):
    print("     * "+ string)

def _separator1():
    print()
    print("===============================================================================")
    print()

def _separator2():
    print()
    print("------------------------------------------------------")
    print()

def _error_config(setting, user_setting, correction):
    print()
    print()
    print("     !!! ERROR !!!")
    print("      * "+ setting)
    print("         -> "+ user_setting +" is not allowed")
    print("         -> Please Check your Config File.")
    print("         -> Options are :")
    for option in correction:
        print("             - "+option)
    print()
    print()

def _warning(setting, correction):
    print()
    print("*** !  WARNING  !  : "+setting+' ***')
    for option in correction:
        print("             -> "+option)
    print()

def _error_config_file_not_found(user_file):
    print()
    print("     !!! ERROR !!!")
    print("      * "+ user_file +" not found")
    print("         -> Please check config file")
    print()

def _display_working_state(a):
        print("         "+a+" ...", end= "\r", flush=True)

def _error(user_entry, correction):
    print()
    print()
    print("     !!! ERROR !!!")
    print("      * "+ user_entry)
    for option in correction:
        print("     -> "+option)
    print()
    print()
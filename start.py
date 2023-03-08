import os
import subprocess
import time
import atexit


# Funktionen som kommer att köras när programmet avslutas
def cleanup():
    p.terminate()
    telemat_p.terminate()

# Hämta sökvägen till den aktuella katalogen
script_dir = os.path.dirname(os.path.realpath(__file__))

# Konstruera den absoluta sökvägen till telemat.py
telemat_script_path = os.path.join(script_dir, "telemat.py")

# Starta telemat.py
print("Startar telemat.py...")
telemat_p = subprocess.Popen(['python', telemat_script_path])

# Registrera cleanup() som en funktion att köras när programmet avslutas
atexit.register(cleanup)

while True:
    # Hämta sökvägen till den aktuella katalogen
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Konstruera den absoluta sökvägen till compare.py
    send_script_path = os.path.join(script_dir, "compare.py")

    # Starta compare.py
    print("Startar compare.py...")
    p = subprocess.Popen(['python', send_script_path])

    # Vänta
    print("Väntar i 1 minut...")
    time.sleep(30)

    # Avsluta compare.py
    print("Avslutar compare.py...")
    p.terminate()

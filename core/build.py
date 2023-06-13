import os
import subprocess
from sys import argv;

# Compiler options
CC = "gcc"
CFLAGS = "-Wall -Icore/include"

# List of source files
SRCS = ["./src/main.c", "./src/lib/cJSON.c", "./src/service/database_server.c", "./src/utils/event_bus.c"]

# Generate object file names from source files
OBJS = [os.path.join("build", os.path.splitext(os.path.basename(src))[0] + ".o") for src in SRCS]

# Name of the final executable
TARGET = os.path.join("build", "main.exe")

def compile_source(src):
    obj = os.path.join("build", os.path.splitext(os.path.basename(src))[0] + ".o")
    cmd = f"{CC} {CFLAGS} -c {src} -o {obj}"
    subprocess.run(cmd, shell=True, check=True)

def build_target():
    objs = " ".join(OBJS)
    cmd = f"{CC} {objs} -o {TARGET}"
    subprocess.run(cmd, shell=True, check=True)

def clean():
    clean_o()
    if os.path.exists(TARGET):
        os.remove(TARGET)

def clean_o():
    for obj in OBJS:
        if os.path.exists(obj):
            os.remove(obj)

def build():
    try:
        # Compile source files
        for src in SRCS:
            compile_source(src)
        
        # Build the target
        build_target()
        clean_o()
        print(f"Build successful! Executable '{TARGET}' created.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during build: {e}")
        clean()

    except KeyboardInterrupt:
        print("Build process interrupted.")
        clean()

if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == "clean":
            clean()
            print("Clean successful!")
        elif argv[1] == "build":
            build()
        else:
            print("Invalid argument")
    else:
        print("Need argument")
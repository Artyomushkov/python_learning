#!/usr/bin/env python3.11

"""Module for displaying system info"""

import argparse
import subprocess
import os

def pipe_execute(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.communicate()[0].decode("utf-8")

def show_distribution_info():
    output = pipe_execute("cat /etc/os-release | grep 'PRETTY_NAME'")
    print("-----Distribution-----") 
    print(output[output.find('=') + 2:len(output) - 2])

def show_memory_info():
    mem_info = subprocess.check_output(["cat", "/proc/meminfo"]).decode("utf-8")
    begin_str = 0
    print("-----Memory-----")
    for i in range(3):
        end_str = mem_info.find('\n', begin_str)
        print(mem_info[begin_str : end_str])
        begin_str = end_str  + 1

def show_cpu_info():
    output = pipe_execute("cat /proc/cpuinfo | grep -E 'model name|cpu cores|cpu MHz'")
    print("-----CPU-----")
    print(output[:len(output) - 1])

def show_user():
    print("-----User-----")
    print(os.getenv("USER"))

def show_load_average():
    output = subprocess.check_output(["uptime"]).decode("utf-8")
    print("-----Load average-----")
    begin_index = output.find('load') + len("load aveage: ")
    print(output[begin_index : len(output) - 1])

def show_ip_addr():
    output = pipe_execute("hostname -I | awk '{print $1}'")
    print("-----IP address-----")
    print(output[:len(output) - 1])

parser = argparse.ArgumentParser()
parser.add_argument('-d', action='store_true', help="show distribution info")
parser.add_argument('-m', action='store_true', help="show information about memory")
parser.add_argument('-c', action='store_true', help="show CPU info")
parser.add_argument('-u', action='store_true', help="show current user")
parser.add_argument('-l', action='store_true', help="show load average")
parser.add_argument('-i', action='store_true', help="show IP address")

args = parser.parse_args()

if args.d:
    show_distribution_info()
if args.m:
    show_memory_info()
if args.c:
    show_cpu_info()
if args.u:
    show_user()
if args.l:
    show_load_average()
if args.i:
    show_ip_addr()

# coding=utf-8
# svn checkout & replace

import os
import re
import shutil
import subprocess

FLAG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/ver.txt'
POST_DIR = os.path.dirname(os.path.abspath(__file__)) + '/_posts'


def get_local_ver():
    if os.path.isfile(FLAG_FILE):
        rf = open(FLAG_FILE, 'r')
        line = rf.readline()
        if len(line) > 0:
            return int(line)
    return 0


def set_local_ver(ver):
    if os.path.isfile(FLAG_FILE):
        os.remove(FLAG_FILE)
    wf = open(FLAG_FILE, 'w')
    wf.write(str(ver))
    wf.close()


def get_svn_latest_version():
    svn_logs = subprocess.Popen("svn info \"svn://git.oschina.net/kylescript/myblog/_posts\"",
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE, shell=True).communicate()[0]
    logs = re.compile('Last Changed Rev: ([\d]+)').findall(svn_logs)
    if isinstance(logs, list):
        if len(logs) > 0:
            return int(logs[0])
    return 0


def svn_checkout():
    # clean tmp dir
    if os.path.isdir(POST_DIR):
        shutil.rmtree(POST_DIR)

    # check out
    subprocess.Popen("svn co \"svn://git.oschina.net/kylescript/myblog/_posts\" " + POST_DIR,
                     stderr=subprocess.STDOUT,
                     stdout=subprocess.PIPE, shell=True).communicate()


def main():
    latest_ver = get_svn_latest_version()
    local_ver = get_local_ver()
    if latest_ver > local_ver:
        svn_checkout()
        set_local_ver(latest_ver)

main()

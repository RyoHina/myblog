# coding=utf-8
# svn checkout & replace

import os
import re
import shutil
import subprocess


def get_local_ver():
    if os.path.isfile("ver.txt"):
        rf = open("ver.txt", 'r')
        line = rf.readline()
        if len(line) > 0:
            return int(line)
    return 0


def set_local_ver(ver):
    if os.path.isfile("ver.txt"):
        os.remove("ver.txt")
    wf = open("ver.txt", 'w')
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


def get_abspath():
    return os.path.dirname(os.path.abspath(__file__))


def svn_checkout():
    # clean tmp dir
    if os.path.isdir(get_abspath() + '/_posts'):
        shutil.rmtree(get_abspath() + '/_posts')

    # check out
    subprocess.Popen("svn co \"svn://git.oschina.net/kylescript/myblog/_posts\" " + get_abspath() + '/_posts',
                     stderr=subprocess.STDOUT,
                     stdout=subprocess.PIPE, shell=True).communicate()


def main():
    latest_ver = get_svn_latest_version()
    local_ver = get_local_ver()
    if latest_ver > local_ver:
        svn_checkout()
        set_local_ver(latest_ver)

main()

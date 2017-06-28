---
layout: post
title: "shadowsocks global proxy for ubuntu desktop"
categories: shadowsocks
tags: shadowsocks-client ubuntu
---

* content
{:toc}
1. install shadowsocks-qt5
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5

2. install genpac
sudo pip install genpac  # donot lose 'sudo'

3. make pac file
sudo wget "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
sudo genpac -p "SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" --output="autoproxy.pac" --gfwlist-local=/home/ss/gfwlist.txt  #replace with your gfwlist.txt path

4. system setting
Open System Setting->Network->Network proxy
M: auto
URL(c):file:///home/ss/autoproxy.pac # replace with your autoproxy.pac file.

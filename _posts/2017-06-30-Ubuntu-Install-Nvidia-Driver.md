---
layout: post
title: "Ubuntu Install Nvidia Driver"
categories: ubuntu
tags: ubuntu-nvidia
---

* content
{:toc}

	
Ubuntu Install Nvidia Driver

For Ubuntu 12.04

	sudo add-apt-repository ppa:bumblebee/stable
	sudo apt-get update
	sudo apt-get install bumblebee bumblebee-nvidia virtualgl linux-headers-generic
	sudo reboot

For Ubuntu 14.04 and later

	sudo apt-get install bumblebee bumblebee-nvidia primus linux-headers-generic
	sudo reboot

https://wiki.ubuntu.com/Bumblebee#Installation


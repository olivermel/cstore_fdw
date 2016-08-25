# Defines our Vagrant environment
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

 # create cstore node (change this to new project)

  config.vm.define :cstore do |cstore_config|
      cstore_config.vm.box = "bento/centos-6.7"
      cstore_config.vm.hostname = "cstore"
      cstore_config.vm.network :private_network, ip: "192.168.0.8"
      cstore_config.vm.provider "virtualbox" do |vb|
      cstore_config.ssh.forward_agent = true
      cstore_config.ssh.forward_x11 = true
      end 
      cstore_config.vm.provision :shell, path: "bootstrap.sh", privileged: false
  end 

end

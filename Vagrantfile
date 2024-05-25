# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "webhook-to-fedora-messaging" do |webhook-to-fedora-messaging|
    webhook-to-fedora-messaging.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/40/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-libvirt.x86_64-40-1.14.vagrant.libvirt.box"
    webhook-to-fedora-messaging.vm.box = "f38-cloud-libvirt"
    webhook-to-fedora-messaging.vm.hostname = "webhook-to-fedora-messaging.tinystage.test"

    webhook-to-fedora-messaging.vm.synced_folder '.', '/vagrant', disabled: true
    webhook-to-fedora-messaging.vm.synced_folder ".", "/home/vagrant/webhook-to-fedora-messaging", type: "sshfs"


    webhook-to-fedora-messaging.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    webhook-to-fedora-messaging.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/playbook.yml"
      ansible.config_file = "devel/ansible/ansible.cfg"
      ansible.verbose = true
    end
  end
end

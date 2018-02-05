# Vagrantfile to build a box with the required software for this library.

$script = <<SCRIPT
echo I am provisioning...
sudo apt-get update
sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo pip3 install nose
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password vagrant'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password vagrant'
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
sudo apt install python3-mysqldb
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.provision "shell", inline: $script
end

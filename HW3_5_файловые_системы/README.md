<h1>Домашнее задание 3.4. Операционные системы, лекция 2 - Петр Иванов</h1>

<h3>1. Узнайте о sparse (разряженных) файлах.</h3>

	Почитал. Это похоже на RLE. Современные FS могут и в потоковый ZIP. 
	Прикольно, что sparse есть на NTFS оказывается. То, что я о нём за 20 лет работы 
	ни разу не слышал, показывает на сколько это всё нужно.  
	
<h3>2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?</h3>

	Вопрос задан некорректно. Объект = файл. У него всё хранится в i-node, в том числе и доступ. Ссылок на него может быть несколько, 
	но поскольку они ведут в одно место, то разрешения там одинаковые. Это касается и аттрибутов файла. 

<h3>3. Сделайте vagrant destroy на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

	Vagrant.configure("2") do |config|
	  config.vm.box = "bento/ubuntu-20.04"
	  config.vm.provider :virtualbox do |vb|
		lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
		lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
		vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
		vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
		vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
		vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
	  end
	end
</h3>	

Зачем же удалять. Можно просто в соседней директории всё сделать. Done. 

<h3>4. Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.</h3>

	vagrant@vagrant:~$ sudo -i
	root@vagrant:~# fdisk -l
	Disk /dev/sda: 64 GiB, 68719476736 bytes, 134217728 sectors
	Disk model: VBOX HARDDISK
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0x3f94c461

	Device     Boot   Start       End   Sectors  Size Id Type
	/dev/sda1  *       2048   1050623   1048576  512M  b W95 FAT32
	/dev/sda2       1052670 134215679 133163010 63.5G  5 Extended
	/dev/sda5       1052672 134215679 133163008 63.5G 8e Linux LVM


	Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
	Disk model: VBOX HARDDISK
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes


	Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
	Disk model: VBOX HARDDISK
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes


	Disk /dev/mapper/vgvagrant-root: 62.55 GiB, 67150807040 bytes, 131153920 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes


	Disk /dev/mapper/vgvagrant-swap_1: 980 MiB, 1027604480 bytes, 2007040 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	


	fdisk /dev/sdb #(n,p [1,2], ..., w)
	
	Получилось так:
	
	Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
	Disk model: VBOX HARDDISK
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disklabel type: dos
	Disk identifier: 0xc5dd1ed4

	Device     Boot   Start     End Sectors  Size Id Type
	/dev/sdb1          2048 3907583 3905536  1.9G 83 Linux
	/dev/sdb2       3907584 5242879 1335296  652M 83 Linux
	

<h3>5. Используя sfdisk, перенесите данную таблицу разделов на второй диск.</h3>

	root@vagrant:~## sfdisk -d /dev/sdb | sfdisk /dev/sdc
	
	Device     Boot   Start     End Sectors  Size Id Type
	/dev/sdc1          2048 3907583 3905536  1.9G 83 Linux
	/dev/sdc2       3907584 5242879 1335296  652M 83 Linux

<h3>6. Соберите mdadm RAID1 на паре разделов 2 Гб.</h3>

	root@vagrant:~## mdadm --create --verbose /dev/md/test_raid1 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

<h3>7. Соберите mdadm RAID0 на второй паре маленьких разделов.</h3>

	root@vagrant:~## mdadm --create --verbose /dev/md/test_raid0 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
	
	root@vagrant:~## cat /proc/mdstat
	Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]
	md126 : active raid0 sdc2[1] sdb2[0]
		  1331200 blocks super 1.2 512k chunks

	md127 : active raid1 sdc1[1] sdb1[0]
		  1950720 blocks super 1.2 [2/2] [UU]
	
<h3>8. Создайте 2 независимых PV на получившихся md-устройствах.</h3>

	root@vagrant:~# pvcreate /dev/md126 /dev/md127
	  Physical volume "/dev/md126" successfully created.
	  Physical volume "/dev/md127" successfully created.

	проверяем
	root@vagrant:~# pvs
	  PV         VG        Fmt  Attr PSize   PFree
	  /dev/md126           lvm2 ---   <1.27g <1.27g
	  /dev/md127           lvm2 ---    1.86g  1.86g
	  /dev/sda5  vgvagrant lvm2 a--  <63.50g     0
	  
<h3>9. Создайте общую volume-group на этих двух PV.</h3>
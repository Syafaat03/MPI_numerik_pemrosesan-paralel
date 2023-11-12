# MPI-Numeric

## Running Numeric Python with MPI Multinode Cluster on Ubuntu Desktop

This guide outlines the steps to create a master and slave, configure SSH, configure NFS, install MPI, and the related steps to run numeric code on Ubuntu Desktop.

## Table of Contents
- [Devices and Tools to Prepare](#devices-and-tools-to-prepare)
- [Bridged Topology](#bridged-topology)
- [Creating Master and Slave](#creating-master-and-slave)
- [SSH Configuration](#ssh-configuration)
- [NFS Configuration](#nfs-configuration)
- [MPI Installation](#mpi-installation)
- [Running Python Code](#running-python-code)

## Devices and Tools to Prepare
- Ubuntu Desktop
  - Ubuntu Desktop Master
  - Ubuntu Desktop Slave 1
  - Ubuntu Desktop Slave 2
  - Ubuntu Desktop Slave 3
- MPI (Master and Slave)
- SSH (Master and Slave)
- NFS (Master and Slave)
- Python Numeric Code

## Bridged Topology
![Topologi Numerik](https://github.com/Syafaat03/laporan_numerik_pemrosesan-paralel/blob/b85a2a661c5f41c3cd04c1f20f2e94c49a0aa4a8/Topologi%20Numerik.png)

## Creating Master and Slave
1. Ensure each master and slave uses a Network Bridge Adapter and is connected to the internet.
2. Determine which device will be the master, slave1, slave2, and slave3.
3. Create a new user on the master and each slave:
    ```bash
    sudo adduser mpiuser
    ```
4. Grant root access with the command:
    ```bash
    sudo usermod -aG sudo mpiuser
    ```
    Repeat the above steps for each slave.
5. Log in to each server with the user `mpiuser`:
    ```bash
    su - mpiuser
    ```
6. Update Ubuntu Desktop and install tools:
    ```bash
    sudo apt update && sudo apt upgrade
    sudo apt install net-tools vim
    ```
7. Configure the `/etc/hosts` file on the master, slave1, slave2, and slave3. Register the IP and hostname of each computer.

## SSH Configuration
1. Install OpenSSH on the master and all slaves:
    ```bash
    sudo apt install openssh-server
    ```
2. Generate a key on the master:
    ```bash
    ssh-keygen -t rsa
    ```
3. Copy the public key to each slave using the following command in the `.ssh` directory:
    ```bash
    cd .ssh
    cat id_rsa.pub | ssh mpiuser@slave1 "mkdir .ssh; cat >> .ssh/authorized_keys"
    ```
    Repeat the command for each slave.

## NFS Configuration
1. Create a shared folder on the master and each slave:
    ```bash
    mkdir numeric
    ```
2. Install NFS on the master:
    ```bash
    sudo apt install nfs-kernel-server
    ```
3. Configure the `/etc/exports` file on the master. Add the following line at the end of the file:
    ```plaintext
    /home/mpiuser/numeric *(rw,sync,no_root_squash,no_subtree_check)
    ```
    The Shared Folder location is the directory where the numeric file was created above.
4. Restart NFS Server:
    ```bash
    sudo exportfs -a
    sudo systemctl restart nfs-kernel-server
    ```
5. Install NFS on each slave:
    ```bash
    sudo apt install nfs-common
    ```
6. Mount the shared folder from the master to each slave:
    ```bash
    sudo mount master:/home/mpiuser/numeric /home/mpiuser/numeric
    ```
    Repeat the command for each slave.

## MPI Installation
1. Install Open MPI on the master and all slaves:
    ```bash
    sudo apt install openmpi-bin libopenmpi-dev
    ```
2. Install the MPI library via pip:
    ```bash
    sudo apt install python3-pip
    pip install mpi4py
    ```
3. Install Numpy on the master and each slave:
    ```bash
    pip3 install numpy
    ```

## Running Python Code
1. Create a new Python file:
    ```bash
    touch /home/mpiuser/numeric/num.py
    ```
2. Navigate to that directory and edit the Python file:
    ```bash
    cd /home/mpiuser/numeric
    nano num.py
    ```
    Then create the Python Numric code. Save by pressing `CTRL + X` and then press `Y`.
   [num.py code](https://github.com/Syafaat03/laporan_numerik_pemrosesan-paralel/blob/b85a2a661c5f41c3cd04c1f20f2e94c49a0aa4a8/num.py)
4. Run the Python code with MPI:
    ```bash
    mpirun -np 3 -hosts master,slave1,slave2 python3 num.py
    ```
   ![py mpi tets](https://github.com/Syafaat03/laporan_numerik_pemrosesan-paralel/blob/b85a2a661c5f41c3cd04c1f20f2e94c49a0aa4a8/py%20mpi%20tets.png)
   The execution result will be displayed with the measured runtime.

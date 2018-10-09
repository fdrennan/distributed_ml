import configparser

def CreateUserData():
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    USERNAME = BUCKET_NAME = config['CONNECTION']['USERNAME']
    PASSWORD = BUCKET_NAME = config['CONNECTION']['PASSWORD']

    user_data ='''#!/bin/bash
    
    cd /root
    apt install apt-transport-https software-properties-common -y
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
    add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'
    apt update -y
    apt install r-base -y
    apt install r-base-core -y
    apt-get install build-essential -y
    
    apt install python-pip -y
    apt install python3-pip -y
    pip3 install --upgrade pip
    pip3 install sklearn matplotlib boto3
    pip install awscli --upgrade
    echo 'export PATH=~/.local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc

    mkdir ~/.aws

    touch ~/.aws/credentials
    echo '[default]' >> ~/.aws/credentials
    '''  + '''echo 'aws_access_key_id=''' + USERNAME + '''' >> ~/.aws/credentials
    echo 'aws_secret_access_key=''' + PASSWORD + '''' >> ~/.aws/credentials

    touch ~/.aws/config
    echo '[default]' >> ~/.aws/config
    echo 'region=us-east-2' >> ~/.aws/config
    echo 'output=json' >> ~/.aws/config'''

    return user_data


'sha1:70bdfd9c118b:dd001ac9fe1a89e434cd0558776d90d081438fcd'
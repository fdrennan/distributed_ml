import configparser

def CreateUserData():
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    USERNAME         = config['CONNECTION']['USERNAME']
    PASSWORD         =  config['CONNECTION']['PASSWORD']
    GIT_USERNAME     = config['GIT']['git_username']
    GIT_EMAIL        = config['GIT']['git_email']
    GIT_REPO         = config['GIT']['repository']
    MODEL_DIRECTORY  = config['MODEL_DATA']['model_directory']
    SCRIPT           = config['MODEL_DATA']['script_to_run']
    BUCKET           = config['BUCKETS']['bucket_name']

    REPOSITORY       = 'git clone ' + GIT_REPO
    MODEL_ZIP        = MODEL_DIRECTORY + '.zip'
    BUCKET_DIR       = BUCKET + "/" + MODEL_ZIP
    DOWNLOAD_COMMAND = 'aws s3 cp s3://' + BUCKET_DIR + " " + MODEL_DIRECTORY + "/" + MODEL_ZIP
    UNZIP            = 'unzip ' + MODEL_ZIP
    RUN              = "python3 " + SCRIPT


    user_data ='''#!/bin/bash
    
    echo 'user_data running correctly' >> where_we_at
        
    cd /root
    
    apt install apt-transport-https software-properties-common -y

    echo "installing updates" >> where_we_at
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
    add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'
    apt update -y
    echo "installing R" >> where_we_at
    apt install r-base -y
    apt install r-base-core -y
    apt-get install build-essential -y
    
    echo "Configuring git" >> where_we_at
    
    apt-get install git-core''' + '''git config --global user.name "''' + GIT_USERNAME + '''"
    git config --global user.email "''' + GIT_EMAIL + '''"
    ''' + REPOSITORY + '''
    cp -r distributed_ml/. .
    echo "installing Python" >> where_we_at
    apt install python-pip -y
    apt install python3-pip -y
    
    pip3 install sklearn matplotlib boto3
    
    echo "installing AWS" >> where_we_at
    
    pip install awscli --upgrade
    echo 'export PATH=~/.local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc

    mkdir ~/.aws

    touch ~/.aws/credentials
    echo '[default]' >> ~/.aws/credentials
    '''  + '''echo 'aws_access_key_id=''' + USERNAME + '''' >> ~/.aws/credentials
    echo 'aws_secret_access_key=''' + PASSWORD + '''' >> ~/.aws/credentials''' + '''
    touch ~/.aws/config
    echo '[default]' >> ~/.aws/config
    echo 'region=us-east-2' >> ~/.aws/config
    echo 'output=json' >> ~/.aws/config
    ''' + DOWNLOAD_COMMAND + '''
    cd ''' +  MODEL_DIRECTORY + '''
    ''' + UNZIP + '''
    ''' + RUN + '''
    echo "Done" >> /root/where_we_at'''

    return user_data


'sha1:70bdfd9c118b:dd001ac9fe1a89e434cd0558776d90d081438fcd'
# pip install awscli
# aws configure
#
# https://docs.python.org/3/library/configparser.html
# source active distributed
# conda env export > environment.yml
# conda env create -f environment.yml
# conda env export --no-builds > distributed.yml
# conda env create -f distributed.yml
# jupyter notebook --no-browser --port=8888

import boto3
import configparser
from user_data import CreateUserData
import os
import datetime

class Distributor():

    NOW = datetime.datetime.now()

    config_exists = os.path.isfile('configuration.ini')

    if config_exists:

        s3 = boto3.resource('s3')
        ec2 = boto3.resource('ec2')

        config = configparser.ConfigParser()
        config.read('configuration.ini')

        BUCKET_NAME = config['BUCKETS']['BUCKET_NAME']
        LOCAL_DIR = config['DATA_DIR']['LOCAL']
        SERVER_DIR = config['DATA_DIR']['LOCAL']
        AMI = config['IMAGES']['UBUNTU_1808']
        RUNNING_IDS = dict(config['EC2_IDS'])
        # Connecting to S3
        BUCKET = boto3.resource('s3').Bucket(BUCKET_NAME)
        MODEL_DIRECTORY = config['MODEL_DIRECTORY']['pwd']
        user_data = CreateUserData()

    def __init__(self):
        if self.config_exists:
            print("Configuration File Found!")
        else:
            print("Please set up a configuration file. .")

    def update_config(self):
        config = configparser.ConfigParser()
        self.config.read('configuration.ini')

    def update_ids(self):
        self.RUNNING_IDS = dict(self.config['EC2_IDS'])

    def get_reservations(self):

        RESERVATIONS = boto3.client('ec2').describe_instances().get('Reservations')

        public_ips = []
        for state in range(0, len(RESERVATIONS)):
            state_logical = RESERVATIONS[state]['Instances'][0]['State']['Name']
            running.append(state_logical)
            if state_logical == 'running':
                public_ips.append(RESERVATIONS[state]['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddresses'][0]['Association']['PublicIp'])

        self.RUNNING = running
        self.PUBLIC_IPS = public_ips
        self.RESERVATIONS = RESERVATIONS

        return(running, public_ips)

    def download_file(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.BUCKET.download_file(self.origin, self.destination)

    def upload_file(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.BUCKET.upload_file(self.origin, self.destination)

    def launch_instances(self, n, size):

        res = self.ec2.create_instances(KeyName="Shiny",
                                     InstanceType=size,
                                     MinCount=1,
                                     MaxCount=n,
                                     SecurityGroupIds=[
                                         'launch-wizard-8'
                                     ],
                                     UserData=self.user_data,
                                     ImageId=self.AMI
                                     )

        self.update_config()
        self.update_ids()

        self.LEN_RUNNING = len(self.RUNNING_IDS)
        self.list_ids = {'server_' + str(key + self.LEN_RUNNING): res[key].instance_id for key in range(len(res))}

        # if len(self.RUNNING_IDS) != 0:
        #     self.ids = self.ids + self.RUNNING_IDS
        self.RUNNING_IDS.update(self.list_ids)

        self.config['EC2_IDS'] = self.RUNNING_IDS
        with open('configuration.ini', 'w') as configfile:
            self.config.write(configfile)

    def clear_instances(self):
        self.config['EC2_IDS'] = {}
        with open('configuration.ini', 'w') as configfile:
            self.config.write(configfile)

    def terminate_instances(self):
        self.ids = list(self.RUNNING_IDS.values())
        self.terminated = self.ec2.instances.filter(InstanceIds=list(self.ids)).terminate()
        self.clear_instances()
        self.update_config()
        self.update_ids()




############# DOWNLOADING DATA #######################
# s3.Bucket(BUCKET_NAME).download_file(KEY, KEY)

# s3.Bucket(BUCKET_NAME).upload_file('distributed.yml', 'distributed_server.yml')
# s3.Bucket(BUCKET_NAME).download_file('distributed_server.yml', 'distributed_server.yml')
# s3.Bucket(BUCKET_NAME).download_file('config_files/configuration.ini', 'configuration.ini')

############## UPLOADING DATA #########################


D = Distributor("my_model")
# D.launch_instances(1, 't2.medium')
print(D.user_data)


# Connecting to EC2

#
# client = boto3.client('ec2')
# client.terminate_instances(InstanceIds=ids)
#
#
# # Create ZIP File to save model
# shutil.make_archive(LOCAL_DIR + '.zip', 'zip', LOCAL_DIR)
#
# ssh -i "Shiny.pem" ubuntu@ec2-18-223-162-43.us-east-2.compute.amazonaws.com

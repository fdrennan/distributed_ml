import distributed_ml as dml

D = dml.Distributor(server = False)
D.launch_instances(1, 't2.medium')
D.upload_file()

D.download_file()

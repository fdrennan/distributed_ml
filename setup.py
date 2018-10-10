import distributed_ml as dml

D = dml.Distributor(server = False)
D.upload_file()
D.launch_instances(1, 't2.medium')

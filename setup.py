import distributed_ml as dml

D = dml.Distributor()
D.upload_file()
D.launch_instances(1, 't2.medium')

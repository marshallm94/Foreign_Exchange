# Foreign Exchange

###### Status: **In Progress** | August 2018

Python & AWS based Foreign Exchange Analysis

#### Setup

1. Navigate to `Foreign_Exchange/src/bash_scripts/` and run `$ bash launch_cluster.sh` from the command line to create an EMR cluster on AWS.

2. Run `$ bash aws_postgres_setup.sh` from the command line to create a PostgreSQL DB Instance on AWS RDS.

3. Once the status of the DB instance named *foreign-exchange* changes to available (can be found on the [AWS RDS Instances page](https://console.aws.amazon.com/rds/home?region=us-east-1#dbinstances:)), click on that instance and copy the **Endpoint**. It should look something like 'foreign-exchange.<some_series_of_letters>.<aws_region>.rds.amazonaws.com'

4. Navigate to `Foreign_Exchange/src/` and open **alpha_vantage_api.py**, **aws_table_setup.py** and **get_data.py**. In each of those files there will be a line that reads:

```python
connection = psycopg2.connect(host='',
                              dbname='forex',
                              user='awsuser',
                              port='5432',
                              password='foreignexchange')
```

Put the **Endpoint** as the host in the line (within quotes, for all three files).

5. Connect to the cluster named "ForexCluster" using ssh (can be found from the [Amazon EMR Dashboard](https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1#cluster-list:))

6. Once connected to the VM, run `[hadoop@ip-172-31-39-234 src]$ conda install psycopg2` to install psycopg2.

7. Clone the Foreign_Exchange repo onto the VM (using git, which was installed during the bootstrapping process).

8. Using `scp`, copy your alpha_vantage_api.json into the `Foreign_Exchange/src` directory **on the VM** from your local machine.

    `$ scp ~/path/to/your/local/file hadoop@<emr_master_public_dns>:/home/hadoop/Foreign_Exchange/src/`

9. **On the VM**, open alpha_vantage_api.py using nano or vim. Change the first few lines under the `if __name__ == "__main__":` to:

```python
with open("/home/hadoop/Foreign_Exchange/src/alpha_vantage_api.json", 'r') as f:
    data = json.load(f)
    api_key = data['api']
```

10. Test that everything is working on the VM by running:

    `[hadoop@ip-172-31-39-234 src]$ python alpha_vantage_api.py`.

    There shouldn't be any output from this script. Next run:

    `[hadoop@ip-172-31-39-234 src]$ python get_data.py`.

    A dataframe with 4 rows and the following columns should be printed to the command line:

    **'from_currency_code', 'from_currency_name', 'to_currency_code',
    'to_currency_name', 'exchange_rate', 'last_refreshed' and   'time_zone'**

11. Open the crontab.txt file and copy everything.

12. **On the VM**, open up the crontab for editing edit (default is vim).

    `[hadoop@ip-172-31-39-234 src]$ crontab -e`

    To enter edit/insert mode, press the "i" key. Paste the contents of the crontab.txt file here. Press the 'esc' key to exit edit mode, and then type ':wq' to write and quit.

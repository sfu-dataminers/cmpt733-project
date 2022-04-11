# Automated Twitter Response Tool
In this project, we aim minimise the airlines' tremendous workload by reducing the amount of tweets to respond to, as well as the time it takes for users to get answers to their questions. Furthermore, the sentiment analysis performed on tweets may aid airlines in monitoring the character of their clients and providing better services to them.

#### Team Members
- Dhruv Patel
- Himalya Bachwani
- Kishan Thumar
- Rahil Balar

### Objective
The automated responses on Twitter, on which many businesses rely these days, do not give people a sense of involvement. Our goal is to reassure the user that their adverse airline query or experience is being considered, and to suggest a viable solution.

### Dataset
- Twitter Labelled Data (Training): https://www.crowdflower.com/data-for-everyone/
- Twitter Unlabelled Data (Training): Fetched customer tweets for selected 8 airlines
- Twitter Unlabelled Data (Testing): Fetching live tweets mentioning @DataMinersSfu

### Project Architecture
![image](https://user-images.githubusercontent.com/23083816/162656503-2eefcbb6-ac3a-40eb-bd9b-1f30d32ab63c.png)

_All the initial commits were pushed in version-1 and after successfull validation it was merged with main branch_

### Steps to run the project

#### **1. Testing on Twitter**
- Setup Confluent Platform on your system by downloading the self managed version of the Confluent Platform: https://www.confluent.io/download
- Setting Up Zookeeper:<br>
  Adjust the zoopkeeper as per your system. In this case we will keep the default values
```
  cd your_directory/confluent-7.0.1/etc/kafka
  nano zookeeper.properties
```
- Setting up Kakfa Server:<br>
  For optimization, we will reduce the default log retention hours to 5, and reduce the log retention and segment bytes to 507374182
 ```
 nano server.properties
 log.retention.hours=5
 log.retention.bytes=507374182
 log.segment.bytes=507374182
 ```
 - Starting the servers:<br>
 We will keep the topic name dataminers for our project
 ```
 your_directory/confluent-7.0.1/bin/zookeeper-server-start your_directory/confluent-7.0.1/etc/kafka/zookeeper.properties
 your_directory/confluent-7.0.1/bin/kafka-server-start your_directory/confluent-7.0.1/etc/kafka/server.properties
 your_directory/confluent-7.0.1/bin/kafka-topics --bootstrap-server localhost:9092 --create --replication-factor 1 --partitions 2 --topic topic_name
 ```
- Starting the kafka producer:
```
python3 your_directory/kafka_producer.py
```
- Listening on kafka consumer:
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 your_directory/kafka_consumer.py topic_name
```
- Tweet your response: <br>
Try raising your issue on twitter with a mention to us i.e. **@DataMinersSfu**

#### **2. Testing on CLI**
- Run twitter_cli.py
```
python3 twitter_cli.py
```
- Browse through the example tweets using Menu option - 1
- Test your example tweet using Menu option - 2

# Save Your Money
The main idea of this repository is create a observability environment of your budget! 

### Configuring Notion

#### Create a table with the following columns (columnName:columnType)
 - <b>name</b>: title
 - <b>category</b>: select
 - <b>method</b>: select
 - <b>type</b>: select
 - <b>value</b>: number
 - <b>date</b>: date

#### Get the Notion table ID
When you are creating/editing the table you can see the ID in url: 
```
https://www.notion.so/[TABLE_ID_IS_HERE]?v=[SOME_MD5_HASH]
```

#### Create a Notion API token

You need to create a Notion integration. Go to this <a href='https://www.notion.so/my-integrations'>page</a> and follow the instructions. Be careful to create integration, make sure that the integration is not public.

#### Make the table available for your integration
At the top right of your table page you can se a three dot icon that will show a option "+ Add connections". Connect you table with your integration.

At this moment Notion is configured!

## MySQL Database configuration
The data is stored in the MySQL database, so we need to set up a a database and a single table that will be used to visualize the results in Grafana.

First of all, we need to create a database called 'sym':
```sql
CREATE DATABASE sym;
```
And now we create the table:
```sql
use sym;
CREATE TABLE `budget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notion_id` varchar(36) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `method` varchar(45) DEFAULT NULL,
  `_type` varchar(45) DEFAULT NULL,
  `value` float(10,2) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `notion_id_UNIQUE` (`notion_id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4;
```

## How to use

Set the following environment variables ( change 'xxx' values with your configurations ):
```bash
export NOTION_API_KEY="xxx"
export NOTION_BUDGET_DB="xxx"
export NOTION_URL="https://api.notion.com"
export MYSQL_HOST="xxx"
export MYSQL_PORT=3306
export MYSQL_DB="sym"
export MYSQL_USER="xxx"
export MYSQL_PASS="xxx"
```
Run the following command:
```bash
$ ./run.py
```

## Using Docker
Build image:
```bash
$ docker build -t sym:latest .
```
Execute the following command to start the container ( change 'xxx' values with your configurations ):
```bash
$ docker run --name sym \
    -e NOTION_API_KEY="xxx" \
    -e NOTION_BUDGET_DB="xxx" \
    -e NOTION_URL="https://api.notion.com" \
    -e MYSQL_HOST="xxx" \
    -e MYSQL_DB="sym" \
    -e MYSQL_PORT=3306 \
    -e MYSQL_USER="xxx" \
    -e MYSQL_PASS="xxx" \
    -d sym:latest
```
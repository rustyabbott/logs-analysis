# Logs Analysis

### Project Overview

This is the first project of Udacity's Fullstack Developer Nanodegree program. The assignment is to create an internal reporting tool that will use information from a given "news" database and analyze what kind of articles the site's readers like. The database contains three tables, which will need to be joined and sorted in various ways to answer:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


### Setup

1. Install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).
2. Clone Udacity's [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
3. [Download the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) (newsdata.sql) into your virtual machine folder ```/vagrant```.


### Log in

1. Start vagrant and log in:
```
$ vagrant up
$ vagrant ssh
```
2. Navigate to ```/vagrant```

### Load the Database
```
vagrant@vagrant:/vagrant psql -d news -f newsdata.psql
```

### Connect to the database
```
vagrant@vagrant:/vagrant psql -d news
```

### Create Views
1. Create article_view:
```
create view article_view as select author,title,count(*) as views from articles,log where log.path like concat('%',articles.slug) group by articles.title,articles.author order by views desc;
```

2. Create new_log_view:
```
create view new_log_view as select date(time),round(100.0*sum(case log.status when '200 OK' then 0 else 1 end)/count(log.status),2) as "error rate" from log group by date(time) order by "error rate" desc;
```

### Display the Output
1. Exit PostgreSQL
2. Navigate to:
```
vagrant@vagrant:/vagrant/logs-analysis
```
3. Run the script:
```
vagrant@vagrant:/vagrant/logs-analysis python3 source.py
```

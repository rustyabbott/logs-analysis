#!/usr/bin/env python3

import psycopg2

# Create article_view
#
# create view article_view as
#   select author,title,count(*) as views
#   from articles,log
#   where log.path like concat('%',articles.slug)
#   group by articles.title,articles.author
#   order by views desc;

question1 = ("What are the three most popular articles of all time?")
query1 = ("select title,views from article_view limit 3;")

question2 = ("Who are the most popular article authors of all time?")
query2 = ("""
            select authors.name,sum(article_view.views) as views
            from article_view,authors
            where authors.id = article_view.author
            group by authors.name
            order by views desc;
        """)

# Create new_log_view
#
# create view new_log_view as
#   select date(time),round(100.0*sum(case
#       log.status when '200 OK' then 0 else 1 end)/
#       count(log.status),2) as "error rate"
#       from log
#       group by date(time)
#       order by "error rate" desc;

question3 = ("On which days did more than 1% of requests lead to errors?")
query3 = ("select * from new_log_view where \"error rate\" > 1;")


def connect(database="news"):
    """
        Connects to 'news' database via pyscopg2
    """
    try:
        connection = psycopg2.connect("dbname={}".format(database))
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.Error) as error:
        print("Database connection failed: ", error)
        connection.close()


def results(query):
    """
        Fetches results from PostgreSQL queries
    """
    connection, cursor = connect()
    cursor.execute(query)
    return cursor.fetchall()
    connection.close()


def print_results(query_results):
    """
        Prints results for query1 and query2
    """
    print(query_results[1])
    for index, results in enumerate(query_results[0]):
        print(str(results[0] + " - " + str(results[1]) + " views."))
    print("\n")


def print_request_errors(query_results):
    """
        Prints results for query3
    """
    print(query_results[1])
    for results in query_results[0]:
        print(str(str(results[0]) + " - "
                  + str(results[1]) + "% request errors."))


if __name__ == '__main__':
    popular_articles = results(query1), question1
    popular_authors = results(query2), question2
    request_errors = results(query3), question3
    print_results(popular_articles)
    print_results(popular_authors)
    print_request_errors(request_errors)

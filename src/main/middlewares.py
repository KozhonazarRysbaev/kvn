from django.db import connection
from django.conf import settings


class SqlPrintMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG:
            self.show_queries(request, response)
        return response

    def show_queries(self, request, response):
        sqltime = 0  # Variable to store execution time
        for query in connection.queries:
            sqltime += float(query["time"])  # Add the time that the query took to the total

        # len(connection.queries) = total number of queries
        print("Page render: " + str(sqltime) + "sec for " + str(len(connection.queries)) + " queries")

        return response
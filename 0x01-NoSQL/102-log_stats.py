#!/usr/bin/env python3
"""
Improves 12-log_stats.py by adding the top 10
of the most present IPs in the collection nginx of the database logs
"""
from pymongo import MongoClient


def log_stats():
    # Connect to the MongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total number of logs
    total_logs = collection.count_documents({})

    # Count the number of logs for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {
            method: collection.count_documents({"method": method})
            for method in methods
    }

    # Count the number of logs with method=GET and path=/status
    status_check = collection.count_documents({
        "method": "GET",
        "path": "/status"
    })

    # Get the top 10 most frequent IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()

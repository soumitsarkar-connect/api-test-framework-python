import os
import logging

def before_all(context):
    reports_path = os.path.join(os.getcwd(), "reports")

    if os.path.exists(reports_path):
        for root, dirs, files in os.walk(reports_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                except Exception as e:
                    logging.warning(f"Could not delete {file_path}: {e}")
    else:
        os.makedirs(reports_path)

    logging.info("Reports folder cleaned.")

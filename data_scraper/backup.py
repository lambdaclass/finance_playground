import logging
import os

import boto3
from botocore.exceptions import ClientError

from data_scraper import utils
from data_scraper.notifications import slack_notification, slack_report

logger = logging.getLogger(__name__)


def backup_data():
    """Uploads scraped files to S3 bucket.
    Set bucket name in environment variable $S3_BUCKET
    """
    try:
        bucket_name = utils.get_environment_var("S3_BUCKET")
    except EnvironmentError as e:
        logger.error(str(e))
        slack_notification("Backup failed. Set $S3_BUCKET env variable",
                           __name__)
        raise e

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    data_path = utils.get_save_data_path()

    cboe_data = os.path.join(data_path, "cboe")
    cboe_folders = []
    if os.path.exists(cboe_data):
        cboe_folders = [
            os.path.join(cboe_data, folder) for folder in os.listdir(cboe_data)
            if not folder.endswith("daily")
        ]

    tiingo_data = os.path.join(data_path, "tiingo")
    tiingo_folders = []
    if os.path.exists(tiingo_data):
        tiingo_folders = [
            os.path.join(tiingo_data, folder)
            for folder in os.listdir(tiingo_data)
        ]

    folders = cboe_folders + tiingo_folders
    for folder in folders:
        _upload_folder(bucket, folder, data_path)

    symbols = [os.path.basename(folder) for folder in folders]
    msg = "Successful backup of symbols: " + ", ".join(symbols)
    slack_report(msg, __name__)


def _upload_folder(bucket, folder, data_path):
    """Uploads folder contents to S3 bucket"""
    if not os.path.isdir(folder):
        return

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            key = os.path.relpath(file_path, data_path)
            if _key_exists(bucket, key):
                logger.debug("File already exists in S3")
                continue
            try:
                bucket.upload_file(file_path, key)
                logger.debug("Uploaded file %s to S3", file)
            except Exception as e:
                msg = "Error uploading data file {} to S3.\nReceived exception message {}".format(
                    file_path, str(e))
                logger.error(msg, exc_info=True)
                slack_notification(msg, __name__)
                raise e


def _key_exists(bucket, key):
    try:
        bucket.Object(key).load()
    except ClientError as e:
        return int(e.response["Error"]["Code"]) != 404
    return False

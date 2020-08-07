# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates thumbnails from the given input of photos.

Creates thumbnails for each photo uploaded. This function
runs asyncronously and outputs a thumbnail to the selected
THUMBNAIL_BUCKET_NAME under the THUMBNAIL_BUCKET_FOLDER.
This function assumes that only photos will be uplaoded to the 
bucket.

"""
import os
import tempfile
import base64
from google.cloud import storage, vision, datastore
from wand.image import Image
import cv2
import json
import re
import sys
import numpy as np

storage_client = storage.Client()
datastore_client = datastore.Client()
vision_client = vision.ImageAnnotatorClient()

THUMBNAIL_SIZE = 64
THUMBNAIL_BUCKET_NAME = 'embeddings_visualizer_output_bucket'
THUMBNAIL_FOLDER_NAME = 'thumbnails'


def process_image_input(file_data, context):
    """Creates thumbnail from given image.

    Retrieves given upload from trigger and uses wand.image
    to create a 64x64 pixel image and uploads it to
    THUMBNAIL_BUCKET_NAME.

    Args:
        file_data:
            Dictionary that contains data specific to the event.
        context:
            Cloud functions event metadata.
    """
    # Retrieves all the neccessary components of the
    # file path this blob will have in the output bucket.
    file_name = file_data['name']
    bucket_name = file_data['bucket']
    user_name, dataset_name, photo_name = get_blob_upload_components(file_name)
    thumbnail_file_name = os.path.join(user_name, dataset_name,
                                       THUMBNAIL_FOLDER_NAME, photo_name)

    print(f'Original image found at: gs://{bucket_name}/{file_name}')

    # Using the tempfile library this function downloads images from
    # the upload.
    print(f'Creating full_size_image_blob...')
    full_size_image_blob = storage_client.bucket(bucket_name).get_blob(
        file_name)
    print(f'Downloading to tmp file...')
    _, tmp_local_filename = tempfile.mkstemp()
    full_size_image_blob.download_to_filename(tmp_local_filename)

    # Uses the Image library to create a thumbnail and saves it
    # to the temp file
    with Image(filename=tmp_local_filename) as image:
        print(f'Creating thumbnail of size {THUMBNAIL_SIZE}px...')
        image.thumbnail(THUMBNAIL_SIZE, THUMBNAIL_SIZE)
        print(f'Saving thumbnail image to {tmp_local_filename}...')
        image.save(filename=tmp_local_filename)

    print(f'Creating thumbnail_blob...')

    # Uses the filepath made earlier with os.path.join to save the
    # thumbnail to the correct directory in the output bucket.
    thumbnail_blob = storage_client.bucket(THUMBNAIL_BUCKET_NAME).blob(
        thumbnail_file_name)



    # Uploads blob with current thumbnail to the correct directory
    # in the output bucket.
    thumbnail_blob.upload_from_filename(tmp_local_filename)


    print(f'Cleaning up tmp file {tmp_local_filename}...')
    os.remove(tmp_local_filename)
    print('Done!')


def get_blob_upload_components(file_name):
    """Retrives the user, dataset, and image names from filepath.

    Splits the filepath on slashes and 
    returns the first two & last results in the filepath from
    the array saved from .split().

    Args:
        file_data:
            Key containing filepath in a string.
    Returns:
        user:
            Name of the user who uploaded the files.
        dataset_name:
            Name of the dataset uploaded.
        photo_name:
            Name of the photo itself.

    """
    print(f'File name: {file_name}')
    parts = file_name.split('/')
    print(f'Parts: {parts}')
    user = parts[0]
    dataset_name = parts[1]
    photo_name = parts[-1]
    return user, dataset_name, photo_name

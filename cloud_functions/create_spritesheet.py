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
"""Used to create a spritesheet from the given thumbnails.
This Cloud Function runs to create a spritesheet of all the thumbnails
that have been uploaded to the bucket. The function checks to make sure
that the file isn't a embeddings or the spritesheet itself, and concatanates
all thumbnails into a numpy array
"""

import os
import tempfile
import base64
from google.cloud import storage, vision, datastore
import json
import re
import sys
import numpy as np
import cv2
import json

# Initiating the storage & datastore clients.
storage_client = storage.Client()
datastore_client = datastore.Client('step-2020-johndallard')
vision_client = vision.ImageAnnotatorClient()
BUCKET_NAME = 'embeddings_visualizer_output_bucket'
SPRITESHEET_FOLDER_NAME = 'spritesheets'
SPRITESHEET = 'spritesheet'

def create_spritesheet(file_data, context):
    """Creates a spritesheet.
    Retrieves thumbnails and outputs them to BUCKET_NAME in a spritesheet
    using a numpy array. Images will be read using cv2
    Args:
        file_data:
            Dictionary that contains data specific to the event.
        context:
            Cloud functions eventmetadata.
    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:
    """

    file_name = file_data['name']
    user_name, dataset_name = get_user_and_dataset_name(file_name)

    spritesheet_file_name = (os.path.join(user_name, dataset_name,
                                        spritesheet_folder_name, SPRITESHEET))

    # We check to make sure the image is does not have the same name as the spr
    # itesheet, so that when we upload the spritesheet the function doesn't run
    # again
    if SPRITESHEET in file_name or '.npy' in file_name:
        return
    spritesheet_file_name = spritesheet_file_name + '.png'

    # Check to make sure there is metadata, if none return no data and error
    # message
    metadata = get_metadata(user_name, dataset_name)
    if metadata is None:
        return

    num_expected_thumbnails = get_expected_thumbnail_number(metadata)

    # Check the amount of images already in the bucket from the dataset
    folder = os.path.join('/', file_name.split('/')[:-1])
    thumbnail_file_names = sorted(list_blobs_with_prefix(BUCKET_NAME, folder))
    num_actual_thumbnails = len(thumbnail_file_names)

    # Compare the number of actual thumbnails to expected. Since this cloud fun
    # ction runs every time something is uploaded, the function checks to make
    # sure all thumbnails are there.
    if num_actual_thumbnails < num_expected_thumbnails:
        return

    spritesheet = None
    for thumbnail_file_name in thumbnail_file_names:
        thumbnail = load_image(BUCKET_NAME, thumbnail_file_name)
        spritesheet = thumbnail if spritesheet is None else np.concatenate(
            (spritesheet,
            thumbnail), axis=1)

    save_image(BUCKET_NAME, spritesheet_file_name, spritesheet)


def load_image(bucket_name, file_name):
    """Loads an image.
    Retrieves image from bucket and returns in in a cv2 format.
    Args:
        bucket_name:
            Dictionary that contains data specific to the bucket.
        file_name:
            Dictionary that contains data specific to the event.
    Returns:
        A cv2 image.
    """
    if not bucket_name or not file_name:
        return
    tmp_file_name = os.path.join('/tmp', file_name.split('/')[-1])
    _, tmp_file_name = tempfile.mkstemp()

    storage_client.bucket(bucket_name).get_blob(
        file_name).download_to_filename(tmp_file_name)
    image = cv2.imread(tmp_file_name)

    os.remove(tmp_file_name)

    return image


def save_image(bucket_name, file_name, image):
    """Saves an image.
    Saves the image by uploading it to the BUCKET_NAME.
    Args:
        bucket_name:
            Dictionary that contains data specific to the bucket.
        file_name:
            Dictionary that contains data specific to the event.
        image:
            Location of image to be saved.
    Returns:
        image: A cv2 image.
    """
    tmp_file_name = os.path.join('/tmp', 'tmp_image.png')
    cv2.imwrite(tmp_file_name, image)

    storage_client.bucket(bucket_name).blob(file_name).upload_from_filename(
        tmp_file_name)
    os.remove(tmp_file_name)
    print(image)
    return image


def get_expected_thumbnail_number(dataset):
    dataset_name, images_count_tuple, model, timestamp, user, viz_type = sorted(
        dataset.item)()
    return images_count_tuple[1]


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.
    Returns all the blobs in the specified bucket with the specified
    prefix.
    Args:
        bucket_name:
            Dictionary that contains data specific to the bucket.
        prefix:
            The prefix for all blobs to be returned..
        Delimeter = None:
            Specifies for specific blobs within the prefix.
    Returns:
        A list of blobs.
    """
    blobs = storage_client.list_blobs(
        bucket_name, prefix=prefix, delimiter=delimiter)

    # We check to see if there is a '.' extension, to ensure that an actual fil
    # e is being uploaded, not a folder since the function runs every time some
    # thing is uploaded
    return [blob.name for blob in blobs if '.' in blob.name]


def get_user_and_dataset_name(file_name):
    """Gets the name of the user and the dataset uploaded.
    Returns the user and dataset name in a tuple by splitting the upload file p
    ath.
    Args:
        file_name:
            Dictionary that contains data specific to the upload.
    Returns:
        The name of the user and dataset name.
    """
    parts = file_name.split('/')
    user = parts[0]
    dataset_name = parts[1]

    # If the area after the second slash (where the datastore name should b
    # e) is empty, then look through the rest of the string until there is 
    # a name a vailable if not then just return the user. The while loop en
    # ds when there is a string that is not empty, meaning there is a name 
    # there.
    i = 1
    while not parts[i] and i < len(parts) - 1:
        i = i + 1
    return user, parts[i] if len(parts[i]) > 0 else 'No dataset found'


def get_metadata(user, dataset_name):
    """Gets the metadata of the specific upload.
    Checks datastore for an the latest entity that matches the name of the user
    and dataset name.
    Args:
        user:
            Name of the user that uploaded the file.
        dataset_name:
            Name of the dataset uploaded.
    Returns:
        the most recent entity uploaded, if nothing
        is present then none.
    """
    query = datastore_client.query(kind='MetaData')
    query.add_filter('user-email', '=', user)
    query.add_filter('dataset-name', '=', dataset_name)
    result = list(query.fetch())
    return result[0] if len(result) >= 1 else None


def get_photo_name(file_name):
    """Gets the name of the photo uploaded, without filepath.
    Splits slases in file_name string and returns the last
    element, which is the name of the image and it's
    extension. If there is no photo found after the last /, then return the str
    ing before
    Args:
        file_name:
            Dictionary that contains data specific to the upload.
    Returns:
        The name of the photo.
    """
    parts = file_name.split('/')

    # If there is no name after the last slash, take the name before the last s
    # lash 
    if not parts[-1]:
        return parts[-2]
    return parts[-1]

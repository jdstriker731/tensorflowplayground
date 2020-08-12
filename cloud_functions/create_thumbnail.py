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
import file_path_utils as fp
from google.cloud import storage, vision, datastore
from wand.image import Image

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
    user_name, dataset_name = get_user_and_dataset_name(file_name)
    photo_name = get_photo_name(file_name)
    thumbnail_file_name = os.path.join(
        user_name, dataset_name,THUMBNAIL_FOLDER_NAME, photo_name)

    # Using the tempfile library this function downloads images from
    # the upload.
    full_size_image_blob = storage_client.bucket(bucket_name).get_blob(
        file_name)
    _, tmp_local_filename = tempfile.mkstemp()
    full_size_image_blob.download_to_filename(tmp_local_filename)

    # Uses the Image library to create a thumbnail and saves it
    # to the temp file
    with Image(filename=tmp_local_filename) as image:
        image.thumbnail(THUMBNAIL_SIZE, THUMBNAIL_SIZE)
        image.save(filename=tmp_local_filename)

    # Uses the filepath made earlier with os.path.join to save the
    # thumbnail to the correct directory in the output bucket.
    thumbnail_blob = storage_client.bucket(THUMBNAIL_BUCKET_NAME).blob(
        thumbnail_file_name)

    # Uploads blob with current thumbnail to the correct directory
    # in the output bucket.
    thumbnail_blob.upload_from_filename(tmp_local_filename)

    os.remove(tmp_local_filename)


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
    return fp.get_user_and_dataset_name(file_name)


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
    return fp.get_photo_name()

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
"""This function creates embeddings from a given image input.

This cloud function first saves all necessary components of the DELG model to t
mp directories from GCP storage buckets and after doing so uses tensorflow to l
oad and run the saved model on the image.
"""
import os
import tempfile
from google.cloud import storage
import cv2
import numpy as np
import tensorflow as tf

REQUIRED_SIGNATURE = 'serving_default'
REQUIRED_OUTPUT = 'global_descriptor'
EMBEDDING_BUCKET_NAME = 'embeddings_visualizer_output_bucket'
EMBEDDINGS_FOLDER_NAME = 'embeddings'
MAX_RESOLUTION = 800

# SETUP (runs once, when deploying):

# Storage API
storage_client = storage.Client()

# Create tmp dirs for DELG SavedModel. (Hard-drive is locked, must download all files to /tmp!) 
os.mkdir('/tmp/saved_model')
os.mkdir('/tmp/saved_model/variables')

# Download DELG SavedModel files:
model_bucket = storage_client.bucket('delg_model_bucket')

saved_model_blob = model_bucket.get_blob('saved_model.pb')
saved_model_blob.download_to_filename('/tmp/saved_model/saved_model.pb')

variable_index_blob = model_bucket.get_blob('variables/variables.index')
variable_index_blob.download_to_filename('/tmp/saved_model/variables/variables.index')

variable_data_blob = model_bucket.get_blob('variables/variables.data-00000-of-00001')
variable_data_blob.download_to_filename('/tmp/saved_model/variables/variables.data-00000-of-00001')

# Load DELG from SavedModel dir.
model = tf.saved_model.load('/tmp/saved_model/')

# Make a fn() from the loaded model.
embedding_fn = model.signatures[REQUIRED_SIGNATURE]

# Entry point: triggered when file is added to the input bucket
def extract_and_save_embedding(file_data, context):
    """Extracts and saves embeddings.

    Runs locally saved delg model on each image, and uploads
    the image blob to storage

    Args:
        file_data:
            Dictionary that contains data specific to the event.
        context:
            Cloud functions eventmetadata.
    """
    image = load_image(file_data['bucket'], file_data['name'])
    embedding = get_embedding(image)
    save_embedding(file_data['name'], embedding)


def load_image(bucket_name, image_file_name):
    """Loads the actual image itself.

    Retrieves the image from storage, and resizes it if neccessary.
    Args:
        bucket_name:
            GCP bucket for the image.
        image_file_name:
            Name of the image itself.
    """
    tmp_image_filename = os.path.join('/tmp', image_file_name.split('/')[-1])

    storage_client.bucket(bucket_name).get_blob(image_file_name).download_to_filename(tmp_image_filename)
    image = cv2.imread(tmp_image_filename)

    # We check to make sure the image isn't too large for the 
    # model that we are running
    height, width, channels = image.shape
    long_side = max(width, height)

    # If the image is larger than the biggest resolution
    # then we have to resize it.
    if long_side > MAX_RESOLUTION:
        scale_ratio = MAX_RESOLUTION / long_side
        width = int(width * scale_ratio)
        height = int(height * scale_ratio)
        new_size = (width, height)
        image = cv2.resize(image, new_size, interpolation = cv2.INTER_AREA)

    os.remove(tmp_image_filename)
    return image


def get_embedding(image):
    """Gets an embedding on the current image.

    Runs the DELG model on the current image.

    Args:
        image:
            CV2 image to be ran through model.
    """    
    image_tensor = tf.convert_to_tensor(image)
    print(f'coverting image to tensor')
    return embedding_fn(image_tensor)[REQUIRED_OUTPUT].numpy()


def save_embedding(image_name, embedding):
    """Saves the image and stores it to the output bucket.

    Runs the DELG model on the current image.
    
    Args:
        embedding:
            Numpy array embeddings for the given image.
        image_name:
            Name of the image, needed for storage.
    """
    # Embeddings have to be saved to a tmp file
    tmp_name = '/tmp/embedding.npy'
    np.save(tmp_name, embedding)

    # Embedding gets saved to directory in storage
    user_name, dataset_name, photo_name = get_blob_upload_components(
        image_name)
    embeddings_file_name = os.path.join
        (user_name, dataset_name, EMBEDDINGS_FOLDER_NAME, photo_name + '.npy')
    print(f'embeddings_file_name = {embeddings_file_name}')
    bucket = storage_client.bucket(EMBEDDING_BUCKET_NAME)
    blob = bucket.blob(embeddings_file_name)
    blob.upload_from_filename(tmp_name)
    os.remove(tmp_name)
    print('removed tmp file!')


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
    parts = file_name.split('/')
    print(f'Parts: {parts}')
    user = parts[0]
    dataset_name = parts[1]
    photo_name = parts[-1]
    return user, dataset_name, photo_name

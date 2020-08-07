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
"""Used to create a tsne embedding coordinates from the given embeddings.

This Cloud Function runs to create coordinates of all the embeddings that have
been uploaded to the bucket. The function checks to make sure all the embedding
s have been uploaded, then gets the coordinates.
"""
import numpy as np
import os
from sklearn.manifold import TSNE
from google.cloud import storage, datastore
import json
import tempfile

# Cloud APIs:
storage_client = storage.Client()
datastore_client = datastore.Client('step-2020-johndallard')
OUTPUT_BUCKET_NAME = 'spritesheet_json'


def run_tsne(trigger_file, _):
    """
        Trigger function to run. Gets t-SNE coordinates from
        embeddings.

        First checks to make sure all embeddings are present, and
        after doing so saves all of them to an array. Once they have
        been saved, the points are saved from the tsne_embed function
        and saved to a json file in an output bucket

        Args:
            trigger_file: 
                Dictionary that contains data specific to the event.
            _:
                Cloud functions event metadata.
    """

    # Looks for all embeddings in the embedding folder to ensure they are all t
    # here
    folder = '/'.join(trigger_file['name'].split('/')[:-1])
    embedding_file_names = sorted(list_blobs_with_prefix(
        trigger_file['bucket'], folder))
    num_actual_embeddings = len(trigger_file['name'])

    user_name, dataset_name = get_user_and_dataset_name(trigger_file['name'])

    metadata = get_metadata(user_name, dataset_name)
    num_expected_embeddings = get_expected_num_embeddings(metadata)

    if num_actual_embeddings < num_expected_embeddings:
        print('Waiting for all embeddings before running t-sne.')
        return

    # Loading the embedding of each image
    embeddings = []
    for embedding_file_name in embedding_file_names:
        this_json = load_embedding(trigger_file['bucket'], embedding_file_name)
        embeddings.append(this_json)

    # Runs tsne_embed on embedding array
    points = tsne_embed(embeddings)

    my_json = {'points': points}

    # Saving output to json file and uploading it to
    # bucket
    tmp_json_filename = os.path.join('/tmp', 'this_json.json')
    with open(tmp_json_filename, 'w') as json_file:
        json.dump(my_json, json_file)
    file_json_name = os.path.join(user_name, dataset_name, 'coordinates.json')
    storage_client.bucket(OUTPUT_BUCKET_NAME).blob(file_json_name).upload_from_filename(
        tmp_json_filename)
    os.remove(tmp_json_filename)


def load_embedding(bucket_name, file_name):
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
    tmp_file_name = os.path.join('/tmp', file_name.split('/')[-1])
    _, tmp_file_name = tempfile.mkstemp()

    storage_client.bucket(bucket_name).get_blob(
        file_name).download_to_filename(tmp_file_name)
    embedding = np.load(tmp_file_name)

    os.remove(tmp_file_name)

    return embedding


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
    print(f'Parts: {parts}')
    user = parts[0]
    dataset_name = parts[1]

    # If the area after the second slash (where the datastore name should be) i
    # s empty, then look through the rest of the string until there is a name a
    # vailable if not then just return the user. The while loop ends when there
    # is a string that is not empty, meaning there is a name there
    i = 1
    while not parts[i] and i < len(parts) - 1:
        i = i + 1
    return user, parts[i] if len(parts[i]) > 0 else 'No dataset found'



def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.

    Returns all the blobs in the specified bucket with the specified prefix.

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
    return [blob.name for blob in blobs if '.' in blob.name]


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
    print("we got to the metadata function")
    query = datastore_client.query(kind='MetaData')
    query.add_filter('user-email', '=', user)
    query.add_filter('dataset-name', '=', dataset_name)
    print("filters added!")
    result = list(query.fetch())
    print(result)
    return result[0] if len(result) >= 1 else None


def get_expected_num_embeddings(metadata):
    """Gets the expected mumber of embeddings from datastore.

    Checks metadata for the correct number of photos uploaded from the datastor
    e entity. For every image there should be an embedding

    Args:
        metadata:
            Metadata for specific upload

    Returns:
        The amount of images from the upload. 
    """
    dataset_name, images_count_tuple, model, timestamp, user, viz_type = (
        sorted(metadata.items()))
    return images_count_tuple[1]


def tsne_embed(embedding_container):
    """
        Function to run TSNE on list of embeddings contained in embedding_conta
        iner

        Returns:
            points:
                List of python dicts of format

                points [
                    {
                        x: str(float),
                        y: str(float),
                        z: str(float)
                    },
                    {
                        x: str(float),
                        y: str(float),
                        z: str(float)
                    }
                    {
                        ...
                    } ...
                ]
    """

    embeddings = np.array(embedding_container)
    tsne_output = TSNE(n_components=3).fit_transform(embeddings)

    tsne_output_list = tsne_output.tolist()

    # Makes an array of dictionaries of points
    points = []
    for tsne_point in tsne_output_list:
        point_dict = {
            'x': tsne_point[0],
            'y': tsne_point[1],
            'z': tsne_point[2]
        }

        points.append(point_dict)

    return points

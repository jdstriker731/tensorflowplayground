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

from unittest import mock
from google.cloud import storage, datastore
import create_spritesheet

NAME = 'bosticc@google.com/coolest_man_alive/original_images/myles_hun.jpg'
PREFIX = 'bosticc@google.com/coolest_man_alive/original_images/'

# todo... add more tests.. wanted to get a pr in.

# This functions tests for the correct metadata retrieval of the file
def test_metadata_retrieval(capsys):
    key = 'image-count:',
    number = '1'

    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.get_metadata('bosticc@google.com', 'coolest_man_alive')
    out, err = capsys.readouterr()
    # This is the key for the object created in storage
    assert key, number in out

# This function checks to make sure a failed metadata retrieval
# returns nothing
def test_failed_metadata_retrieval(capsys):
    key = 'image-count:',
    number = '1'

    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.get_metadata('', 'coolest_man_alive')
    out, err = capsys.readouterr()
    # This is the key for the object created in storage
    assert '' in out

# This function checks to make sure we get the correct
# user and dataset name
def test_user_and_dataset(capsys):

    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.get_user_and_dataset_name(NAME)
    out, err = capsys.readouterr()
    # This is the key for the object created in storage
    assert 'bosticc@google.com' in out


# This functions tests for the correct photo name of the file
def test_photo_name(capsys):
    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.get_photo_name(NAME)
    out, err = capsys.readouterr()
    assert 'myles_hun.jpg' in out


# We test to make sure if we have a empty directory
# that the function terminates
def test_load_image(capsys):
    bucket_name ='embeddings_visualizer_output_bucket'
    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.load_image('', bucket_name)
    out, err = capsys.readouterr()
    assert 'Cant find that photo' in out

# This functions tests for the correct photo name of the file
def test_failed_photo_name(capsys):
    context = mock.MagicMock()
    context.event_id = 'step-2020-johndallard'
    context.event_type = 'gcs-event'

    # Call tested function
    create_spritesheet.get_photo_name('')
    out, err = capsys.readouterr()
    assert '' in out


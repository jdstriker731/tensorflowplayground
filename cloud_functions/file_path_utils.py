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
"""
These two functions are used by multiple cloud functions, multiple times. Th
ey both get a certain element of the file path from the photo uploaded.
"""


def get_user_and_dataset_name(file_name):
    """Gets the name of the user and the dataset uploaded.
    Returns the user and dataset name in a tuple by splitting the uploa
    d file path.
    Args:
        file_name:
            Dictionary that contains data specific to the upload.
    Returns:
        The name of the user and dataset name.
    """
    parts = file_name.split('/')
    user = parts[0]
    # If the area after the second slash (where the datastore name should be) i
    # s empty, then look through the rest of the string until there is a name a
    # vailable if not then just return the user. The while loop ends when there
    # is a string that is not empty, meaning there is a name there
    i = 1
    while not parts[i] and i < len(parts) - 1:
        i = i + 1
    return user, parts[i] if len(parts[i]) > 0 else 'No dataset found'


def get_photo_name(file_name):
    """Gets the name of the photo uploaded, without filepath.
    Splits slases in file_name string and returns the last
    element, which is the name of the image and it's
    extension. If there is no photo found after the last /, then return
    the string before.
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

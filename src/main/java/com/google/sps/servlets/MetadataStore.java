// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.google.sps.servlets;

import java.util.List;

/**
 * An interface that defines methods for interacting
 * with some type of external database (ex: Datastore, Firestore, SQL)
 */
public interface MetadataStore {

  /**
   * Stores a valid Metadata type into an external database.
   */
  public void storeData(Metadata data);

  /**
   * Retrieves the metadata information for a particular dataset.
   */
  public Metadata retrieveMetadata(String datasetName);

  /**
   * Retrieves all the names of datasets belonging to a 
   * particular user.
   */
  public List<String> getUsersDatasets(String user);

  /**
   * Checks to see if a particular user already has a dataset
   * with a particular name.
   */
  public boolean metadataExists(String datasetName, String user);
}

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

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.SortDirection;
import com.google.appengine.api.datastore.Query.Filter;
import com.google.appengine.api.datastore.Query.FilterOperator;
import com.google.appengine.api.datastore.Query.FilterPredicate;
import java.util.ArrayList;
import java.util.List;

/**
 * A class for storing and accessing Metadata entities within
 * Datastore.
 * @implements {MetadataStore}
 */
public class DatastoreMetadataStore implements MetadataStore {

  public DatastoreMetadataStore() {}

  /**
   * Stores a valid Metadata type into Datastore
   */
  public void storeData(Metadata data) {
    // Create service call to access Datastore
    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();

    // Create a new Entity
    Entity datasetEntity = new Entity("MetaData");
    datasetEntity.setProperty("user-email", data.user());
    datasetEntity.setProperty("dataset-name", data.dataset());
    datasetEntity.setProperty("model", data.model());
    datasetEntity.setProperty("visualizer-type", data.visualization());
    datasetEntity.setProperty("image-count", data.numberOfImages());
    datasetEntity.setProperty("timestamp", data.timestamp());

    // Place entity withing Datastore
    datastore.put(datasetEntity);
  }
  
  /**
   * Retrieves the metadata information stored withing Datastore
   * using a given dataset name.
   */
  public Metadata retrieveMetadata(String datasetName) {
    // Check to see if any entity has the same matching dataset name
    for (Entity entity : getAllDatastoreEntities().asIterable()) {
      String dataset = (String) entity.getProperty("dataset-name");

      if (dataset.equals(datasetName)) {
        // Get the remaining properties
        String email = (String) entity.getProperty("user-email");
        String model = (String) entity.getProperty("model");
        String visualizerType = (String) entity.getProperty("visualizer-type");
        long imageCount = (Long) entity.getProperty("image-count");
        long time = (Long) entity.getProperty("timestamp");
        return new AutoValue_Metadata(email, dataset, model, visualizerType, imageCount, time);
      }
    }
    return null;
  }

  /**
   * Retrieves all the names of datasets belonging to a 
   * particular user.
   */
  public List<String> getUsersDatasets(String user) {
    List<String> userDatasets = new ArrayList<String>();
    for (Entity entity : getAllDatastoreEntitiesForUser(user).asIterable()) {
      // Get this the dataset-name for this entry and store it
      String dataset = (String) entity.getProperty("dataset-name"); 
      userDatasets.add(dataset);
    }
    return userDatasets;
  }

  /**
   * Checks to see if a particular user already has a dataset
   * with a particular name.
   */
  public boolean metadataExists(String datasetName, String user) { 
    for (Entity entity : getAllDatastoreEntities().asIterable()) {
      String email = (String) entity.getProperty("user-email");
      String dataset = (String) entity.getProperty("dataset-name");

      if (email.equals(user)) {
        if (dataset.equals(datasetName)) {
          return true;
        }
      }
    }
    return false;
  }

  /**
   * Retrieves all of the entities from Datastore and 
   * returns them in a PreparedQuery.
   */
  private static PreparedQuery getAllDatastoreEntities() {
    Query query = new Query("MetaData").addSort("timestamp", SortDirection.ASCENDING);

    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
    PreparedQuery results = datastore.prepare(query);
    
    return results;
  }
  
  /**
   * Retrieves all of the entities from Datastore for a particular user and 
   * returns them in a PreparedQuery.
   */
  private static PreparedQuery getAllDatastoreEntitiesForUser(String user) {
    Filter propertyFilter = new FilterPredicate("user-email", FilterOperator.EQUAL, user);

    Query query = new Query("MetaData").setFilter(propertyFilter).addSort("timestamp", SortDirection.ASCENDING);
    
    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
    PreparedQuery results = datastore.prepare(query);

    return results;
  }
}

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


import static com.google.appengine.api.datastore.FetchOptions.Builder.withLimit;

import java.util.ArrayList;
import java.util.List;
import org.junit.Assert;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import com.google.appengine.tools.development.testing.LocalDatastoreServiceTestConfig;
import com.google.appengine.tools.development.testing.LocalServiceTestHelper;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.SortDirection;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

import com.google.sps.servlets.Metadata;
import com.google.sps.servlets.DatastoreMetadataStore;

public class DatastoreMetadataStoreTest {

  private final LocalServiceTestHelper helper =
      new LocalServiceTestHelper(new LocalDatastoreServiceTestConfig());

  // Entities to be put into [mock] Datastore
  private Entity datasetEntity1;
  private Entity datasetEntity2;
  private Entity datasetEntity3;
  private Entity datasetEntity4;
  private Entity datasetEntity5;
  private Entity datasetEntity6;
  private Entity datasetEntity7;

  // Sample metadata information for an entry in Datastore
  private static final String USER = "johndallard@google.com";
  private static final String DATASET = "my_test_dataset";
  private static final String MODEL = "DELG";
  private static final String VISUALIZATION = "t-SNE";
  private static final int NUMBER_OF_IMAGES = 7;
  private static final long TIMESTAMP = 1596730599767L;

  // Instance of DatastoreMetadatastore class 
  private MetadataStore datastoreStorage = new DatastoreMetadataStore();
  
  @Before
  public void setUp() {
    helper.setUp();
    setUpDatastore();
  }

  @After
  public void tearDown() {
    helper.tearDown();
  }
  
  @Test
  public void basicMetadataRetrieval() {
    // Test to show correct metadata retrieval for a particular dataset

    Metadata metadata = Metadata.of(USER, DATASET, MODEL, VISUALIZATION, NUMBER_OF_IMAGES, TIMESTAMP);
    datastoreStorage.storeData(metadata);
    Assert.assertEquals(metadata, datastoreStorage.retrieveMetadata(metadata.dataset()));
  }
  
  @Test
  public void retrieveNonexistantMetadata() {
    // Test to show what happens when a dataset doesn't exist

    Metadata metadata = datastoreStorage.retrieveMetadata("non_existant_dataset");
    Assert.assertEquals(null, metadata);
  }
  
  @Test
  public void testRetrieveUsersDatasets() {
    // Test the proper retrieval of a user's datasets

    List<String> testDatasetList = new ArrayList<String>();
    testDatasetList.add("johnnys_first_dataset");
    testDatasetList.add("test_testerson");
    testDatasetList.add("my_set");
    testDatasetList.add("latest_and_greatest");
    testDatasetList.add("set_five");
    testDatasetList.add("test_dataset");

    Assert.assertEquals(testDatasetList, datastoreStorage.getUsersDatasets("johndallard@google.com"));
  }

  @Test
  public void nonexistantUserDatasetsRetrieval() {
    // Test to show that nothing is returned when nonexistant user's
    // datasets are searched for in Datastore

    List<String> emptyDatasetList = new ArrayList<String>();
    Assert.assertEquals(emptyDatasetList, datastoreStorage.getUsersDatasets("myfake_email@gmail.com"));
  }

  @Test
  public void datasetForUserExists() {
    // Test to show metadataExists() will return true when a 
    // user has a particular dataset name belonging to them in Datastore 

    Assert.assertEquals(true, datastoreStorage.metadataExists("test_dataset", "johndallard@google.com"));
  }

  @Test
  public void nonexistantDatasetAndUserCombo() {
    // Test to show metadataExists() will return false when 
    // both the user and dataset name don't exist in Datastore

    Assert.assertEquals(false, datastoreStorage.metadataExists("truly_fake_dataset", "johndee731@gmail.com"));
  }
  
  @Test
  public void userDoesNotHaveDataset() {
    // Test to show metadataExists() will return false when 
    // the user exists but they don't have this dataset

    Assert.assertEquals(false, datastoreStorage.metadataExists("not_my_set", "johndallard@google.com"));
  }

  @Test
  public void userDoesNotOwnDataset() {
    // Test to show metadataExists() will return false when 
    // the user exists but the dataset belongs to another user

    Assert.assertEquals(false, datastoreStorage.metadataExists("gundams", "johndallard@google.com"));
  }

  public void setUpDatastore() {
    DatastoreService ds = DatastoreServiceFactory.getDatastoreService();

    datasetEntity1 = new Entity("MetaData");
    datasetEntity1.setProperty("user-email", "johndallard@google.com");
    datasetEntity1.setProperty("dataset-name", "johnnys_first_dataset");
    datasetEntity1.setProperty("model", "DELG");
    datasetEntity1.setProperty("visualizer-type", "t-SNE");
    datasetEntity1.setProperty("image-count", 12);
    datasetEntity1.setProperty("timestamp", 1596646266299L);

    datasetEntity2 = new Entity("MetaData");
    datasetEntity2.setProperty("user-email", "askewc@google.com");
    datasetEntity2.setProperty("dataset-name", "gundams");
    datasetEntity2.setProperty("model", "DELG");
    datasetEntity2.setProperty("visualizer-type", "t-SNE");
    datasetEntity2.setProperty("image-count", 5);
    datasetEntity2.setProperty("timestamp", 1596484244221L);

    datasetEntity3 = new Entity("MetaData");
    datasetEntity3.setProperty("user-email", "johndallard@google.com");
    datasetEntity3.setProperty("dataset-name", "my_set");
    datasetEntity3.setProperty("model", "DELG");
    datasetEntity3.setProperty("visualizer-type", "t-SNE");
    datasetEntity3.setProperty("image-count", 30);
    datasetEntity3.setProperty("timestamp", 1596666738747L);

    datasetEntity4 = new Entity("MetaData");
    datasetEntity4.setProperty("user-email", "johndallard@google.com");
    datasetEntity4.setProperty("dataset-name", "test_dataset");
    datasetEntity4.setProperty("model", "DELG");
    datasetEntity4.setProperty("visualizer-type", "t-SNE");
    datasetEntity4.setProperty("image-count", 7);
    datasetEntity4.setProperty("timestamp", 1596730599767L);

    datasetEntity5 = new Entity("MetaData");
    datasetEntity5.setProperty("user-email", "johndallard@google.com");
    datasetEntity5.setProperty("dataset-name", "set_five");
    datasetEntity5.setProperty("model", "DELG");
    datasetEntity5.setProperty("visualizer-type", "t-SNE");
    datasetEntity5.setProperty("image-count", 100);
    datasetEntity5.setProperty("timestamp", 1596668868234L);

    datasetEntity6 = new Entity("MetaData");
    datasetEntity6.setProperty("user-email", "johndallard@google.com");
    datasetEntity6.setProperty("dataset-name", "test_testerson");
    datasetEntity6.setProperty("model", "DELG");
    datasetEntity6.setProperty("visualizer-type", "t-SNE");
    datasetEntity6.setProperty("image-count", 42);
    datasetEntity6.setProperty("timestamp", 1596661024776L);

    datasetEntity7 = new Entity("MetaData");
    datasetEntity7.setProperty("user-email", "johndallard@google.com");
    datasetEntity7.setProperty("dataset-name", "latest_and_greatest");
    datasetEntity7.setProperty("model", "DELG");
    datasetEntity7.setProperty("visualizer-type", "t-SNE");
    datasetEntity7.setProperty("image-count", 77);
    datasetEntity7.setProperty("timestamp", 1596668419537L);

    
    // Place entities in emulated Datastore
    ds.put(datasetEntity1);
    ds.put(datasetEntity2);
    ds.put(datasetEntity3);
    ds.put(datasetEntity4);
    ds.put(datasetEntity5);
    ds.put(datasetEntity6);
    ds.put(datasetEntity7);
  }
}

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
import com.google.common.collect.ImmutableList; 
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

import com.google.sps.servlets.Metadata;
import com.google.sps.servlets.DatastoreMetadataStore;

public class DatastoreMetadataStoreTest {

  private final LocalServiceTestHelper helper =
      new LocalServiceTestHelper(new LocalDatastoreServiceTestConfig());

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
    // Test to show correct metadata retrieval for a particular dataset.

    Metadata metadata = 
        Metadata.of("johndallard@google.com", "my_test_dataset", "DELG", 
        "t-SNE", 7, 1596730599769L);
    datastoreStorage.storeData(metadata);
    Assert.assertEquals(metadata, datastoreStorage.retrieveMetadata(metadata.dataset()));
  }
  
  @Test
  public void retrieveNonexistantMetadata() {
    // Test to show what happens when a dataset doesn't exist.

    Metadata metadata = datastoreStorage.retrieveMetadata("non_existant_dataset");
    Assert.assertEquals(null, metadata);
  }
  
  @Test
  public void testRetrieveUsersDatasets() {
    // Test the proper retrieval of a user's datasets.

    List<String> testDatasetList = 
        ImmutableList.of("johnnys_first_dataset", "test_testerson", 
        "my_set", "latest_and_greatest", "set_five", "test_dataset");
    Assert.assertEquals(testDatasetList, 
        datastoreStorage.getUsersDatasets("johndallard@google.com"));
  }

  @Test
  public void nonexistantUserDatasetsRetrieval() {
    // Test to show that nothing is returned when nonexistant user's datasets are searched for in 
    // Datastore.

    List<String> emptyDatasetList = new ArrayList<String>();
    Assert.assertEquals(emptyDatasetList, 
        datastoreStorage.getUsersDatasets("myfake_email@gmail.com"));
  }

  @Test
  public void datasetForUserExists() {
    // Test to show metadataExists() will return true when a user has a particular dataset name 
    // belonging to them in Datastore.

    Assert.assertTrue(datastoreStorage.metadataExists("test_dataset", "johndallard@google.com"));
  }

  @Test
  public void nonexistantDatasetAndUserCombo() {
    // Test to show metadataExists() will return false when both the user and dataset name don't 
    // exist in Datastore.

    Assert.assertFalse(
        datastoreStorage.metadataExists("truly_fake_dataset", "johndee731@gmail.com"));
  }
  
  @Test
  public void userDoesNotHaveDataset() {
    // Test to show metadataExists() will return false when the user exists but they don't have
    // this dataset.

    Assert.assertFalse(datastoreStorage.metadataExists("not_my_set", "johndallard@google.com"));
  }

  @Test
  public void userDoesNotOwnDataset() {
    // Test to show metadataExists() will return false when the user exists but the dataset belongs
    // to another user.

    Assert.assertFalse(datastoreStorage.metadataExists("gundams", "johndallard@google.com"));
  }

  public void setUpDatastore() {
    DatastoreService ds = DatastoreServiceFactory.getDatastoreService();
    
    Metadata metadata1 = 
        Metadata.of("johndallard@google.com", "johnnys_first_dataset", 
        "DELG", "t-SNE", 12, 1596646266299L);

    Metadata metadata2 = 
        Metadata.of("askewc@google.com", "gundams", "DELG", "t-SNE", 5, 1596484244221L);

    Metadata metadata3 = 
        Metadata.of("johndallard@google.com", "my_set", "DELG", "t-SNE", 30, 1596666738747L);

    Metadata metadata4 = 
        Metadata.of("johndallard@google.com", "test_dataset", "DELG", "t-SNE", 7, 1596730599767L);
    
    Metadata metadata5 = 
        Metadata.of("johndallard@google.com", "set_five", "DELG", "t-SNE", 100, 1596668868234L);

    Metadata metadata6 = 
        Metadata.of("johndallard@google.com", "test_testerson", 
        "DELG", "t-SNE", 42, 1596661024776L);

    Metadata metadata7 = 
        Metadata.of("johndallard@google.com", "latest_and_greatest", 
        "DELG", "t-SNE", 77, 1596668419537L);

    datastoreStorage.storeData(metadata1);
    datastoreStorage.storeData(metadata2);
    datastoreStorage.storeData(metadata3);
    datastoreStorage.storeData(metadata4);
    datastoreStorage.storeData(metadata5);
    datastoreStorage.storeData(metadata6);
    datastoreStorage.storeData(metadata7);
  }
}

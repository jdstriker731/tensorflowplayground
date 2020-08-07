import React from 'react';
import EmbeddingForm from './Form';
import styles from './App.scss';
import {ThreeRenderer} from './threeVisualizer.js'

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { datasets: [],
                    selectedDataset: "" };
    this.fetchUserDatasets = this.fetchUserDatasets.bind(this);
    this.selectionCallback = this.selectionCallback.bind(this);
  }

  selectionCallback(selection) {
    this.setState(() => {
      return {selectedDataset: selection};
      }, () => {console.log("dataset set to: " + selection)});
  }

    
  componentDidMount() {
    this.fetchUserDatasets();
  }

  fetchUserDatasets() {
    fetch("/dataset-names").then(response => response.json()).then(userDatasets => {
      // Store the names of the datasets the user has made
      this.setState({ datasets: userDatasets });
    });
  }

  datasetSelected() {
    return !!this.state.selectedDataset;
  }

  render() {
    return (
      <div className="App">
        <EmbeddingForm userDatasets={this.state.datasets} callback={this.selectionCallback} />
        { 
        this.datasetSelected() &&
        <ThreeRenderer canvasWidth={800} canvasHeight={800} dataset={this.state.selectedDataset} />
        }
      </div>
    );
  }
}

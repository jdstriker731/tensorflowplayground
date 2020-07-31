import React from 'react';
import EmbeddingForm from './Form';
import styles from './App.scss';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { datasets: [] };
    this.fetchUserDatasets = this.fetchUserDatasets.bind(this);
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


  render() {
    return (
      <div className="App">
        <EmbeddingForm userDatasets={this.state.datasets} />
      </div>
    );
  }
}

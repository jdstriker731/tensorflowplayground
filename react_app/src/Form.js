import React from 'react';
import CreationModal from './CreationModal.js';

const checkLoginStatus = () => {
  // Determine Log-in status of user
  window.location.replace('/authenticate');
};

class EmbeddingForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedValue: "",
      createMode: false
    };

    this.setSelection = this.setSelection.bind(this);
    this.submitSelection = this.submitSelection.bind(this);
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
  }

  setSelection(event) {
    event.persist();
    this.setState({selectedValue: event.target.value}, () => {
      console.log(this.state.selectedValue)
    });
  }

  submitSelection() {
    this.props.callback(this.state.selectedValue);
  }

  // Handles showing and hiding modal for dataset uploads
  showModal() {
    this.setState({ createMode: true });
  }

  hideModal() {
    this.setState({ createMode: false });
  }

  render() {
    return (
      <div className="form-wrapper">
        <CreationModal show={this.state.createMode} close={this.hideModal} />
        <button type="button" onClick={checkLoginStatus}>Login/Logout</button>
        <br />
        <div className="form">
          <div className="embedding-form">
              <label className="form-category">
                <span className="category-title">Dataset:</span>
                <select onChange={this.setSelection} name="dataset" id="dataset">
                  {this.props.userDatasets.map(value => (
                    <option className="form-option" key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </label>
            <button onClick={this.submitSelection} className="form-submit">
              Submit
            </button>
          </div>
        </div>
        <button
          type="button"
          className="create-dataset-button"
          onClick={this.showModal}
        >
          Create a new dataset
        </button>
      </div>
    );
  }
}

export default EmbeddingForm;

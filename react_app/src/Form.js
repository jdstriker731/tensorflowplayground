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
      values: [],
      createMode: false
    };

    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
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
          <form className="embedding-form" onSubmit={this.handleSubmit}>
              <label className="form-category">
                <span className="category-title">Dataset:</span>
                <select name="dataset" id="dataset">
                  {this.props.userDatasets.map(value => (
                    <option className="form-option" key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </label>
            <button type="submit" className="form-submit">
              Submit
            </button>
          </form>
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

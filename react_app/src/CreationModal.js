import React, { useState } from 'react';
import UploadIndicator from './UploadIndicator.js';
import styles from './CreationModal.scss';

function CreationModal({ show, close, children }) {
  // ------STATE MANAGEMENT-------
  const [files, setFiles] = useState([]);
  const [datasetName, setDatasetName] = useState("");
  const [hasName, setHasName] = useState(false);
  const [infoAvailable, setInfoAvailable] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const delay = ms => new Promise(res => setTimeout(res, ms));

  function datasetNameChange(event) {
    event.persist();
    setDatasetName(event.target.value);
    setHasName(true);
  }

  function fileUpload(event) {
    event.persist();
    setFiles([...files, ...event.target.files]);
    setInfoAvailable(true);
  }

  // Resets state to default values so that dialog refreshes if user enters again
  function clearStateAndClose() {
    setFiles([]);
    setDatasetName([]);
    setHasName(false);
    setInfoAvailable(false);
    setUploadComplete(false);
    document.getElementById('input-dialog').reset();

    close();
  }
  
  async function datasetUpload() {
    setUploading(true);
    await delay(4000); // Temporarily mock upload until web infrastructure in place
    setUploading(false);
    setUploadComplete(true);
  }
  
  return (
    show && (
    <div className='creation-modal'>
      <section className="modal-main">
        <UploadIndicator show={uploading}/>
        <form className="input-dialog" id="input-dialog" action="/upload" method="POST" enctype="multipart/form-data">
          <input
            type="text"
            className="dataset-namer"
            id="dataset-namer"
            name="dataset-namer"
            placeholder="Dataset name..."
            onChange={datasetNameChange}
          />
          <input
            type="file"
            className="file-upload-dialog"
            id="file-upload-dialog"
            name="file-upload-dialog"
            onChange={fileUpload}
            disabled={!hasName}
            accept=".jpg, .jpeg, .png"
            multiple
          />
          <label className="file-label" htmlFor="file-upload-dialog">
            Browse for photos
          </label>
          <div className="uploadInfo">
            <div className="dataset-info" disabled={!infoAvailable}>
              <p>Dataset Info:</p>
              <p>Name: {datasetName.length ? datasetName : 'N/A'}</p>
              <p>Number of images: {files.length > 0 ? files.length : 'N/A'}</p>
            </div>
            {!uploadComplete && (
              <button
                type="submit"
                className="dataset-upload"
                disabled={!infoAvailable}
                onClick={datasetUpload}
              >
                Upload dataset
              </button>
            )}
          </div>
          {uploadComplete && (
            <div className="post-upload">
              <p>Dataset upload complete!</p>
              <button className="close-modal" onClick={clearStateAndClose}>
                Close
              </button>
            </div>
          )}
        </form>
        {!uploadComplete && (
          <button className="cancel" onClick={clearStateAndClose}>
            Cancel
          </button>
        )}
      </section>
    </div>
  ));
}

export default CreationModal;

import React from 'react';
import Loader from 'react-loader-spinner';

function UploadIndicator({ show }) {

  return (
    show && (
      <div className="creation-modal">
        <Loader
          type="TailSpin"
          color="#4287f5"
          height="100"
          width="100"
          top="auto"
          bottom="auto"
        /> 
      </div>
    )
  );
}

export default UploadIndicator;

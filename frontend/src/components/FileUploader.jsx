import PropTypes from 'prop-types';

export default function FileUploader({ selectedFile, onFileSelect }) {
  const handlePick = (event) => {
    const file = event.target.files[0];
    if (file && file.type !== 'application/pdf') {
      onFileSelect(null);
      return;
    }
    onFileSelect(file);
  };

  return (
    <div className="file-uploader">
      <input id="file" type="file" accept="application/pdf" onChange={handlePick} />
      <label htmlFor="file" className="file-button">
        {selectedFile ? selectedFile.name : 'Select PDF file'}
      </label>
      {selectedFile && <span className="file-size">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</span>}
    </div>
  );
}

FileUploader.propTypes = {
  selectedFile: PropTypes.instanceOf(File),
  onFileSelect: PropTypes.func.isRequired,
};

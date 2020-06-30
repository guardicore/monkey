import React from 'react';
import AuthComponent from '../AuthComponent';

import {FilePond} from 'react-filepond';
import 'filepond/dist/filepond.min.css';


class PbaInput extends AuthComponent {

  constructor(props) {
    super(props);
    console.log("Constructor called");
    // set schema from server
    this.state = this.getStateFromProps(this.props);
  }

  getStateFromProps(props){
    let options = props.options
    // set schema from server
    return {
      PBAFile: options.PbaFile,
      filename: options.filename,
      apiEndpoint: options.apiEndpoint,
      setPbaFile: options.setPbaFile
    };
  }

  getPBAfile() {
    if (this.state.PBAFile.length !== 0) {
      return this.state.PBAFile
      return PbaInput.getMockPBAfile(this.state.PBAFile)
    } else if (this.state.filename) {
      return PbaInput.getFullPBAfile(this.state.filename)
    }
  }

  static getMockPBAfile(mockFile) {
    let pbaFile = [{
      name: mockFile.name,
      source: mockFile.name,
      options: {
        type: 'limbo'
      }
    }];
    pbaFile[0].options.file = mockFile;
    return pbaFile
  }


  static getFullPBAfile(filename) {
    return [{
      source: filename,
      options: {
        type: 'limbo'
      }
    }];
  }

  getServerParams(path) {
    return {
      url: path,
      process: this.getRequestParams(),
      revert: this.getRequestParams(),
      restore: this.getRequestParams(),
      load: this.getRequestParams(),
      fetch: this.getRequestParams()
    }
  }

  getRequestParams() {
    return {headers: {'Authorization': this.jwtHeader}}
  }

  render() {
    return (<FilePond
      key={this.state.apiEndpoint}
      server={this.getServerParams(this.state.apiEndpoint)}
      files={this.getPBAfile()}
      onupdatefiles={fileItems => {
        if (fileItems.length > 0) {
            this.state.setPbaFile([fileItems[0].file], fileItems[0].file.name)
        } else {
            this.state.setPbaFile([], "")
        }
      }}
    />)
  }
}


export default PbaInput;

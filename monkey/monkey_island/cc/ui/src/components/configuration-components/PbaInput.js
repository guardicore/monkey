import React from 'react';
import AuthComponent from '../AuthComponent';

import {FilePond} from 'react-filepond';
import 'filepond/dist/filepond.min.css';


class PbaInput extends AuthComponent {

  constructor(props) {
    super(props);
    // set schema from server
    this.state = this.getStateFromProps(this.props);
  }

  getStateFromProps(props){
    let options = props.options
    // set schema from server
    return {
      filename: options.filename,
      apiEndpoint: options.apiEndpoint,
      setPbaFilename: options.setPbaFilename
    };
  }

  componentDidUpdate(prevProps, _prevState, _snapshot) {
    if(prevProps.options.filename !== this.props.options.filename && this.props.options.filename === ''){
      this.setState({filename: this.props.options.filename})
    }
  }

  getPBAfile() {
    if (this.state.filename) {
      return PbaInput.getFullPBAfile(this.state.filename)
    }
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
            this.state.setPbaFilename(fileItems[0].file.name)
        } else {
            this.state.setPbaFilename('')
        }
      }}
    />)
  }
}


export default PbaInput;

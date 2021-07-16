import * as React from 'react';

class TextBox extends React.Component {

  render() {
    return (
      <p>{this.props.schema.text}</p>
    );
  }
}

export default TextBox;

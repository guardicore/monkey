import {css} from '@emotion/core';
import React, {Component} from 'react';
import {GridLoader} from 'react-spinners';
import * as PropTypes from 'prop-types';

const loading_css_override = css`
    display: block;
    margin-right: auto;
    margin-left: auto;
`;


export default class ReportLoader extends Component {
  render() {
    return <div id="loading-report" className='sweet-loading'>
      <h1>Generating Report...</h1>
      <GridLoader
        css={loading_css_override}
        sizeUnit={'px'}
        size={20}
        color={'#ffcc00'}
        loading={this.props.loading}
      />
    </div>
  }
}

ReportLoader.propTypes = {loading: PropTypes.bool};

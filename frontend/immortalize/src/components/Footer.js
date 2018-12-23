import React from 'react';
import PropTypes from 'prop-types';

const Footer = (props) => (
  <footer id="footer" style={props.timeout ? {display: 'none'} : {}}>
    <p className="copyright">Licensed under <a href="https://github.com/JSeam2/ShitpostBot2018/blob/master/LICENSE.md">MIT License</a></p>
  </footer>
)
import React from 'react';
import PropTypes from 'prop-types';

const Header = (props) => (
  <header id="header" style={props.timeout ? {display: 'none'} : {}}>
    <div className="content">
      <div className="inner">
        <h1>Immortalize</h1>
        <p>Immortalize yourself with Artificial Intelligence and Natural Language Generation</p>
      </div>
    </div>
    <nav>
      <ul>
        <li><a href="https://github.com/jseam2/shitpostbot2018">Github</a></li>
        <li><a href="javascript:;" onClick={() => {props.onOpenArticle('about')}}>About</a></li>
      </ul>
    </nav>
  </header>
)

Header.propTypes = {
  onOpenArticle: PropTypes.func,
  timeout: PropTypes.bool
}

export default Header;
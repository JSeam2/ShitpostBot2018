import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

class GenBox extends React.Component {
  constructor(props) {
    super(props);
    this.getData = this.getData.bind(this);
    this.state = {
      text: "Click Generate",
    }
  }

  getData() {
    // Get data from endpoint
    axios.get(this.props.endpoint)
    .then((res) => {
      console.log(res);
      this.setState({
        text: res.data.message
      });

    })
    .catch((err) => {
      console.log(err)
      this.setState({
        text: "Error Getting Text"
      });
    });

  }

  render() {
    return(
      <div id="footer" className="box" style={this.props.timeout ? {display: 'none'} : {}}>
        <center>
        <h2>{this.props.title}</h2>
          <button className="button" onClick={() => this.getData()}>Generate</button>
          <div className="gen-box">
            <p id="lstm-text" style={{ whiteSpace: 'pre-wrap' }}>{this.state.text}</p>
          </div>
        </center>
      </div>
    );
  }
}

GenBox.propTypes = {
  title: PropTypes.string,
  endpoint: PropTypes.string,
  timeout: PropTypes.bool
}


export default GenBox;
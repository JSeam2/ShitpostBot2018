import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

class Main extends React.Component {
  render() {
    let close = <div className="close" onClick={() => {this.props.onCloseArticle()}}></div>

    return(
        <div ref={this.props.setWrapperRef} id="main" style={this.props.timeout ? {display: 'flex'} : {display: 'none'}}>
          <article id="about" className={`${this.props.article === 'about' ? 'active': ''} ${this.props.articleTimeout ? 'timeout': ''}`} style={{display:'none'}}>
            <h2 className="major">About</h2>
            {/*<span className="image main"></span> to add header image*/}
            <p>
              <strong>Is it possible to reanimate ourselves in the event of death?</strong>
            </p>

            <p>
              While it appears difficult to upload our entire consciousness and store that consciousness in a digital form,
              social media appears to be a good enough approximation. We post our thoughts in the form of text or images.
              The ideas we subscribe and the scenes we capture are indicative of our conscious experience in that moment in time.
              Given the large amount of time spent on social media, we possess a valuable corpus of information about ourselves allowing
              us to develop models upon our own provided data. Given the current available technique in machine learning and deep learing,
              it becomes a realistic possibility of recreating ourselves digitally.
            </p>

            <p>
              For now, we will focus purely on textual information as an indicator of our consciousness. With the textual information,
              we can recreate posts that a person would post from their newsfeed. This can be achieved with generative text models.
              We investigate on a few generative techniques: Markov Chain Generation, Recurrent Neural Networks, and Generative Adverserial Networks.
              The current state of generative techniques are by no means perfect or close to the abilities of a human being.
              As such, this project remains as a work in progress. With newer advances in AI, we will improve the model when time permits.
            </p>

            <p>
              Contact Me:
              <ul>
                <li><a href="www.jseam.com">Blog</a></li>
                <li><a href="https://medium.com/@jseam">Medium</a></li>
                <li><a href="https://www.instagram.com/positivitynoh8/">Instagram</a></li>
                <li><a href="https://twitter.com/positivitynoh8/">Twitter</a></li>
              </ul>
            </p>
            {close}
          </article>
        </div>
    )
  }
}

Main.propTypes = {
  route: PropTypes.object,
  article: PropTypes.string,
  articleTimeout: PropTypes.bool,
  onCloseArticle: PropTypes.func,
  timeout: PropTypes.bool,
  setWrapperRef: PropTypes.func.isRequired
}

export default Main;
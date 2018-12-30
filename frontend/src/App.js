import React, { Component } from 'react';
// import logo from './logo.svg';
import './style/main.scss';

import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';
import GenBox from './components/GenBox';

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      isArticleVisible: false,
      timeout: false,
      articleTimeout: false,
      article: '',
      loading: 'is-loading'
    };

    this.handleOpenArticle = this.handleOpenArticle.bind(this);
    this.handleCloseArticle = this.handleCloseArticle.bind(this);
    this.handleClickOutside = this.handleClickOutside.bind(this);
    this.setWrapperRef = this.setWrapperRef.bind(this);
  }

  componentDidMount() {
    this.timeoutId = setTimeout(() => {
      this.setState({loading: ''}); 
    }, 100);
    document.addEventListener('mousedown', this.handleClickOutside);
  }

  componentWillUnmount() {
    if(this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  setWrapperRef(node) {
    this.wrapperRef = node;
  }

  handleOpenArticle(article) {
    this.setState({
      isArticleVisible: !this.state.isArticleVisible,
      article: article
    });

    setTimeout(() => {
      this.setState({
        timeout: !this.state.timeout
      })
    }, 325);

    setTimeout(() => {
      this.setState({
        articleTimeout: !this.state.articleTimeout
      })
    }, 350);
  }

  handleCloseArticle() {
    this.setState({
      articleTimeout: !this.state.articleTimeout
    });

    setTimeout(() => {
      this.setState({
        timeout: !this.state.timeout
      })
    }, 325);

    setTimeout(() => {
      this.setState({
        isArticleVisible: !this.state.isArticleVisible,
        article: ''
      })
    }, 350);
  }

  handleClickOutside(event) {
    if (this.wrapperRef && !this.wrapperRef.contains(event.target)) {
      if (this.state.isArticleVisible) {
        this.handleCloseArticle();
      }
    }
  }

  render() {
    return (
      <div className={`body ${this.state.loading} ${this.state.isArticleVisible ? 'is-article-visible' : ''}`}>
        <div id="wrapper">
          <Header onOpenArticle={this.handleOpenArticle} timeout={this.state.timeout} />
          <Main
            isArticleVisible={this.state.isArticleVisible}
            timeout={this.state.timeout}
            articleTimeout={this.state.articleTimeout}
            article={this.state.article}
            onCloseArticle={this.handleCloseArticle}
            setWrapperRef={this.setWrapperRef}
          />
          <GenBox
            title="Markov Chain Post Generator"
            endpoint="https://d2nzkaujplb9m9.cloudfront.net/generator/markov"
            timeout={this.state.timeout}
          />
          <GenBox
            title="LSTM RNN Post Generator"
            endpoint="https://d2nzkaujplb9m9.cloudfront.net/generator/lstm"
            timeout={this.state.timeout}
          />
          {/*<GenBox
            title="GAN Post Generator (TODO)"
            endpoint=""
            timeout={this.state.timeout}
          />
        */}
          <Footer timeout={this.state.timeout} />
        </div>
        {/*<div id="bg"></div>*/}
      </div>
    )
  }
}

export default App;

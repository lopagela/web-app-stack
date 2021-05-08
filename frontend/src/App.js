import React, { Component } from 'react';
// import logo from './logo.svg';
import LinkForm from "./components/Link/LinkForm.js"
import LinkTable from "./components/Link/LinkTable.js"
import './App.css';
import axios from 'axios';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      urls: [],
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  getLinks() {
    const urlApiLink = `${process.env.REACT_APP_API_URL}/api/v1/links`;
      axios.get(urlApiLink)
      .then((response) => {
          console.debug('Successfully downloaded the links');
          this.setState({urls: response.data.urls})
      })
      .catch((error) => {
          console.warn('Received an error from the API');
          console.warn(error)
      })
  }

  refreshLinks() {
    this.getLinks();
  }

  handleSubmit(url) {
    console.debug(`A url was submitted=${url}`);
    const urlApiLink = `${process.env.REACT_APP_API_URL}/api/v1/links`;
      axios.post(urlApiLink, {url: url})
      .then((response) => {
          console.info('Received a successful response from the API');
          console.info(response);
          this.refreshLinks();
      })
      .catch((error) => {
          console.warn('Received an error from the API');
          console.warn(error)
      })
  }

  componentDidMount() {
    this.getLinks();
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h1>Welcome to this (kind of useless) application!</h1>
        </div>
        <div>
          <p>
            Enter a valid HTTP(S) link the field below and click on send!
          </p>
          <p>
            This will save the link in the backend and displays it to you. Pretty cool huh?!
          </p>
        </div>
        <LinkForm handleSubmit={this.handleSubmit}/>
        <LinkTable urls={this.state.urls}/>
      </div>
    );
  }
}

export default App;

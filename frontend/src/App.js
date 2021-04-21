import React, { Component } from 'react';
// import logo from './logo.svg';
import LinkForm from "./components/Link/LinkForm.js"
import LinkTable from "./components/Link/LinkTable.js"
import './App.css';
import axios from 'axios';

// TODO make a components that renders the links saved in the app : GET /api/v1/link
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      links: [],
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  getLinks() {
    const urlApiLink = `${process.env.REACT_APP_API_URL}/api/v1/link`;
      axios.get(urlApiLink)
      .then((response) => {
          console.debug('Successfully downloaded the links');
          this.setState({links: response.data.links})
      })
      .catch((error) => {
          console.warn('Received an error from the API');
          console.warn(error)
      })
  }

  refreshLinks() {
    this.getLinks();
  }

  handleSubmit(link) {
    console.debug(`A link was submitted=${link}`);
    const urlApiLink = `${process.env.REACT_APP_API_URL}/api/v1/link`;
      axios.post(urlApiLink, {link: link})
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
        <LinkTable links={this.state.links}/>
      </div>
    );
  }
}

export default App;

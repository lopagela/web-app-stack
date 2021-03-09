import React, { Component } from 'react';
import axios from 'axios';
class LinkForm extends Component {
  constructor(props) {
    super(props);
    this.state = {link: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({link: event.target.value});
  }

  saveLink(link) {
    const urlApiLink = `${process.env.REACT_APP_API_URL}/api/v1/link`;
    axios.post(urlApiLink, {link: link})
    .then((response) => {
        console.info('Received a successful response from the API');
        console.info(response);
    })
    .catch((error) => {
        console.warn('Received an error from the API');
        console.warn(error)
    })
  }

  handleSubmit(event) {
  const { link } = this.state
    console.debug(`A link was submitted=${link}`);
    this.saveLink(link);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
      <label>
        Link:
        <input type="text" value={this.state.link} onChange={this.handleChange} />
      </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default LinkForm;
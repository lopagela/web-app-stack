import React, { Component } from 'react';
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

  // Wrapper of the handleSummit method given in the props
  handleSubmit(event) {
    console.debug(`Caught a form send action`)
    const { link } = this.state;
    this.props.handleSubmit(link)
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
      <label>
        Link:
        <input type="text" value={this.state.link} onChange={this.handleChange} />
      </label>
        <input type="submit" value="Send!" />
      </form>
    );
  }
}

export default LinkForm;
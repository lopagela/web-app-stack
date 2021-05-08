import React, { PureComponent } from 'react';
import styles from "./Link.module.css";

const regexpLink = RegExp("^http(s)?://")
class LinkTable extends PureComponent {

  prettyLink(_url) {
    const url = String(_url);
    if (! url.match(regexpLink)) {
      console.warn(`${url} is not a valid http(s) link, continuing`);
    }
    return String(url).replace(regexpLink, "");
  }

  render() {
    const tableItems = this.props.urls.map((url, indexUrl) => (
      <p key={indexUrl}><strong>Link {indexUrl}: </strong><a href={url}>{this.prettyLink(url)}</a></p>
    ));
    return (
      <div className={styles.linkContainer}>
        <div className={styles.tableLink}>
          {tableItems}
        </div>
      </div>
    )
  }
}

export default LinkTable;
import React, { PureComponent } from 'react';
import styles from "./Link.module.css";

const regexpLink = RegExp("^http(s)?://")
class LinkTable extends PureComponent {

  prettyLink(_link) {
    const link = String(_link);
    if (! link.match(regexpLink)) {
      console.warn(`${link} is not a valid http(s) link, continuing`);
    }
    return String(link).replace(regexpLink, "");
  }

  render() {
    const tableItems = this.props.links.map((link, indexLink) => (
      <p key={indexLink}><strong>Link {indexLink}: </strong><a href={link}>{this.prettyLink(link)}</a></p>
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
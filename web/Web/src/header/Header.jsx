import '../App.css'
import './Header.css'
import { Link } from "react-router-dom";

function Header({headerColor,headerHide}) {
    const color =headerColor ? "black": "";
    const hide = headerHide ? "hide": "";
  return (
      <div className={"header up "+ color +" " +hide}  id="header">
        <div className="name_container">
            <Link to="/" className="name" style={{ color: '#dddddd' }}>Name Placeholder</Link>
        </div>
        <div className="links_container">
            <Link to="/songs" style={{ color: '#dddddd'} } >songs</Link><a>posts</a>
        </div>
      </div>
  )
}

export default Header

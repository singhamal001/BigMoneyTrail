import { useState, useEffect } from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
// import logo from '../assets/img/logo.svg';
// import logo from '../assets/img/BMT-removebg-preview.png';
import logo from '../assets/img/bmtnew-removebg-preview.png';
import { HashLink } from 'react-router-hash-link';
import { Link } from "react-router-dom";


export const NavBar = () => {
  const [activeLink, setActiveLink] = useState('home');
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    }

    window.addEventListener("scroll", onScroll);

    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const onUpdateActiveLink = (value) => {
    setActiveLink(value);
  }

  return (
    <Navbar expand="md" className={scrolled ? "scrolled" : ""}>
      <Container>
        <Navbar.Brand href="/">
          <img src={logo} alt="Logo" />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav">
          <span className="navbar-toggler-icon"></span>
        </Navbar.Toggle>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" className={activeLink === 'home' ? 'active navbar-link' : 'navbar-link'} onClick={() => onUpdateActiveLink('home')}>Home</Nav.Link>
            <Nav.Link as={Link} to="/co-pilot" className={activeLink === 'copilot' ? 'active navbar-link' : 'navbar-link'} onClick={() => onUpdateActiveLink('copilot')}>Co-Pilot</Nav.Link>
            <Nav.Link as={Link} to="/dashboard" className={activeLink === 'dashboard' ? 'active navbar-link' : 'navbar-link'} onClick={() => onUpdateActiveLink('dashboard')}>Dashboard</Nav.Link>
            <Nav.Link as={Link} to="/about" className={activeLink === 'about' ? 'active navbar-link' : 'navbar-link'} onClick={() => onUpdateActiveLink('about')}>About-Us</Nav.Link>
          </Nav>
          <span className="navbar-text">
            <HashLink to='/co-pilot'>
              <button className="vvd"><span>Try Co-Pilot NOW!</span></button>
            </HashLink>
          </span>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
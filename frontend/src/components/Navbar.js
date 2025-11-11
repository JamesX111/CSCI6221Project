import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  const linkStyle = {
    textDecoration: 'none',
    color: 'white',
    padding: '0.5rem 1rem',
    border: '2px solid black',
    borderRadius: '5px',
    transition: 'all 0.25s ease-in-out',
    fontWeight: 500,
  };

  const hoverStyle = {
    backgroundColor: 'black',
    color: 'white',
  };

  const handleMouseOver = (e) => {
    e.target.style.backgroundColor = hoverStyle.backgroundColor;
    e.target.style.color = hoverStyle.color;
  };

  const handleMouseOut = (e) => {
    e.target.style.backgroundColor = 'white';
    e.target.style.color = 'black';
  };

  return (
    <nav
      style={{
        backgroundColor: '#082c6c', // moderate darker blue
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        height: '70px',
        padding: '0 2rem',
      }}
    >
      {/* Left side: Hospital Management */}
      <div style={{ color: 'white', fontSize: '1.5rem', fontWeight: 'bold' }}>
        <Link
          to="/"
          style={{ color: 'white', textDecoration: 'none' }}
        >
          Hospital Management
        </Link>
      </div>

      {/* Right side: Links */}
      <div style={{ display: 'flex', gap: '1rem' }}>
        {['Patients', 'Events', 'Resources', 'Accidents'].map((text) => (
          <Link
            key={text}
            to={`/${text.toLowerCase()}`}
            style={linkStyle}
            onMouseOver={handleMouseOver}
            onMouseOut={handleMouseOut}
          >
            {text}
          </Link>
        ))}
      </div>
    </nav>
  );
};

export default NavBar;

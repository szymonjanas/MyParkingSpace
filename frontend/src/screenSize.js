import { useState, useEffect } from 'react';

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height
  };
}

export function useScreenSize() {
  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());

  function handleResize() {
    setWindowDimensions(getWindowDimensions());
  }
  
  useEffect(() => {
    window.addEventListener('resize', handleResize);
  }, []);

  function isMobileWithParam(width) {
    return windowDimensions.width < width;
  }

  const isMobile = () => isMobileWithParam(900);

  return { isMobile };
}

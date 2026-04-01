import './App.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import InstructionUpload from './components/InstructionUpload';
import InputUpload from './components/InputUpload';
import DownloadFile from './components/DownloadFile';
import Toast from './components/Toast';
import { useState } from 'react';
import LoadingBar from 'react-top-loading-bar'
import Spinner from './components/Spinner';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './components/Home';
import hand from './assets/Hand.gif';

function App() {

  const [alert, setAlert] = useState(null);
  const [progress, setProgress] = useState(0);
  const [direction, setDirection] = useState(false);

  const showAlert = (message, type) => {
    setAlert({
      msg: message,
      type: type
    })
    setTimeout(() => {
      setAlert(null);
    }, 4000);
  }

  const showDirection = () => {
    setDirection(true);
    setTimeout(() => {
      setDirection(false);
    }, 3000);
  }

  return (
    <>
      <Navbar showDirection={showDirection} />
      <div className='bg-[radial-gradient(ellipse_90%_20%_at_top,var(--color-blue-800)_40%,#171328_100%)] h-lvh'>
        <div className='flex flex-row-reverse'>
          <Toast alert={alert} setAlert={setAlert} />
        </div>
        <Router>
          <LoadingBar height={3} color='#f11946' progress={progress} />
          {(progress != 0 && progress != 100) && <Spinner />}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/instruction" element={<InstructionUpload setProgress={setProgress} showAlert={showAlert} />} />
            <Route path="/input" element={<InputUpload setProgress={setProgress} showAlert={showAlert} />} />
            <Route path="/Download" element={<DownloadFile setProgress={setProgress} showAlert={showAlert} />} />
          </Routes>
        </Router>
        {direction && <img src={hand} className="absolute bottom-20 right-42" />}
        <Footer />
      </div>
    </>
  )
}

export default App

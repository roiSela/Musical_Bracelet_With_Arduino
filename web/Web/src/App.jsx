import { useState,useRef,useEffect } from 'react'
import './App.css'
import {Route,Routes} from "react-router-dom"
import Home from './home/Home'
import Songs from './songs/Songs'

function App() {
  return (
      <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/songs" element={<Songs />}/>
      </Routes>
  )
}

export default App

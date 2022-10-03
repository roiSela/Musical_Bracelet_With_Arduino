import './App.css'
import {Route,Routes} from "react-router-dom"
import Home from './home/Home'
import Songs from './songs/Songs'
import Posts from './posts/Posts'

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />}/>
            <Route path="/songs" element={<Songs />}/>
            <Route path="/posts" element={<Posts />}/>
        </Routes>
    )
}

export default App

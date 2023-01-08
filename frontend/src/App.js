import axios from 'axios';
import './App.css';

function App() {

  const handleUploadImage = async (ev) => {
    console.log('this is the ev:', ev);
    ev.preventDefault();

    const data = new FormData();
    data.append('file', ev.target.files[0]);
    data.append('filename', ev.target.files[0].name);
    await axios({
      url: 'http://localhost:8000/read', 
      data, 
      method: 'post',
      responseType:'arraybuffer' })
}
return (
  <div className="App">
    <input type="file" onChange={handleUploadImage} />
  </div>
);
}

export default App;

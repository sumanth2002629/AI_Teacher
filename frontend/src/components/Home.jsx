import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { saveAs } from 'file-saver';
import "bootstrap/dist/css/bootstrap.min.css";
import Button from 'react-bootstrap/Button';

function Home() {
    const navigate = useNavigate();
  const [file, setFile] = useState(null)
  const [pdfFile, setPdfFile] = useState(null)

  // On file select (from the pop up)
  const onFileChange = (event) => {
      // Update the state
      setFile(event.target.files[0])
  };

  // On file upload (click the upload button)
  const onFileUpload = async () => {
      // // Create an object of formData
      const formData = new FormData();

      // // Update the formData object
      console.log(file)
      formData.append(
          "audio", file
      );
      try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
          method: 'POST',
          body: formData,
        });
  
        if (response.ok) {
          console.log('File uploaded successfully');
          setPdfFile("success")

        } else {
          console.error('Failed to upload file');
        }
      } catch (error) {
        console.error('Network error:', error);
      }

      // // Details of the uploaded file
      // console.log(this.state.selectedFile);

      // // Request made to the backend api
      // // Send formData object
      // axios.post("api/uploadfile", formData);
  };

  const handleDownloadNotes = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/notes', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/pdf',
        },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'notes.pdf'; // Set the desired file name here
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else {
        console.error('Failed to fetch PDF file');
        // Handle failure
      }
    } catch (error) {
      console.error('Error fetching PDF file:', error);
      // Handle error
    }
  };
       
  const handleQuiz = (event) => {
    event.preventDefault();
    navigate("/quiz");
  };
  

  return (
  <div>
    <div className="title" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '2% auto'
        }}>
            <h1 style={{fontFamily:"Audrey"}}>GenWizard</h1>
            <h6 style={{marginTop:"3%"}}>An AI Teaching Assistant ready to help you.</h6>
            <h6>Don't want to hear all those boring lectures?</h6>
            <h6>Well AI can hear them for you and give you summary notes.</h6>
            <div className="audio-upload" style={{margin:"3%", borderStyle:"solid", padding:"1%", borderRadius:"5%"}}>
              <input className="input" name="audio"
                  type="file"
                  onChange={onFileChange}
                  accept=".wav"
              /> <br />
              <label htmlFor="audio">Only .wav files accepted</label>
              <div className="d-grid gap-2" style={{marginTop:"5%"}}>
                    <Button variant="primary" size="lg" onClick={onFileUpload}>
                        Upload
                    </Button>
                </div>
            </div>
            <div >
              {pdfFile && (
                <div className="container" style={{ display:"flex"}}>
                  <div className="button-container" style={{marginRight:"10%"}}>
                    <button className="btn btn-success" onClick={handleDownloadNotes}>Download Notes</button>
                  </div>
                  
                  <div className="button-container" style={{marginLeft:"10%"}}>
                    <button className="btn btn-info" onClick={handleQuiz}>Take Quiz</button>
                  </div>
                </div>
              )}
            </div>
        </div>
     {/* <Routes>
       <Route exact path="/" element={<Home />} />
       <Route path="/play" element={<Play />} />
       <Route path="/score" element={<Score />} />
     </Routes>  */}
   </div>
  );
}

export default Home;


import React from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';

function Score(props) {
    const navigate = useNavigate();
    
    const location = useLocation();
    const data = location.state;
    function playAgain() {
        navigate("/");
    }
    
    return(
        <div className="container" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '4% auto',
            height: '50vh',
            width: '30vw',
            border: '1px solid #63696f',
            borderRadius: '4px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        }}>
            <div className="score">
                <h2>Your Score is <h1>{data.score}/{data.total}</h1></h2>
                <br />
                <br />
            </div>
            <button className="btn btn-primary" onClick={playAgain}>Home</button>
        </div>
    );
}

export default Score;
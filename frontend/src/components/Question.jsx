import React from "react";
import "./question.css"
import "bootstrap/dist/css/bootstrap.min.css";
function Question(props) {
    return (
        <div className="question">
            <h3 className="queText">{props.question.question}</h3>
            
            {props.question.options.map((option, optionIndex) => (
                <div className="form-check option" key={optionIndex}>
                    
                    <input
                    className="form-check-input radio"
                    type='radio'
                    name={`Q${props.index}`}
                    value={option}
                    onChange={() => props.handleAnswerSelection(props.index, option)}
                    checked={props.selectedAnswers[props.index] === option}
                    />
                    <label className="form-check-label">{option}</label>
                </div>
                
            ))}
            
        </div>
    );
}

export default Question;
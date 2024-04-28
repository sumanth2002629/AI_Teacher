import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Question from './Question';
import "bootstrap/dist/css/bootstrap.min.css";

const Quiz = () => {
    const [questions, setQuestions] = useState(null);
    const [selectedAnswers, setSelectedAnswers] = useState({});
    const navigate = useNavigate();
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  useEffect(() => {
    // Fetch questions from backend when component mounts
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/quiz'); // Replace with actual backend URL
      if (response.ok) {
        let data = await response.json();

        if(typeof(data)==="string")
        {
          data = JSON.parse(data);
        }
        console.log(data)
        console.log(typeof(data))
        setQuestions(data);
      } else {
        console.error('Failed to fetch questions');
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  const handleAnswerSelection = (questionId, answer) => {
    setSelectedAnswers(prevAnswers => ({
      ...prevAnswers,
      [questionId]: answer
    }));
  };
  const handleNextQuestion = () => {
    setCurrentQuestionIndex(prevIndex => prevIndex + 1);
};

const handlePreviousQuestion = () => {
    setCurrentQuestionIndex(prevIndex => prevIndex - 1);
};

  const handleRestartQuiz = () => {
    setSelectedAnswers({});
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    let score = 0;
    questions.forEach((question, index) => {
      const selectedOptionIndex = selectedAnswers[index];
      if (selectedOptionIndex === question.answer) {
        score++;
      }
    });

    navigate('/score/', { state: { score: score, total: questions.length} });
  };
  let currentQuestion = -1;
  if(questions)
    currentQuestion = questions[currentQuestionIndex];

return(
    // <div className="container">
    //     <form onSubmit={handleFormSubmit}>
    //         {questions.map((question, index) => (
    //             <Question key={index} index={index} question={question} selectedAnswers={selectedAnswers} handleAnswerSelection={handleAnswerSelection}/>
    //         ))}
    //     <div className="submit-button" style={{
    //         display: 'flex',
    //         justifyContent: 'center',
    //         marginTop: '20px',
    //         marginBottom: '100px'
    //     }}>
    //         <button className="btn btn-primary" type="submit">Submit</button>
    //     </div>
    //     </form>
    // </div>
    currentQuestion!=-1 &&(<div className="container">
            <form onSubmit={handleFormSubmit}>
                <Question
                    key={currentQuestionIndex}
                    index={currentQuestionIndex}
                    question={currentQuestion}
                    selectedAnswers={selectedAnswers}
                    handleAnswerSelection={handleAnswerSelection}
                />
                <div className="navigation-buttons" style={{
                    display: 'flex',
                    justifyContent: 'center',
                    marginTop: '20px',
                    marginBottom: '100px'
                }}>
                    <button
                        className="btn btn-primary mr-2"
                        type="button"
                        onClick={handlePreviousQuestion}
                        disabled={currentQuestionIndex === 0}
                        style={{margin:"5%"}}
                    >
                        Previous
                    </button>
                    {currentQuestionIndex < questions.length - 1 && (
                        <button
                            className="btn btn-primary"
                            type="button"
                            onClick={handleNextQuestion}
                            style={{margin:"5%"}}
                        >
                            Next
                        </button>
                    )}
                    {currentQuestionIndex === questions.length - 1 && (
                        <button
                            className="btn btn-primary"
                            type="submit"
                        >
                            Submit
                        </button>
                    )}
                </div>
            </form>
        </div>)
);
};

export default Quiz;

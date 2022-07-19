import React from 'react';
import GreenArrow from './GreenArrow';
import RedArrow from './RedArrow';


const Arrows = (props) => {
    const probscore = props.probscore


    return (
        <div>
            {probscore > 0.6 ? <GreenArrow /> : <RedArrow />}
            <p style={{ fontWeight: "bold", fontSize: 30 }}>
                {props.probscore}
            </p>
        </div>
    )
}

export default Arrows;
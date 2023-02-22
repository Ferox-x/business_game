import React from "react"
import "./createGameStyles/inputStartGame.scss"

function InputStartGame({ htmlFor, type, value, placeholder, name, label, ...props }) {
	return (
		<label className="form_label_start_game" htmlFor={htmlFor}>
			{label}
			<input
				className="start_game_input"
				type={type}
				id={htmlFor}
				placeholder={placeholder}
			/>
		</label>
	)
}

export default InputStartGame

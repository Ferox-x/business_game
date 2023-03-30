import React from "react"
import "./createGameStyles/inputStartGame.scss"

function InputStartGame({
	htmlFor,
	type,
	value,
	placeholder,
	name,
	label,
	changeValue,
	...props
}) {
	return (
		<label className="form_label_start_game" htmlFor={htmlFor}>
			{label}
			<input
				className="form_label_start_game__input"
				type={type}
				id={htmlFor}
				placeholder={placeholder}
				onChange={(event) => {
					changeValue(event.target.value)
				}}
			/>
		</label>
	)
}

export default InputStartGame

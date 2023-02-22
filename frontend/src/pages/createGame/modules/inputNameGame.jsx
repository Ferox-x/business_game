import React from "react"
import "../modules/createGameStyles/inputNameGame.scss"

function InputNameGame({ value, setValue, ...props }) {
	return (
		<input
			value={value}
			onChange={(event) => {
				setValue(event.target.value)
			}}
			className={"input_create_game"}
			placeholder={"Введите название игры"}
		></input>
	)
}

export default InputNameGame

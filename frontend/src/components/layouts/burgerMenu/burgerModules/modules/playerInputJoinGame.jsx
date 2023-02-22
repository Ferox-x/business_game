import React from "react"
import "../burgerStyles/playerInputJoinGame.scss"

function PlayerInputJoinGame(props) {
	return (
		<input
			className={"input_join_game"}
			placeholder={"Введите пригласительный код"}
		></input>
	)
}

export default PlayerInputJoinGame

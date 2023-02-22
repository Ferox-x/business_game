import React from "react"
import "../burgerStyles/buttonCreateGame.css"

function PlayerButtonJoinCode({ children, ...props }) {
	return <div className={"btn_create_game btn_join_game btn_reset"}>{children}</div>
}

export default PlayerButtonJoinCode

import React from "react"
import "../burgerStyles/buttonCreateGame.css"

function ButtonCreateGame({ classname, children, onClick, ...props }) {
	return (
		<div className={"btn_create_game btn_reset"} onClick={onClick}>
			{children}
		</div>
	)
}

export default ButtonCreateGame

import React from "react"
import "../burgerStyles/buttonCreateGame.css"

function ButtonCreateGame({ classname, children, ...props }) {
	return <div className={"btn_create_game btn_reset"}>{children}</div>
}

export default ButtonCreateGame
